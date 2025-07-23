#!/bin/bash

# -----------------------------
# Section 1: List of notebooks
# -----------------------------
NOTEBOOKS=(
  "Cheat_sheet.ipynb"
  "Jupyter_Notebook_Template.ipynb"
  # Add more notebook filenames here
)

# -----------------------------------------------
# Section 2: Sync each notebook using 'jupytext'
# -----------------------------------------------
for nb in "${NOTEBOOKS[@]}"; do
  echo "Syncing $nb..."
  jupytext --sync "$nb"
done