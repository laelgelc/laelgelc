#!/bin/bash

# Create a directory named 'work' in the user's home directory and clone the 'laelgelc' repository in it:
# ubuntu@ip-172-31-43-202:~$ mkdir work
# ubuntu@ip-172-31-43-202:~$ cd work
# ubuntu@ip-172-31-43-202:~/work$ git clone https://github.com/laelgelc/laelgelc.git

clear

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- Starting System Update and Basic Packages Installation ---"

# Updating and upgrading the system
sudo apt update && sudo apt upgrade -y || { echo "Failed to update and upgrade packages"; exit 1; }

# Installing necessary packages
sudo snap install aws-cli --classic
sudo apt install -y python3-pip python3-venv git curl xsel ripgrep html2text zip unzip bzip2 pipx ffmpeg tesseract-ocr tesseract-ocr-por tesseract-ocr-spa ocrmypdf

echo "--- Starting TreeTagger Setup ---"

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

echo "--- Starting Python Virtual Environment Setup ---"

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

echo "--- Starting Git Global Parameters Setup ---"

# Ensure Git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed!"
    exit 1
fi

# Set Git global parameters
git config --global user.name "Rogério Yamada"
git config --global user.email "eyamrog@gmail.com"

# Create or update global .gitignore
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

# Set global excludesfile
git config --global core.excludesfile "$HOME"/.gitignore_global

# Confirm configuration
#git config --global --list

echo "--- Starting Firefox Non-Snap Setup ---"

# Remove Firefox Snap if needed
echo "Removing Firefox Snap..."
sudo snap remove firefox || true

# Add Mozilla Team PPA
echo "Adding Mozilla Team PPA..."
sudo add-apt-repository -y ppa:mozillateam/ppa

# Configure APT Priority for PPA
# This prevents Ubuntu from trying to reinstall the snap version
echo "Configuring PPA priorities..."
sudo tee /etc/apt/preferences.d/mozilla-firefox <<EOF
Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001

Package: firefox*
Pin: release o=Ubuntu*
Pin-Priority: -1
EOF

# Enable automatic updates for the PPA version
echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox

# Install Firefox and dependencies
echo "Installing Firefox and headless dependencies..."
sudo apt install -y firefox libasound2t64 libdbus-glib-1-2 libgtk-3-0t64 libx11-xcb1 xvfb

echo "--- Firefox Setup Complete! ---"
#firefox --version
apt policy firefox

echo "--- Starting GitHub SSH Setup ---"

# Generate SSH key pair
ssh-keygen -t ed25519 -C "eyamrog@gmail.com" -f "$HOME/.ssh/id_ed25519" -N ""

echo "SSH key generated. Here is your public key to add to GitHub:"
cat "$HOME/.ssh/id_ed25519.pub"

# Rebooting the system for kernel's update
#sudo reboot
