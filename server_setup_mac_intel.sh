#!/bin/bash

# Create a directory named 'work' in the user's home directory and clone the 'laelgelc' repository in it:
# Rog-Mac:~ eyamrog$ mkdir work
# Rog-Mac:~ eyamrog$ cd work
# Rog-Mac:work eyamrog$ git clone https://github.com/laelgelc/laelgelc.git

clear

# Updating and upgrading the system
brew update && brew upgrade || { echo "Failed to update and upgrade packages"; exit 1; }

# Installing necessary packages
brew install aws-cli
brew install python3-pip python3-venv xsel ripgrep html2text zip unzip pipx ffmpeg

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
#git config --global --list
git config --global user.name "Rogério Yamada"
git config --global user.email eyamrog@gmail.com

# Rebooting the system for kernel's update
#sudo shutdown -r now
