# Download the Anaconda installer for Linux directly using 'wget' (make sure to check for the latest version on the Anaconda website):
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh

# Run the installer
bash Anaconda3-2024.10-1-Linux-x86_64.sh

Allow the installation script to configure automatic Conda initialisation.

# Create 'mr_r_env', a specific Conda environment for 'R'
conda create --name my_r_env r-base r-essentials

conda env list

conda activate my_r_env

conda list

# Install the 'IRkernel' - After activating the environment, open an 'R' session by typing 'R' in the terminal. In the 'R' session, run (if you update or modify your 'R' environment and need to ensure that the 'IRkernel' reflects the changes, you can simply rerun the commands):

install.packages("IRkernel")
IRkernel::installspec(name = 'my_r_env', user = TRUE) # Registers the kernel for Jupyter for the current user

# Check the Jupyter kernels
jupyter kernelspec list
