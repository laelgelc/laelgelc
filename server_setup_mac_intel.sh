#!/bin/bash

# Create a directory named 'work' in the user's home directory and clone the 'laelgelc' repository in it:
# Rog-Mac:~ eyamrog$ mkdir work
# Rog-Mac:~ eyamrog$ cd work
# Rog-Mac:work eyamrog$ git clone https://github.com/laelgelc/laelgelc.git

clear

# Updating and upgrading the system
brew update && brew upgrade || { echo "Failed to update and upgrade packages"; exit 1; }

# Installing necessary packages
#brew install awscli
brew install xsel ripgrep html2text zip unzip pipx ffmpeg

# Creating directory for TreeTagger
mkdir -p "$HOME"/treetagger/

# Defining base URL for TreeTagger files
BASE_URL="https://cis.uni-muenchen.de/~schmid/tools/TreeTagger/data"

# Downloading TreeTagger - uncomment the version of programme that matches the type of system
cd "$HOME"/treetagger/
curl -O "${BASE_URL}/tree-tagger-MacOSX-Intel-3.2.3.tar.gz"
curl -O "${BASE_URL}/tagger-scripts.tar.gz"
curl -O "${BASE_URL}/install-tagger.sh"
curl -O "${BASE_URL}/english.par.gz"
curl -O "${BASE_URL}/portuguese2.par.gz"

# Installing TreeTagger
chmod +x "$HOME"/treetagger/install-tagger.sh
"$HOME"/treetagger/install-tagger.sh

# Appending TreeTagger paths to .zshrc
echo >> "$HOME"/.zshrc
echo "# The following lines add TreeTagger to the PATH variable" >> "$HOME"/.zshrc
echo "export PATH=\$PATH:/Users/eyamrog/treetagger/cmd" >> "$HOME"/.zshrc
echo "export PATH=\$PATH:/Users/eyamrog/treetagger/bin" >> "$HOME"/.zshrc
#source "$HOME"/.zshrc

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

# macOS system files
.DS_Store

# Environment & secrets
.env
*.env

# JupyterLab
.ipynb_checkpoints/

# RStudio
.Rhistory

# LaTeX
*.aux
*.bbl
*.blg
*.lof
*.log
*.lol
*.lot
*.out
*.toc
*.fls
*.fdb_latexmk
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
#sudo shutdown -r now
