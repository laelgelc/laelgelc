#!/bin/bash

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
# macOS system files
.DS_Store

# Environment & secrets
.env
EOF

## Set global excludesfile
git config --global core.excludesfile "$HOME"/.gitignore_global

## Confirm configuration
git config --global --list
