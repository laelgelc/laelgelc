# `conda` maintenance

## `conda` release notes

[conda release notes](https://docs.conda.io/projects/conda/en/latest/release-notes.html)

## Update `conda`

```shell
current_conda_version="$(conda --version | awk '{print $2}')"

echo "Current conda version: $current_conda_version"

latest_conda_version="$(
  conda search conda \
    | awk '/^conda[[:space:]]+/ {print $2}' \
    | sort -V \
    | tail -n 1
)"

if [[ -z "$latest_conda_version" ]]; then
    echo "Error: could not determine latest conda version" >&2
    exit 1
fi

read -r -p "Update conda to version $latest_conda_version? [y/N] " reply

case "$reply" in
    [yY]|[yY][eE][sS])
        conda install -n base -c defaults "conda=$latest_conda_version" --yes
        ;;
    *)
        echo "Skipping conda update."
        ;;
esac
```

## Update the `my_env` environment

```shell
REPO_DIR="$(find "$HOME" -type d -name laelgelc -exec test -d "{}/.git" \; -print -quit)"

if [[ -z "$REPO_DIR" ]]; then
    echo "Error: Git repository 'laelgelc' was not found under $HOME"
    exit 1
fi

CONDAENV_FILE="$REPO_DIR/setup/env/condaenv.yaml"

if [[ ! -f "$CONDAENV_FILE" ]]; then
    echo "Error: conda environment file was not found:"
    echo "$CONDAENV_FILE"
    exit 1
fi

echo "Repository found:"
echo "$REPO_DIR"
echo
echo "Conda environment file:"
echo "$CONDAENV_FILE"
echo

read -r -p "Update conda environment 'my_env' from this file? [y/N] " reply

case "$reply" in
    [yY]|[yY][eE][sS])
        conda activate my_env
        conda env update --file "$CONDAENV_FILE" --prune --yes
        ;;
    *)
        echo "Skipping conda environment update."
        ;;
esac
```