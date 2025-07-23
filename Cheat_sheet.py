# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# <center>
# <img src="https://laelgelcpublic.s3.sa-east-1.amazonaws.com/lael_50_years_narrow_white.png.no_years.400px_96dpi.png" width="300" alt="LAEL 50 years logo">
# <h3>APPLIED LINGUISTICS GRADUATE PROGRAMME (LAEL)</h3>
# </center>
# <hr>

# %% [markdown]
# # Cheat sheet

# %% [markdown]
# ## LaTeX compilation

# %% [markdown]
# ### `latexmk` - Automatic LaTeX document generation routine

# %% [markdown]
# ```
# (my_env) eyamrog@Rog-iMac cl_st1_eyamrog_en % latexmk -pdf main.tex
# ``

# %% [markdown]
# | Command                    | What It Does                                     |
# |----------------------------|--------------------------------------------------|
# | latexmk -pdf main.tex      | Compile to PDF using pdfLaTeX                    |
# | latexmk -lualatex main.tex | Compile to PDF using LuaLaTeX                    |
# | latexmk -xelatex main.tex  | Compile to PDF using XeLaTeX                     |
# | latexmk -c                 | Clean up auxiliary files                         |
# | latexmk -C                 | Clean everything, including the PDF              |
# | latexmk -pdf -f main.tex   | Force compilation with pdfLaTeX even with errors |
#

# %% [markdown]
# ### LaTeX mumbo jumbo

# %% [markdown]
# ```
# (my_env) eyamrog@Rog-iMac cl_st1_eyamrog_en % pdflatex main.tex
# (my_env) eyamrog@Rog-iMac cl_st1_eyamrog_en % bibtex main
# (my_env) eyamrog@Rog-iMac cl_st1_eyamrog_en % pdflatex main.tex
# (my_env) eyamrog@Rog-iMac cl_st1_eyamrog_en % pdflatex main.tex
# ```

# %% [markdown]
# ## PyCharm shortcuts

# %% [markdown]
# ### Move the cursor:

# %% [markdown]
# - to the end of a line
#     - `Cmd` + `Rigth Arrow key` (macOS)
# - to the beginning of a line
#     - `Cmd` + `Left Arrow key` (macOS)

# %% [markdown]
# ### Place cursors in specific points in the text

# %% [markdown]
# Hold the following key and click where you want each cursor
# - `Option` (macOS)
# - `Alt` (Windows/Linux)

# %% [markdown]
# ### Place cursors in multiple consecutive lines

# %% [markdown]
# #### Method 1

# %% [markdown]
# 1. Select the entire block of lines
# 2. Press:
# - `Option` + `Shift` + `G` (macOS)
# - `Alt` + `Shift` + `G` (Windows/Linux)
#
# This places a cursor at the end of each selected line. You can also move the cursors to the beginning of the line with `Cmd` + `Left Arrow key`

# %% [markdown]
# #### Method 2

# %% [markdown]
# Toggle to `Column Selection Mode` with the following shortcuts then drag your mouse down the column to place cursors
# - `Cmd` + `Shift` + `8` (macOS)
# - `Alt` + `Shift` + `Insert` (Windows/Linux)

# %% [markdown]
# ### Change all occurrences of a word

# %% [markdown]
# - `Cmd` + `Ctrl` + `G` (macOS)
# - `Ctrl` + `Alt` + `Shift` + `J` (Windows/Linux)

# %% [markdown]
# ## Pairing Jupyter Notebooks with `Jupytext`

# %% [markdown]
# ### Pair a notebook with
# Jupytext will automatically sync changes between the `ipynb` and `.py` files when you save either one in Jupyter Notebook or JupyterLab. If you use another editor, you have to run Jupytext's synchronisation command.

# %% [markdown]
# ```
# jupytext --set-formats ipynb,py:percent notebook.ipynb
# ```

# %% [markdown]
# ### Synchronize the paired files with
# (the inputs are loaded from the most recent paired file)

# %% [markdown]
# ```
# jupytext --sync notebook.py
# ```

# %% [markdown]
# ### Unpair the files with

# %% [markdown]
# ```
# jupytext --set-formats ipynb notebook.ipynb
# ```

# %% [markdown]
# ### Convert a notebook in one format to another with
# (use -o if you want a specific output file)

# %% [markdown]
# ```
# jupytext --to ipynb notebook.py
# ```

# %% [markdown]
# ## Logging

# %% [markdown]
# ### Option 1

# %%
log_filename = f"{filename}.log"

# Setting up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

# %% [markdown]
# ### Option 2

# %%
# Setting up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{output_directory}/chatgpt_review.log"),
        logging.StreamHandler()
    ]
)

# %% [markdown]
# ## Formatting HTML files with VS Code's built-in formatter

# %% [markdown]
# Open the HTML file and press `Shift + Alt + F`

# %% [markdown]
# ## Checking the amount of RAM, CPU and Disk on an Ubuntu host

# %% [markdown]
# ```
# eyamrog@Rog-ASUS:~$ free -h
#                total        used        free      shared  buff/cache   available
# Mem:           7.8Gi       860Mi       6.0Gi       3.0Mi       921Mi       6.6Gi
# Swap:          2.0Gi       3.0Mi       2.0Gi
# eyamrog@Rog-ASUS:~$ nproc
# 12
# eyamrog@Rog-ASUS:~$ df -h
# Filesystem      Size  Used Avail Use% Mounted on
# none            3.9G     0  3.9G   0% /usr/lib/modules/6.6.87.2-microsoft-standard-WSL2
# none            3.9G  4.0K  3.9G   1% /mnt/wsl
# drivers         952G  213G  740G  23% /usr/lib/wsl/drivers
# /dev/sdd       1007G   12G  945G   2% /
# none            3.9G   80K  3.9G   1% /mnt/wslg
# none            3.9G     0  3.9G   0% /usr/lib/wsl/lib
# rootfs          3.9G  2.7M  3.9G   1% /init
# none            3.9G  896K  3.9G   1% /run
# none            3.9G     0  3.9G   0% /run/lock
# none            3.9G     0  3.9G   0% /run/shm
# none            3.9G   76K  3.9G   1% /mnt/wslg/versions.txt
# none            3.9G   76K  3.9G   1% /mnt/wslg/doc
# C:\             952G  213G  740G  23% /mnt/c
# snapfuse        128K  128K     0 100% /snap/bare/5
# snapfuse         56M   56M     0 100% /snap/aws-cli/1526
# snapfuse         74M   74M     0 100% /snap/core22/2010
# snapfuse         56M   56M     0 100% /snap/aws-cli/1518
# snapfuse         74M   74M     0 100% /snap/core22/2045
# snapfuse         92M   92M     0 100% /snap/gtk-common-themes/1535
# snapfuse         51M   51M     0 100% /snap/snapd/24718
# snapfuse         50M   50M     0 100% /snap/snapd/24792
# snapfuse        132M  132M     0 100% /snap/ubuntu-desktop-installer/1276
# snapfuse        132M  132M     0 100% /snap/ubuntu-desktop-installer/1286
# tmpfs           3.9G  4.0K  3.9G   1% /run/user/1000
# eyamrog@Rog-ASUS:~$ 
# ```

