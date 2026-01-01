#!/bin/bash

# Create a directory named 'work' in the user's home directory and clone the 'laelgelc' repository in it:
# ubuntu@ip-172-31-43-202:~$ mkdir work
# ubuntu@ip-172-31-43-202:~$ cd work
# ubuntu@ip-172-31-43-202:~/work$ git clone https://github.com/laelgelc/laelgelc.git

clear

# Updating and upgrading the system
sudo apt update && sudo apt upgrade -y || { echo "Failed to update and upgrade packages"; exit 1; }

# Installing necessary packages
sudo snap install aws-cli --classic
sudo apt install -y python3-pip python3-venv git curl xsel ripgrep html2text zip unzip bzip2 pipx ffmpeg tesseract-ocr ocrmypdf

# Creating directory for TreeTagger
mkdir -p "$HOME"/treetagger/

# Defining base URL for TreeTagger files
BASE_URL="https://cis.uni-muenchen.de/~schmid/tools/TreeTagger/data"

# Downloading TreeTagger - uncomment the version of programme that matches the type of system
cd "$HOME"/treetagger/
#curl -O "${BASE_URL}/tree-tagger-linux-3.2.5.tar.gz"
curl -O "${BASE_URL}/tree-tagger-ARM64-3.2.tar.gz"
curl -O "${BASE_URL}/tagger-scripts.tar.gz"
curl -O "${BASE_URL}/install-tagger.sh"
curl -O "${BASE_URL}/english.par.gz"
curl -O "${BASE_URL}/portuguese2.par.gz"

# Installing TreeTagger
chmod +x "$HOME"/treetagger/install-tagger.sh
"$HOME"/treetagger/install-tagger.sh

# Appending TreeTagger paths to .bashrc
echo >> "$HOME"/.bashrc
echo "# The following lines add TreeTagger to the PATH variable" >> "$HOME"/.bashrc
echo "export PATH=\$PATH:/home/ubuntu/treetagger/cmd" >> "$HOME"/.bashrc
echo "export PATH=\$PATH:/home/ubuntu/treetagger/bin" >> "$HOME"/.bashrc
#source "$HOME"/.bashrc

# Setting up Python virtual environment
# Regarding Google Cloud Python APIs, please check https://github.com/googleapis/google-cloud-python
cd "$HOME"
#python3 -m pip install --upgrade pip
python3 -m venv my_env
source "$HOME"/my_env/bin/activate
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment not activated!"
    exit 1
fi
pip install -r "$HOME"/work/laelgelc/my_env.req
#pip install --upgrade -r "$HOME"/work/laelgelc/my_env.req
python -m ipykernel install --user --name=my_env

# Setting up 'git' global parameters
## Ensure Git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed!"
    exit 1
fi

## Set Git global parameters
git config --global user.name "Rogério Yamada"
git config --global user.email "eyamrog@gmail.com"

## Create or update global .gitignore
touch "$HOME"/.gitignore_global
cat << EOF >> "$HOME"/.gitignore_global
# General
nohup.out

# Environment & secrets
.env

# JupyterLab
.ipynb_checkpoints/

# RStudio
.Rhistory

# LaTeX
*.aux
*.bbl
*.bcf
*.blg
*.lof
*.log
*.lol
*.lot
*.out
*.toc
*.fls
*.fdb_latexmk
*.run.xml
*.synctex.gz
*.nav
*.snm
*.vrb
*.dvi
*.ps
*.synctex

EOF

## Set global excludesfile
git config --global core.excludesfile "$HOME"/.gitignore_global

## Confirm configuration
#git config --global --list

# Rebooting the system for kernel's update
#sudo reboot
