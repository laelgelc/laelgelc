#!/usr/bin/env bash
# Run: bash run_python_ec2.sh [options] -- command [args...]
# Use --help for options and shutdown/exit behavior.
set -uo pipefail

usage() {
  cat <<'EOF'
Usage: bash run_python_ec2.sh [options] -- command [args...]
  --config PATH          Read settings from PATH instead of the adjacent default.
  --no-config            Ignore the adjacent default configuration.
  --dry-run              Do not activate, validate, run, notify, or stop.
  --no-stop-on-failure   Leave the instance running if setup, validation,
                         command, or signal handling fails.
  --stop-on-failure      Request a stop on failure (the default).
  --conda-env NAME       Activate this Conda environment before running.
  --conda-sh PATH        Conda shell initialization script (required with --conda-env).
  --sns-topic-arn ARN    Publish a notification before requesting stop.
  --sns-region REGION    SNS region (default: region in topic ARN).
  --validate PATH        Run this executable with the command and its arguments
                         after activation and before the command.
  --help                 Show this help; no shutdown is attempted.

By default a valid invocation requests an EC2 stop even if the command fails.
IMDSv2, curl, the AWS CLI and EC2 stop permissions are required; SNS publish
permission is also required if configured. A notification failure is reported
but does not prevent the stop request. Exit status is the command/setup/signal
status if nonzero, otherwise 1 if notification or shutdown failed, otherwise 0.
The dry run prints no command arguments. Neither SNS nor launcher messages
include command arguments. The command and validation hook may log them.
An optional run_python_ec2.conf next to the launcher is read as literal
KEY=VALUE data, not shell code. CLI options override configuration settings.
EOF
}