# %% [markdown]
# ## macOS

# %% [markdown]
# ### Capturing an image from a Jupyter Notebook over JupyterLab

# %% [markdown]
# This shortcut works for Windows as well.

# %% [markdown]
# `Shift` + `Right click`

# %% [markdown]
# ### Capturing a portion of screen shot

# %% [markdown]
# `Shift` + `Command` + 4

# %% [markdown]
# ### Capturing a portion of screen shot

# %% [markdown]
# `Shift` + `Command` + 3

# %% [markdown]
# ### Select a line

# %% [markdown]
# `Shift` + `Command` + `Right/Left arrow`

# %% [markdown]
# ### Copy a directory recursively

# %% [markdown]
# ```
# cp -R <source_directory> <destination_directory>
# ```

# %% [markdown]
# ## Windows PowerShell

# %% [markdown]
# ```
# # Set a temporary alias on Windows PowerShell to turn `dir` into `ll`
# Set-Alias ll dir
#
# # Command similar to `tail -f <file>`
# Get-Content <file> -Wait
#
# # Remove a directory recursively like `rm -r <path>`
# Remove-Item -Recurse -Force <path>
# ```

# %% [markdown]
# ## Windows shortcuts to minimise all windows

# %% [markdown]
# - `Win` + `D`: Shows the desktop (minimises all windows) - Press again to restore them
# - `Win` + `M`: Minimises all windows (but doesn’t restore them with a second press)
# - `Win` + `Shift` + `M`: Restores all minimised windows after using `Win` + `M`

# %% [markdown]
# ## Pandoc

# %% [markdown]
# ```
# pandoc -s <yourfile>.tex -o <cleaned_text>.txt
# ```

# %% [markdown]
# ## TeX Live

# %% [markdown]
# ```
# tlmgr --help
# tlmgr update --self      # Updates tlmgr itself
# tlmgr update --list
# tlmgr update --all       # Updates all installed packages
# tlmgr install <package>  # Installs a specific package
# ```

# %% [markdown]
# ## Parallels Desktop

# %% [markdown]
# ### Mounting the CDROM to install `Parallels Guest Tools` on an Ubuntu server without GUI

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ sudo mkdir /media/cdrom
# eyamrog@ubuntu:~$ sudo mount -o exec /dev/sr0 /media/cdrom
# eyamrog@ubuntu:~$ cd /media/cdrom
# eyamrog@ubuntu:~$ sudo ./install
# ```

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ sudo umount /media/cdrom
# ```

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ ls /media/psf/Home
# ```

# %% [markdown]
# ### Mapping the host's home directory to the Ubuntu server's home directory

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ cd $HOME
# eyamrog@ubuntu:~$ ls /media/psf/Home
# eyamrog@ubuntu:~$ ln -s /media/psf/Home /home/eyamrog/host_home
# eyamrog@ubuntu:~$ ls host_home
# ```

# %% [markdown]
# ## Enabling `SSH` on an Ubuntu server

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ sudo systemctl enable ssh
# eyamrog@ubuntu:~$ sudo systemctl start ssh
# eyamrog@ubuntu:~$ sudo systemctl status ssh
# ```

# %% [markdown]
# ### Finding the Ubuntu server's IP address

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ ip a | grep "inet "
# ```

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ ssh your_username@your_server_ip
# ```

# %% [markdown]
# ### Generating SSH key pairs

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# ```

# %% [markdown]
# ### Deploying existing SSH key pairs

# %% [markdown]
# ```
# eyamrog@ubuntu:~$ cat ./host_home/work/key_pairs/eyamrog1.pub >> ./.ssh/authorized_keys
# eyamrog@ubuntu:~$ chmod 600 ./.ssh/authorized_keys
# eyamrog@ubuntu:~$ ll ./.ssh/
# total 12
# drwx------ 2 eyamrog eyamrog 4096 Jul 15 12:33 ./
# drwxr-x--- 7 eyamrog eyamrog 4096 Jul 15 12:06 ../
# -rw------- 1 eyamrog eyamrog  743 Jul 15 12:35 authorized_keys
# eyamrog@ubuntu:~$ 
# ```

# %% [markdown]
# ## Ubuntu server graceful shutdown

# %% [markdown]
# ```
# sudo poweroff
# ```

# %% [markdown]
# ```
# sudo shutdown -h now
# ```

# %% [markdown]
# ## Archiving

# %% [markdown]
# ```
# # Creates a compressed archive file of the contents of the `cl_images` directory
# tar czvf cl_images_eyamrog.tar.gz cl_images
#
# # Creates a compressed archive file. The `-C` option changes the directory to `cl_images` before adding its contents to the archive file
# tar czvf cl_images_eyamrog.tar.gz -C cl_images .
#
# # Extracts the contents of the archive file
# tar xzvf cl_images_eyamrog.tar.gz
#
# # Extracts the contents of the archive file. The `-C` option is used to change the directory to `cl_images` before extracting the files from the archive 
# mkdir cl_images
# tar xzvf cl_images_eyamrog.tar.gz -C cl_images
#
# # Installs `zip` and `unzip` commands
# sudo apt install -y zip
#
# # Creates a compressed `.zip` file of the contents of the `directory` directory
# zip -r directory.zip /path/to/directory
#
# # Creates a compressed `.zip` file of the contents of the `file` file
# zip file.zip file
#
# # Split a large ZIP file into 100MB parts
# split -b 100m large_file.zip large_file_zip_part_
#
# # Reassemble the large ZIP file
# cat large_file_zip_part_* > large_file.zip
#
# # Lists the contents of the ZIP file before extracting it
# unzip -l large_file.zip
#
# # Verifies (tests) the contents of the ZIP file for integrity
# unzip -t large_file.zip
#
# # Extracts the contents of the `.zip` archive
# unzip file.zip
#
# # Extracts the contents of the `.zip` archive into the `directory` directory
# mkdir /path/to/directory
# unzip file.zip -d /path/to/directory
# ```

