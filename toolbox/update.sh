#!/usr/bin/env bash

set -euo pipefail

# ============================================================
# Daily Ubuntu / Snap / Conda / Git maintenance script
# ============================================================

PROJECTS_DIR="$HOME/PycharmProjects"
#GITALL_SCRIPT="$PROJECTS_DIR/gitall.py"
GITALL_SCRIPT="$PROJECTS_DIR/laelgelc/toolbox/gitall.py"
CONDA_ENV="my_env"
LOG_DIR="$HOME/update-logs"
LOG_FILE="$LOG_DIR/update-$(date '+%Y-%m-%d_%H-%M-%S').log"

mkdir -p "$LOG_DIR"

# Send all output both to terminal and log file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "============================================================"
echo "Starting update script"
echo "Date: $(date)"
echo "Log file: $LOG_FILE"
echo "============================================================"

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Error: required command not found: $1"
        exit 1
    fi
}

section() {
    echo
    echo "------------------------------------------------------------"
    echo "$1"
    echo "------------------------------------------------------------"
}

cleanup() {
    if [[ -n "${SUDO_KEEPALIVE_PID:-}" ]]; then
        kill "$SUDO_KEEPALIVE_PID" 2>/dev/null || true
    fi
}

trap cleanup EXIT

section "Checking required commands"

require_command sudo
require_command apt
require_command snap
require_command conda
require_command python

echo "All required commands are available."

section "Checking configured paths"

if [[ ! -d "$PROJECTS_DIR" ]]; then
    echo "Error: projects directory does not exist:"
    echo "$PROJECTS_DIR"
    exit 1
fi

if [[ ! -f "$GITALL_SCRIPT" ]]; then
    echo "Error: gitall.py was not found at:"
    echo "$GITALL_SCRIPT"
    echo
    echo "Please edit GITALL_SCRIPT near the top of this file."
    exit 1
fi

echo "Projects directory: $PROJECTS_DIR"
echo "Git helper script: $GITALL_SCRIPT"
echo "Conda environment: $CONDA_ENV"

section "Requesting sudo password"

sudo -v

# Keep sudo credentials alive while this script is running.
# This avoids repeated password prompts without storing the password.
while true; do
    sudo -n true
    sleep 60
    kill -0 "$$" || exit
done 2>/dev/null &

SUDO_KEEPALIVE_PID=$!

section "Disk usage before cleanup"

df -h

section "Updating apt package lists"

sudo apt update

section "Upgrading installed apt packages"

sudo apt upgrade -y

section "Performing full apt upgrade"

sudo apt full-upgrade -y

section "Removing unused apt packages"

sudo apt autoremove --purge -y

section "Cleaning apt cache"

sudo apt clean

section "Refreshing snap packages"

sudo snap refresh

section "Preparing Conda"

CONDA_BASE="$(conda info --base)"

if [[ ! -f "$CONDA_BASE/etc/profile.d/conda.sh" ]]; then
    echo "Error: Conda initialization script not found:"
    echo "$CONDA_BASE/etc/profile.d/conda.sh"
    exit 1
fi

# shellcheck source=/dev/null
source "$CONDA_BASE/etc/profile.d/conda.sh"

section "Cleaning Conda cache"

conda clean --all -y

section "Activating Conda environment"

conda activate "$CONDA_ENV"

section "Pulling all Git repositories"

cd "$PROJECTS_DIR"
python "$GITALL_SCRIPT" pull --base-dir "$PROJECTS_DIR"

section "Checking Git repository statuses"

python "$GITALL_SCRIPT" status --base-dir "$PROJECTS_DIR"

section "Disk usage after cleanup"

df -h

section "Update completed successfully"

echo "Finished at: $(date)"
echo "Log file saved to:"
echo "$LOG_FILE"
echo "============================================================"