dry_run=0
no_stop_on_failure=0
conda_env= conda_sh= sns_topic= sns_region= validator=
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P) || exit 2
config_path=$script_dir/run_python_ec2.conf
config_explicit=0
config_disabled=0
# Locate configuration before parsing overrides; stop at the workload boundary.
args=("$@")
for ((i=0; i<${#args[@]}; i++)); do
  case ${args[i]} in
    --) break ;;
    --config)
      if ((i + 1 >= ${#args[@]})) || [[ -z ${args[i+1]} || ${args[i+1]} == --* ]]; then
        printf 'Missing value for --config\n' >&2; exit 2
      fi
      ((i+=1)); config_path=${args[i]}; config_explicit=1; config_disabled=0 ;;
    --no-config) config_disabled=1; config_explicit=0 ;;
    --conda-env|--conda-sh|--sns-topic-arn|--sns-region|--validate) ((i+=1)) ;;
  esac
done
if ((!config_disabled)); then
  if [[ -e $config_path || -L $config_path ]]; then
    if [[ ! -f $config_path || ! -r $config_path ]]; then
      printf 'Cannot read configuration: %s\n' "$config_path" >&2; exit 2
    fi
    config_dir=$(cd -- "$(dirname -- "$config_path")" && pwd -P) || exit 2
    declare -A config_seen=()
    line_number=0
    while IFS= read -r line || [[ -n $line ]]; do
      ((line_number+=1))
      [[ $line =~ ^[[:space:]]*$ || $line =~ ^[[:space:]]*# ]] && continue
      if [[ ! $line =~ ^([a-z_]+)=(.*)$ ]]; then
        printf 'Invalid configuration line %s\n' "$line_number" >&2; exit 2
      fi
      key=${BASH_REMATCH[1]} value=${BASH_REMATCH[2]}
      if [[ -n ${config_seen[$key]+set} ]]; then
        printf 'Duplicate configuration key: %s\n' "$key" >&2; exit 2
      fi
      config_seen[$key]=1
      case $key in
        conda_env) conda_env=$value ;;
        conda_sh) conda_sh=$value; [[ -z $value || $value == /* ]] || conda_sh=$config_dir/$value ;;
        sns_topic_arn) sns_topic=$value ;;
        sns_region) sns_region=$value ;;
        validate) validator=$value; [[ -z $value || $value == /* ]] || validator=$config_dir/$value ;;
        stop_on_failure)
          case $value in true) no_stop_on_failure=0 ;; false) no_stop_on_failure=1 ;;
            *) printf 'Invalid stop_on_failure value\n' >&2; exit 2 ;; esac ;;
        *) printf 'Unknown configuration key: %s\n' "$key" >&2; exit 2 ;;
      esac
    done < "$config_path"
  elif ((config_explicit)); then
    printf 'Configuration not found: %s\n' "$config_path" >&2; exit 2
  fi
fi
while (($#)); do
  case "$1" in
    --help) usage; exit 0 ;;
    --dry-run) dry_run=1; shift ;;
    --no-stop-on-failure) no_stop_on_failure=1; shift ;;
    --stop-on-failure) no_stop_on_failure=0; shift ;;
    --no-config) shift ;;
    --config) shift 2 ;;
    --conda-env|--conda-sh|--sns-topic-arn|--sns-region|--validate)
      option=$1
      if (($# < 2)) || [[ -z $2 || $2 == --* ]]; then
        printf 'Missing value for %s\n' "$option" >&2; exit 2
      fi
      case "$option" in
        --conda-env) conda_env=$2 ;;
        --conda-sh) conda_sh=$2 ;;
        --sns-topic-arn) sns_topic=$2 ;;
        --sns-region) sns_region=$2 ;;
        --validate) validator=$2 ;;
      esac
      shift 2 ;;
    --) shift; break ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done
if (($# == 0)) || [[ -z $1 ]]; then
  printf 'A command is required after --.\n' >&2; exit 2
fi
if [[ -n $conda_env && -z $conda_sh || -z $conda_env && -n $conda_sh ]]; then
  printf 'Both --conda-env and --conda-sh are required together.\n' >&2; exit 2
fi
if ((dry_run)); then
  printf 'Dry run: command, validation, environment activation, SNS and EC2 stop skipped.\n'
  exit 0
fi

stop_instance() {
  local status=$1 token instance_id region topic_region result=0 action
  if ! command -v curl >/dev/null || ! command -v aws >/dev/null; then
    printf 'Error: curl and AWS CLI are required to stop the instance.\n' >&2
    return 1
  fi
  if ! token=$(curl -fsS --connect-timeout 2 --max-time 5 -X PUT \
      http://169.254.169.254/latest/api/token \
      -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600') || [[ -z $token ]]; then
    printf 'Error: unable to obtain IMDSv2 token; instance not stopped.\n' >&2; return 1
  fi
  if ! instance_id=$(curl -fsS --connect-timeout 2 --max-time 5 \
      -H "X-aws-ec2-metadata-token: $token" \
      http://169.254.169.254/latest/meta-data/instance-id) || [[ ! $instance_id =~ ^i-[a-zA-Z0-9]+$ ]]; then
    printf 'Error: unable to obtain a valid instance ID; instance not stopped.\n' >&2; return 1
  fi
  region=$(curl -fsS --connect-timeout 2 --max-time 5 \
      -H "X-aws-ec2-metadata-token: $token" \
      http://169.254.169.254/latest/meta-data/placement/region) || region=
  region=${region:-${AWS_REGION:-${AWS_DEFAULT_REGION:-}}}
  if [[ ! $region =~ ^[a-z0-9-]+$ ]]; then
    printf 'Error: unable to determine instance region; instance not stopped.\n' >&2; return 1
  fi
  action='a stop will be requested'
  if ((no_stop_on_failure && status != 0)); then
    action='the instance will be left running'
  fi
  if [[ -n $sns_topic ]]; then
    topic_region=$sns_region
    if [[ -z $topic_region ]]; then
      IFS=: read -r _ _ _ topic_region _ <<< "$sns_topic"
    fi
    if [[ ! $topic_region =~ ^[a-z0-9-]+$ ]]; then
      printf 'Error: unable to determine SNS region.\n' >&2; result=1
    elif ! aws sns publish --region "$topic_region" --topic-arn "$sns_topic" \
        --subject 'EC2 job finished' \
        --message "EC2 job on $instance_id in $region finished with exit status $status; $action." >/dev/null; then
      printf 'Error: SNS notification failed.\n' >&2; result=1
    fi
  fi
  if ((no_stop_on_failure && status != 0)); then
    printf 'Failure: leaving instance running as requested.\n' >&2
    return "$result"
  fi
  if aws ec2 stop-instances --region "$region" --instance-ids "$instance_id" >/dev/null; then
    printf 'Stop requested for instance %s in %s.\n' "$instance_id" "$region"
  else
    printf 'Error: EC2 stop request failed.\n' >&2; result=1
  fi
  return "$result"
}

child=
on_signal() {
  local signal=$1 status=$2
  trap '' INT TERM HUP
  if [[ -n $child ]]; then
    kill -s "$signal" "$child" 2>/dev/null || :
    wait "$child" 2>/dev/null || :
    child=
  fi
  exit "$status"
}
finish() {
  local status=$?
  trap - EXIT
  trap '' INT TERM HUP
  if ! stop_instance "$status"; then
    if ((status == 0)); then status=1; fi
  fi
  exit "$status"
}
trap finish EXIT
trap 'on_signal INT 130' INT
trap 'on_signal TERM 143' TERM
trap 'on_signal HUP 129' HUP

if [[ -n $conda_env ]]; then
  if [[ ! -f $conda_sh ]] || ! source "$conda_sh" || ! conda activate "$conda_env"; then
    printf 'Error: Conda activation failed.\n' >&2; exit 1
  fi
fi
run_child() {
  "$@" &
  child=$!
  local status=0
  wait "$child" || status=$?
  child=
  return "$status"
}
if [[ -n $validator ]]; then
  run_child "$validator" "$@" || exit $?
fi
run_child "$@"