# %% [markdown]
# ## Git

# %% [markdown]
# ```
# git clone https://github.com/laelgelc/cl_images.git
#
# git config --global --edit
#
# git status
#
# git add <file>
#
# git add .
#
# git restore --staged <file>
#
# git restore <file>
#
# git stash
# # Save your current changes and revert your working directory to match the HEAD commit
# # Great for when you need to switch branches quickly but don't want to commit your incomplete work
#
# git stash list
#
# git stash apply
# # Reapply the most recent stash
#
# git stash apply stash@{1}
#
# git stash drop
# # Delete the most recent stash
#
# git stash drop stash@{1}
#
# git pull
#
# git commit -m "20231221-1156"
#
# git push
#
# git reset --soft HEAD~1
# # Undo the commit but keep the changes
#
# git reset HEAD~1
# # Undo the commit and unstage the changes
#
# git log
# # Type 'q' to exit the log view
#
# find . -type f -size +100M
# # Search through the specified directory and its subdirectories to find files that are larger than 100 MB
#
# Get-ChildItem -Path . -File -Recurse | Where-Object {$_.Length -gt 100MB}
# # Windows PowerShell equivalent of the previous command
#
# find . -type f -name "*old*"
# # Search through the specified directory and its subdirectories to find files that have 'old' in its filename
#
# zip file.zip file
# # Compress files that were found to be larger than 100 MB
#
# ll *.zip
# # Check all ZIP files, run the 'find' command again to confirm that the ZIP files are smaller than 100 MB
#
# # To completely disregard all changes in your local repository and restore it to match the remote repository, follow these steps:
# git status
# git reset --hard # Discard local changes and reset all modified files
# git checkout main # Ensure you're on the correct branch
# git fetch origin # Pull the latest changes from the remote repository
# git reset --hard origin/main # Forcefully match your local branch with the remote branch
#
# ```

# %% [markdown]
# ## Checking if two files are exactly the same at a binary level

# %% [markdown]
# ```
# (my_env) ubuntu@ip-172-31-28-113:~/work/cl_st1_gelc/ph1/tweets$ cmp tagged_ori.txt tagged.txt
# (my_env) ubuntu@ip-172-31-28-113:~/work/cl_st1_gelc/ph1/tweets$ cmp tagged_ori.txt tokens.txt
# tagged_ori.txt tokens.txt differ: byte 9, line 1
# (my_env) ubuntu@ip-172-31-28-113:~/work/cl_st1_gelc/ph1/tweets$ 
# (my_env) ubuntu@ip-172-31-28-113:~/work/cl_st1_gelc/ph1/tweets$ diff -q tagged_ori.txt tagged.txt
# (my_env) ubuntu@ip-172-31-28-113:~/work/cl_st1_gelc/ph1/tweets$ diff -q tagged_ori.txt tokens.txt
# Files tagged_ori.txt and tokens.txt differ
# (my_env) ubuntu@ip-172-31-28-113:~/work/cl_st1_gelc/ph1/tweets$ 
# ```

# %% [markdown]
# ## Changing permissions of files recursively

# %% [markdown]
# ```
# chmod 755 --recursive group3/
# cd group3/
# find . -type f -exec chmod 644 {} \;
# ```

# %% [markdown]
# ## Amazon S3 Bucket policy for bucket public access
# Replace 'laelgelcclimages' by the corresponding bucket name

# %% [markdown]
# ```
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Principal": "*",
#             "Action": "s3:GetObject",
#             "Resource": "arn:aws:s3:::laelgelcclimages/*"
#         }
#     ]
# }
# ```

# %% [markdown]
# ## Google Cloud [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc)

# %% [markdown]
# ```
# ubuntu@ip-172-31-19-178:~/my_env$ source bin/activate
# (my_env) ubuntu@ip-172-31-19-178:~/my_env$ gcloud auth application-default login
# Go to the following link in your browser:
#
#     https://<omitted>
#
# Enter authorization code: <omitted>
#
# Credentials saved to file: [/home/ubuntu/.config/gcloud/application_default_credentials.json]
#
# These credentials will be used by any library that requests Application Default Credentials (ADC).
# WARNING: 
# Cannot find a quota project to add to ADC. You might receive a "quota exceeded" or "API not enabled" error. Run $ gcloud auth application-default set-quota-project to add a quota project.
# (my_env) ubuntu@ip-172-31-19-178:~/my_env$ gcloud auth application-default set-quota-project <omitted>
#
# Credentials saved to file: [/home/ubuntu/.config/gcloud/application_default_credentials.json]
#
# These credentials will be used by any library that requests Application Default Credentials (ADC).
#
# Quota project "<omitted>" was added to ADC which can be used by Google client libraries for billing and quota. Note that some services may still bill the project owning the resource.
# (my_env) ubuntu@ip-172-31-19-178:~/my_env$ 
# ```

# %% [markdown]
# ## OpenSSH

# %% [markdown] vscode={"languageId": "plaintext"}
# ```
# eyamrog@RogLet-ASUS:~$ sudo apt install putty-tools
# eyamrog@RogLet-ASUS:~$ cp /mnt/c/Users/eyamr/OneDrive/Documentos/0-Technology/LAELGELC20231117.ppk .
# eyamrog@RogLet-ASUS:~$ puttygen LAELGELC20231117.ppk -O private-openssh -o LAELGELC20231117.pem
# eyamrog@RogLet-ASUS:~$ chmod 400 LAELGELC20231117.pem
# eyamrog@RogLet-ASUS:~$ eval "$(ssh-agent -s)"
# Agent pid 924
# eyamrog@RogLet-ASUS:~$ ssh-add LAELGELC20231117.pem
# Identity added: LAELGELC20231117.pem (LAELGELC20231117.pem)
# eyamrog@RogLet-ASUS:~$ ssh -A -t ubuntu@ec2-18-231-160-175.sa-east-1.compute.amazonaws.com
# The authenticity of host 'ec2-18-231-160-175.sa-east-1.compute.amazonaws.com (18.231.160.175)' can't be established.
# ED25519 key fingerprint is SHA256:a/MtF4Zlyzxv9OIljp3Jr/BY2emQcl/6ZFHETKkmrjk.
# This key is not known by any other names
# Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
# Warning: Permanently added 'ec2-18-231-160-175.sa-east-1.compute.amazonaws.com' (ED25519) to the list of known hosts.
# Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.2.0-1016-aws x86_64)
#
#  * Documentation:  https://help.ubuntu.com
#  * Management:     https://landscape.canonical.com
#  * Support:        https://ubuntu.com/advantage
#
#   System information as of Sat Dec  2 15:29:51 UTC 2023
#
#   System load:  0.080078125       Processes:             96
#   Usage of /:   22.0% of 9.51GB   Users logged in:       0
#   Memory usage: 20%               IPv4 address for eth0: 172.31.36.94
#   Swap usage:   0%
#
#
# Expanded Security Maintenance for Applications is not enabled.
#
# 0 updates can be applied immediately.
#
# Enable ESM Apps to receive additional future security updates.
# See https://ubuntu.com/esm or run: sudo pro status
#
#
# Last login: Sat Dec  2 15:14:29 2023 from 189.120.73.98
# ubuntu@ip-172-31-36-94:~$ 
# ```

# %% [markdown]
# ## AWS CLI

# %% [markdown] vscode={"languageId": "plaintext"}
# ```
# # Listing the objects in a bucket with corresponding sizes and redirecting the output into a file
# aws s3 ls s3://laelgelctweets/ --human-readable --summarize > files.txt
#
# # Creating folders in a bucket
# PS C:\Users\eyamr> aws s3api put-object --bucket gelctweets --key 2019_01/
# {
#     "ETag": "\"d41d8cd98f00b204e9800998ecf8427e\"",
#     "ServerSideEncryption": "AES256"
# }
# ```

# %% [markdown]
# ## Anaconda Distribution

# %% [markdown]
# Python repositories:
# - https://anaconda.org/
# - https://pypi.org/

# %% [markdown]
# ### Environment management - via `condaenv.xml` file

# %% [markdown]
# ```
# (base) C:\Users\eyamr>cd Downloads
#
# (base) C:\Users\eyamr\Downloads>dir
#  Volume in drive C is OS
#  Volume Serial Number is B268-C40D
#
#  Directory of C:\Users\eyamr\Downloads
#
# 02/08/2024  10:59    <DIR>          .
# 19/07/2024  07:37    <DIR>          ..
# 02/08/2024  11:08               412 condaenv.yml
# 02/08/2024  11:04               809 scratchpad.sh
#                2 File(s)          1.221 bytes
#                2 Dir(s)  898.125.189.120 bytes free
#
# (base) C:\Users\eyamr\Downloads>conda env create -f condaenv.yml
# <omitted>
#
#
# (base) C:\Users\eyamr\Downloads>conda env list
# # conda environments:
# #
# base                  *  C:\Users\eyamr\anaconda3
# my_env                   C:\Users\eyamr\anaconda3\envs\my_env
#
#
# (base) C:\Users\eyamr\Downloads>conda activate my_env
#
# (my_env) C:\Users\eyamr\Downloads>conda list
# <omitted>
#
#
# (my_env) C:\Users\eyamr\Downloads>pip install gogettr truthbrush webvtt-py
# <omitted>
#
#
# (my_env) C:\Users\eyamr\Downloads>conda deactivate
#
# (base) C:\Users\eyamr\Downloads>exit
# ```

# %% [markdown]
# ### Environment management - manually

# %% [markdown]
# ```
# (base) C:\Users\eyamr>conda env list
# # conda environments:
# #
# base                  *  C:\Users\eyamr\anaconda3
# Env20240401              C:\Users\eyamr\anaconda3\envs\Env20240401
#
#
# (base) C:\Users\eyamr>conda remove --name Env20240401 --all
# (base) C:\Users\eyamr>conda create --name my_env
# (base) C:\Users\eyamr>conda activate my_env
# (my_env) C:\Users\eyamr>conda list
# # packages in environment at C:\Users\eyamr\anaconda3\envs\my_env:
# #
# # Name                    Version                   Build  Channel
#
# (my_env) C:\Users\eyamr> conda install beautifulsoup4
# (my_env) C:\Users\eyamr>conda install gogettr
# <omitted>
# PackagesNotFoundError: The following packages are not available from curren:
# <omitted>
# (my_env) C:\Users\eyamr>pip install gogettr
# (my_env) C:\Users\eyamr>
# ```

# %% [markdown]
# ### Cloud Notebooks

# %% [markdown] vscode={"languageId": "plaintext"}
# ```
# (base) 22:41 ~/LAEL GELC $ conda create --name env20231215 python=3.10 ipykernel -y
#
# (base) 22:47 ~/LAEL GELC $ conda activate env20231215                                                                                                                           
# (env20231215) 22:47 ~/LAEL GELC $ conda list   
#
# (env20231215) 22:57 ~/LAEL GELC $ conda install -c conda-forge pysmartdl
#
# (env20231215) 22:50 ~/LAEL GELC $ conda install pyspark
# ```

# %% [markdown]
# ## JupyterLab

# %% [markdown]
# ```
# source "$HOME"/my_env/bin/activate
# nohup jupyter-lab --ip 0.0.0.0 --no-browser --allow-root --ServerApp.root_dir="$HOME" &
# jupyter server list
# ```

# %% [markdown]
# ## Notes about Research Data Processing

# %% [markdown]
# ```
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ ll
# total 1224644
# drwxrwxrwx 1 eyamrog eyamrog       512 Apr 15 14:53  ./
# drwxrwxrwx 1 eyamrog eyamrog       512 Apr  1 03:07  ../
# drwxrwxrwx 1 eyamrog eyamrog       512 Apr 14 19:20  .ipynb_checkpoints/
# -rwxrwxrwx 1 eyamrog eyamrog       282 Mar 31 16:16  desktop.ini*
# -rwxrwxrwx 1 eyamrog eyamrog 231557811 Apr 15 14:49  text_uniq_first_view.tsv*
# -rwxrwxrwx 1 eyamrog eyamrog  58806097 Apr 15 14:53  text_uniq_first_view.xlsx*
# -rwxrwxrwx 1 eyamrog eyamrog 854050828 Apr 15 14:49  tweets_all2.tsv*
# -rwxrwxrwx 1 eyamrog eyamrog 109616884 Apr 15 14:52  tweets_all2.xlsx*
# -rwxrwxrwx 1 eyamrog eyamrog       165 Apr 15 14:53 '~$text_uniq_first_view.xlsx'*
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ grep -ic "petista" text_uniq_first_view.tsv
# 3527
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ grep -ic "lulista" text_uniq_first_view.tsv
# 383
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ grep -ic "pistola" text_uniq_first_view.tsv
# 298
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ grep -ic "entrevista" text_uniq_first_view.tsv
# 3812
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ grep -ic "soldado" text_uniq_first_view.tsv
# 386
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ grep -ic "comunista" text_uniq_first_view.tsv
# 2732
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ grep -ic "cuba" text_uniq_first_view.tsv
# 973
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$
#
# 20 a 50 mil tweets
#
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ grep -i "pistola" text_uniq_first_view.tsv > pistola.tsv
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ ll
# total 1224792
# drwxrwxrwx 1 eyamrog eyamrog       512 Apr 15 15:09  ./
# drwxrwxrwx 1 eyamrog eyamrog       512 Apr  1 03:07  ../
# drwxrwxrwx 1 eyamrog eyamrog       512 Apr 14 19:20  .ipynb_checkpoints/
# -rwxrwxrwx 1 eyamrog eyamrog         0 Apr 15 15:07  Scratch_Pad.txt*
# -rwxrwxrwx 1 eyamrog eyamrog       282 Mar 31 16:16  desktop.ini*
# -rwxrwxrwx 1 eyamrog eyamrog    148164 Apr 15 15:09  pistola.tsv*
#
# sample.tsv
#
# cat sample* > alltweets.tsv
#
#
# Para descobrir se 'Bolsonaro' está em todos os tweets que contém 'ladrão':
# grep -ic "ladrão" tweets_all2.tsv # Anote a quantidade
# grep -i "ladrão" tweets_all2.tsv > sample.tsv
# grep -ic "Bolsonaro" sample.tsv # Se a quantidade for a mesma, 'Bolsonaro' está em todos os tweets
#
#
# demoji package customisation
#
# change delimiters:
#  
# open /opt/homebrew/lib/python3.10/site-packages/demoji/__init__.py
#  
# then replace:
#  
# def replace_with_desc(string, sep=":"):
#  
# with:
#  
# def replace_with_desc(string, sep="<", sepb=">"):
#  
# and replace:
#  
#  
#         result = result.replace(emoji, sep + desc + sep)
#  
#  
# with
#  
#         result = result.replace(emoji, sep + desc + sepb)
#  
# save file and run:
#  
# demoji <text>
# has context menu
#
# Repositório no Dropbox
# https://www.dropbox.com/scl/fo/7y8jjo3ev8wb7u6r8nvcr/AF5u0Lv39mc-fJv3RXLA8Fw?rlkey=6ogy1gxrtgka85dyqaftav1sc&dl=0
# ```

# %% [markdown]
# ## Code snippets

# %% [markdown]
# ### Setup

# %% [markdown] vscode={"languageId": "plaintext"}
# ```
# # Attach the IAM Role 'S3-Admin-Access' to the Ubuntu EC2 instance
# sudo apt update
# sudo apt upgrade -y
# # Reboot the EC2 instance from the AWS Console
# sudo apt install -y awscli
# # Set up Python virtual environment
# sudo apt install -y python3-pip
# sudo apt install -y python3-venv
# python3 -m venv my_env
# source "$HOME"/my_env/bin/activate
# ```

# %% [markdown]
# ### Setup and Execution in background

# %% [markdown]
# ```
# # Spin up an EC2 instance (m5a.large)
# # Attach the 'S3-Admin-Access' IAM role to the EC2 instance
# git clone https://github.com/laelgelc/cl_st1_inrs.git
# cd cl_st1_inrs
# git config --global --edit
# bash setup_server.sh
# logout
# # Reboot the EC2 instance
# source ~/my_env/bin/activate
# cd cl_st1_inrs
# tar xzvf CL_St1_Ph2_INRS.tar.gz
# nohup python -u cl_st1_ph3_inrs.py &
# tail -f nohup.out
# nohup bash lmda.sh &
# deactivate
# logout
# ```

# %% [markdown]
# ### Slicing dataframes

# %% [markdown]
# ```
# # Cutting from row 8 onwards
# df = df.loc[8:]
# df = df.reset_index(drop=True)
# ```

# %% [markdown]
# ```
# # Cutting from the beginning until the row 504
# df = df.loc[:504]
# df = df.reset_index(drop=True)
# ```

# %% [markdown]
# ```
# #df_test = df_scielo_preprint_preChatGPT_en.head(4) # Alternative command
# df_test = df_scielo_preprint_preChatGPT_en.iloc[:4]
# df_test = df_test.reset_index(drop=True)
# ```

# %% [markdown]
# ```
# df_new_test.head(30)
# ```

# %% [markdown]
# ```
# df_new_test.iloc[124:183]
# ```

# %% [markdown]
# ### Handling cases of `SettingWithCopyWarning`

# %% [markdown]
# Pandas often raises a `SettingWithCopyWarning` when it detects an operation that might result in an unintended modification of a DataFrame. This warning occurs when you're trying to set a value on a slice or a subset of the DataFrame, which may or may not be a view or a copy of the original DataFrame. This behavior can lead to unpredictable results.
#
# Here’s a common scenario that triggers this warning:

# %% [markdown]
# ```
# import pandas as pd
#
# # Create a DataFrame
# data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
# df = pd.DataFrame(data)
#
# # Create a slice of the DataFrame
# subset_df = df[df['Age'] > 25]
#
# # Attempt to modify the slice directly
# subset_df['Age'] = subset_df['Age'] + 1
# ```

# %% [markdown]
# In this example, pandas raises a `SettingWithCopyWarning` because subset_df is a slice of the original DataFrame df, and modifying subset_df directly can lead to unexpected behavior.
#
# To avoid this warning, you should create an explicit copy of the slice before modifying it:

# %% [markdown]
# ```
# # Create an explicit copy of the slice
# subset_df = df[df['Age'] > 25].copy()
#
# # Now modify the copied DataFrame
# subset_df['Age'] = subset_df['Age'] + 1
# ```

# %% [markdown]
# This ensures that you’re working on a new DataFrame, and any changes won’t affect the original DataFrame, thus avoiding the warning.

# %% [markdown]
# ### Setting input and output filenames using `argparse` and `RegEx`

# %% [markdown]
# ```
# # Importing the required libraries
# import argparse
# import re
# import pandas as pd
#
# # Setting the input and output filenames
# parser = argparse.ArgumentParser(description='Getting input filename.')
# parser.add_argument(
#     '--input_filename', help='Input filename.')
# args = parser.parse_args()
#
# def add_pt_suffix(filename):
#     # Extract the base filename without the extension
#     base_filename = re.match(r'^([A-Za-z0-9-_,\s]+)\.[A-Za-z]{1,5}$', filename).group(1)
#     
#     # Append "_pt" to the base filename
#     new_filename = f'{base_filename}_pt'
#     
#     # Add the original file extension back
#     new_filename += re.search(r'\.[A-Za-z]{1,5}$', filename).group()
#     
#     return new_filename
#
# input_filename = args.input_filename
# output_filename = add_pt_suffix(input_filename)
#
# print(input_filename)
# print(output_filename)
# ```

# %% [markdown]
# Test with:

# %% [markdown]
# ```
# (my_env) eyamrog@Rog-ASUS:~$ python cl_st1_mariana_dataset.py --input_filename mari2016_1.jsonl
# mari2016_1.jsonl
# mari2016_1_pt.jsonl
# (my_env) eyamrog@Rog-ASUS:~$ 
# ```

# %% [markdown]
# ### Slicing the contents of a row with RegEx

# %% [markdown]
# ```
# df.at[0, 'Speaker'] = 1 # Adding column 'Speaker' by initialising it with a numeric value in order to avoid DtypeWarning
# df = df.astype('object') # Converting the column to the desired data type
#
# for index, row in df.iterrows():
#     match = re.match(r'^([a-zA-Z0-9_., ]+):\xa0', row['Text'])
#     if match:
#         speaker = match.group(1)
#         df.at[index, 'Speaker'] = speaker
#         text_without_speaker = row['Text'][len(match.group(0)):]
#         df.at[index, 'Text'] = text_without_speaker
#     else:
#         # Handle the case when no match is found (optional)
#         #df.at[index, 'Speaker'] = ''  # Set a default value
#         pass
# ```

# %% [markdown]
# ### Miscellaneous RegEx

# %% [markdown]
# ```
# moderators = re.match(r'(^\w+)', moderators).group(1)
#
# participants = re.match(r'^\w+ \w+ (\w+-\w+)', participants).group(1)
#
# moderators = re.sub(r', \w+$', '', moderators)
#
# df.loc[8, 'Text'] = re.sub(r'^\[\*\] ', '', df.loc[8, 'Text'])
#
# df.loc[5, 'Text'] = re.sub(r'^\w+ \w+, \w+\[\*\]', '', df.loc[5, 'Text'])
# ```

# %% [markdown]
# ### Checking and changing a dataframe cell

# %% [markdown]
# ```
# df.loc[103, 'Text']
# ```

# %% [markdown]
# ```
# df.loc[103, 'Text'] = re.sub(r':', ' -', df.loc[103, 'Text'])
# ```

# %% [markdown]
# ```
# df.loc[103, 'Text']
# ```

# %% [markdown]
# ### Dropping a row in a dataframe

# %% [markdown]
# ```
# df.drop(477, inplace=True)
# df = df.reset_index(drop=True)
#
# df.drop([1011, 1012, 1013], inplace=True)
# df = df.reset_index(drop=True)
# ```

# %% [markdown]
# ### Dropping a column in a dataframe

# %% [markdown]
# ```
# df_scielo_preprint_preChatGPT_en.drop('Text Paragraphs Count', axis=1, inplace=True)
#
# df_scielo_preprint_preChatGPT_en = df_scielo_preprint_preChatGPT_en.drop('Text Paragraphs Count', axis=1)
# ```

# %% [markdown]
# ### Creating a column with the value of a cell

# %% [markdown]
# ```
# title = df.at[0, 'Text']
# df['Title'] = title
#
# debate = df.at[2, 'Text']
# df['Debate'] = debate
#
# date = df.at[1, 'Text']
# df['Date'] = date
#
# participants = df.at[2, 'Text']
# participants = re.match(r'^\w+ (\w+-\w+-\w+)', participants).group(1)
# #participants = re.sub(r'^\w+:\n', '', participants)
# #participants = re.sub(r'\n', ' ', participants)
# df['Participants'] = participants
#
# moderators = df.at[5, 'Text']
# moderators = re.match(r'(^\w+ \w+)', moderators).group(1)
# #moderators = re.sub(r'^\w+:\n', '', moderators)
# df['Moderators'] = moderators
# ```

# %% [markdown]
# ### Consolidating multiple JSONL files into one JSONL file and transferring them

# %% [markdown]
# #### Code snippets

# %% [markdown]
# ##### Using `cat`

# %% [markdown] vscode={"languageId": "plaintext"}
# ```
# mkdir mari
#
# cd mari
#
# aws s3 cp s3://gelcawsemr/2019_1/filtered_tweets.jsonl/ . --recursive
#
# find . -type f | wc -l
#
# cat *.json > mari2019_1.jsonl
#
# aws s3 cp mari2019_1.jsonl s3://laelgelcawsemrmariana/
#
# rm *
# ```

# %% [markdown]
# ##### Using `jq`

# %% [markdown] vscode={"languageId": "plaintext"}
# ```
# sudo apt install -y jq
#
# mkdir mari
#
# cd mari
#
# aws s3 cp s3://gelcawsemr/2019_1/filtered_tweets.jsonl/ . --recursive
#
# find . -type f | wc -l
#
# find . -name '*.json' -print0 | xargs -0 jq -s '.' > mari2019_1.jsonl
#
# aws s3 cp mari2019_1.jsonl s3://laelgelcawsemrmariana/
#
# rm *
# ```

# %% [markdown]
# #### Via 'consolidate.sh'

# %% [markdown] vscode={"languageId": "plaintext"}
# ```
# !/bin/bash
#
# # Set parameters
# path="2019_03"
# filename="mari201903.jsonl"
# origin_bucket="gelcawsemr"
# destination_bucket="laelgelcawsemrmariana"
#
# # Create input directory
# mkdir "$HOME"/"$path"/
#
# # Copy JSON files to the input directory
# aws s3 cp s3://"$origin_bucket"/"$path"/filtered_tweets.jsonl/ $HOME/"$path"/ --recursive
#
# # Consolidate the JSON files into a single 
# cat "$HOME"/"$path"/*.json > $HOME/"$path"/"$filename"
#
# # Copy the consolidated file to the destination bucket
# aws s3 cp "$HOME"/"$path"/"$filename" s3://"$destination_bucket"/
#
# # Remove the input directory
# rm -r "$HOME"/"$path"/
# ```

# %% [markdown]
# ### Splitting large JSONL files

# %% [markdown]
# ```
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ ll
# total 2466300
# drwxrwxrwx 1 eyamrog eyamrog        512 Jun 19 13:04 ./
# drwxrwxrwx 1 eyamrog eyamrog        512 Jun  8 17:01 ../
# <omitted>
# -rwxrwxrwx 1 eyamrog eyamrog 2523737751 Jun 19 13:04 mari2017_1.jsonl*
# <omitted>
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ sed -n '$=' mari2017_1.jsonl
# 568559
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ echo '568559/2' | bc
# 284279
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ split -l 284280 mari2017_1.jsonl
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ sed -n '$=' xaa
# 284280
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$ ll
# total 4930924
# <omitted>
# -rwxrwxrwx 1 eyamrog eyamrog 2523737751 Jun 19 13:04 mari2017_1.jsonl*
# <omitted>
# -rwxrwxrwx 1 eyamrog eyamrog 1281293904 Jun 19 13:32 xaa*
# -rwxrwxrwx 1 eyamrog eyamrog 1242443847 Jun 19 13:33 xab*
# eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads$
# ```

# %% [markdown]
# ### Listing Unicode characters

# %% [markdown]
# ```
# import re
# from collections import Counter
#
# def extract_unicode_characters(text):
#     # Define the RegEx pattern for matching Unicode characters
#     pattern = r'\\u[0-9A-Fa-f]{4}'
#     
#     # Find all matches in the text
#     matches = re.findall(pattern, text)
#     
#     # Count the occurrences of each UNICODE character
#     char_count = Counter(matches)
#     
#     return char_count
#
# # Extract Unicode characters and their counts
# unicode_counts = extract_unicode_characters(df_true_json_prettified)
#
# # Print the results
# for char, count in unicode_counts.items():
#     print(f'Character {char}: Count = {count}')
# ```

# %% [markdown]
# ### Replacing Unicode characters

# %% [markdown]
# ```
# df_fake_json_prettified_2 = df_fake_json_prettified.\
# replace('\\u000b', '').\
# replace('\\u0026', '&').\
# replace('\\u003d', '=').\
# replace('\\u00a0', '').\
# replace('\\u00a1', '¡').\
# replace('\\u00a3', '£').\
# replace('\\u00ad', '').\
# replace('\\u00af', '¯').\
# replace('\\u00b0', '°').\
# replace('\\u00b4', '´').\
# replace('\\u00bf', '¿').\
# replace('\\u00c9', 'É').\
# replace('\\u00e0', 'à').\
# replace('\\u00e1', 'á').\
# replace('\\u00e2', 'â').\
# replace('\\u00e7', 'ç').\
# replace('\\u00e9', 'é').\
# replace('\\u00ea', 'ê').\
# replace('\\u00eb', 'ë').\
# replace('\\u00ed', 'í').\
# replace('\\u00f1', 'ñ').\
# replace('\\u00f3', 'ó').\
# replace('\\u00f4', 'ô').\
# replace('\\u00f6', 'ö').\
# replace('\\u00fa', 'ú').\
# replace('\\u00fc', 'ü').\
# replace('\\u0101', 'ā').\
# replace('\\u0107', 'ć').\
# replace('\\u014d', 'ō').\
# replace('\\u017d', 'Ž').\
# replace('\\u017e', 'ž').\
# replace('\\u200a', ' ').\
# replace('\\u200b', ' ').\
# replace('\\u200B', ' ').\
# replace('\\u200e', '').\
# replace('\\u200f', '').\
# replace('\\u2013', '–').\
# replace('\\u2014', '—').\
# replace('\\u2018', "'").\
# replace('\\u2019', "'").\
# replace('\\u201c', '"').\
# replace('\\u201d', '"').\
# replace('\\u2022', '•').\
# replace('\\u2026', '…').\
# replace('\\u2028', '(LS)').\
# replace('\\u2029', '(PS)').\
# replace('\\u202a', '(LRE)').\
# replace('\\u202c', '').\
# replace('\\u2032', "'").\
# replace('\\u2033', "''").\
# replace('\\u20ac', '€').\
# replace('\\u2122', '(TM)').\
# replace('\\u2611', '☑').\
# replace('\\u27a1', '➡').\
# replace('\\u30c4', 'ツ').\
# replace('\\ufe0f', '◌️').\
# replace('\\ufeff', '').\
# replace('\\uffff', '')
# ```

# %% [markdown]
# ### List of Identified Unicode characters

# %% [markdown]
# [Unicode reference](https://www.compart.com/en/unicode)

# %% [markdown]
# ```
# \u000b = <Line Tabulation> (VT)
# \u0026 = Ampersand = &
# \u003d = Equals Sign = =
# \u00a0 = No-Break Space (NBSP)
# \u00a1 = Inverted Exclamation Mark = ¡
# \u00a3 = Pound Sign = £
# \u00ad = Soft Hyphen (SHY)
# \u00af = Macron = ¯
# \u00b0 = Degree Sign = °
# \u00b4 = Acute Accent = ´
# \u00bf = Inverted Question Mark = ¿
# \u00c9 = Latin Capital Letter E with Acute = É
# \u00e0 = Latin Small Letter A with Grave = à
# \u00e1 = Latin Small Letter A with Acute = á
# \u00e2 = Latin Small Letter A with Circumflex = â
# \u00e7 = Latin Small Letter C with Cedilla = ç
# \u00e9 = Latin Small Letter E with Acute = é
# \u00ea = Latin Small Letter E with Circumflex = ê
# \u00eb = Latin Small Letter E with Diaeresis = ë
# \u00ed = Latin Small Letter I with Acute = í
# \u00f1 = Latin Small Letter N with Tilde = ñ
# \u00f3 = Latin Small Letter O with Acute = ó
# \u00f4 = Latin Small Letter O with Circumflex = ô
# \u00f6 = Latin Small Letter O with Diaeresis = ö
# \u00fa = Latin Small Letter U with Acute = ú
# \u00fc = Latin Small Letter U with Diaeresis = ü
# \u0101 = Latin Small Letter A with Macron = ā
# \u0107 = Latin Small Letter C with Acute = ć
# \u014d = Latin Small Letter O with Macron = ō
# \u017d = Latin Capital Letter Z with Caron = Ž
# \u017e = Latin Small Letter Z with Caron = ž
# \u200a = Hair Space = ' '
# \u200b = Zero Width Space (ZWSP) = ' '
# \u200B = Zero Width Space (ZWSP) = ' '
# \u200e = Left-to-Right Mark (LRM)
# \u200f = Right-to-Left Mark (RLM)
# \u2013 = En Dash = –
# \u2014 = Em Dash = —
# \u2018 = Left Single Quotation Mark = '
# \u2019 = Right Single Quotation Mark = '
# \u201c = Left Double Quotation Mark = "
# \u201d = Right Double Quotation Mark = "
# \u2022 = Bullet = •
# \u2026 = Horizontal Ellipsis = …
# \u2028 = Line Separator = (LS)
# \u2029 = Paragraph Separator = (PS)
# \u202a = Left-to-Right Embedding (LRE)
# \u202c = Pop Directional Formatting (PDF)
# \u2032 = Prime = '
# \u2033 = Double Prime = ''
# \u20ac = Euro Sign = €
# \u2122 = Trade Mark Sign = (TM)
# \u2611 = Ballot Box with Check = ☑
# \u27a1 = Black Rightwards Arrow = ➡
# \u30c4 = Katakana Letter Tu = ツ
# \ufe0f = Variation Selector-16 (VS16) = ◌️
# \ufeff = Zero Width No-Break Space (BOM, ZWNBSP)
# \uffff = Undefined Character
# ```

# %% [markdown]
# ### Counting expressions in a certain dataframe column using RegEx

# %% [markdown]
# ```
# def extract_emoji_counts(df, text_column):
#     """
#     Extracts specifically formatted emoji counts from texts in a pandas DataFrame.
#
#     Args:
#         df (pd.DataFrame): DataFrame containing the texts.
#         text_column (str): Name of the column containing text to be processed.
#
#     Returns:
#         dict: A dictionary with emoji counts.
#     """
#     # Define the RegEx pattern for '{{Emoji:...}}'
#     emoji_pattern = r'EMOJI_.*?_e'
#
#     # Extract all matches from the specified text column
#     matches = df[text_column].str.findall(emoji_pattern)
#
#     # Flatten the list of matches
#     flat_matches = [match for sublist in matches for match in sublist]
#
#     # Count the occurrences of each emoji
#     emoji_counts = pd.Series(flat_matches).value_counts()
#
#     return emoji_counts
#
# # Get emoji counts
# emoji_counts_result = extract_emoji_counts(df_tweets_filtered, 'text')
#
# print('Emoji counts:')
# print(emoji_counts_result)
# ```

# %% [markdown]
# ### Removing selected invisible Unicode characters

# %% [markdown]
# ```
# import re
#
# def remove_invisible_unicode(text):
#     # Remove characters in the 'Format (Cf)' category (U+2066 and U+2069)
#     cleaned_text = re.sub(r'[\u2066\u2069]', '', text)
#     return cleaned_text
#
# # Example usage:
# text_unicode = "Sr presidente ⁦@jairbolsonaro⁩, está na hora de desenvolvermos armas nucleares."
# cleaned_text = remove_invisible_unicode(text_unicode)
# print(cleaned_text)
# ```

# %% [markdown]
# ### Tokenisation

# %% [markdown]
# ```
# import re
#
# # Defining a function to tokenise a string
# def tokenise_string(input_line):
#     # Replace URLs with placeholders
#     url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\b'
#     placeholder = '<URL>'  # Choose a unique placeholder
#     urls = re.findall(url_pattern, input_line)
#     tokenised_line = re.sub(url_pattern, placeholder, input_line)  # Replace URLs with placeholders
#     
#     # Replace curly quotes with straight ones
#     tokenised_line = tokenised_line.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
#     # Separate common punctuation marks with spaces
#     tokenised_line = re.sub(r'([.\!?,"\'/()])', r' \1 ', tokenised_line)
#     # Add a space before '#'
#     tokenised_line = re.sub(r'(?<!\s)#', r' #', tokenised_line)  # Add a space before '#' if it is not already preceded by one
#     # Reduce extra spaces by a single space
#     tokenised_line = re.sub(r'\s+', ' ', tokenised_line)
#     
#     # Replace the placeholders with the respective URLs
#     for url in urls:
#         tokenised_line = tokenised_line.replace(placeholder, url, 1)
#     
#     return tokenised_line
#
# line = 'Hello! “C3PO”,    are you   there?Go to http://google.com, or https://example.com and http://jaded.com.br  https://t.co/U5wtRuWxSm,    #case  and ‘find more’ about#comodore#bozo#daunting       !'
# tokenised_line = tokenise_string(line)
#
# print(tokenised_line)
# ```

# %%
