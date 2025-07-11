#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Source conda.sh
# source /etc/profile.d/conda.sh

# Environment name
ENV_NAME="vaParts"

# Check if the environment exists
if conda env list | grep -q "^$ENV_NAME "; then
    echo "Environment $ENV_NAME exists. Removing it..."
    conda deactivate
    conda env remove -n $ENV_NAME -y
fi

# Create the PyCharm environment with Python 3.12
echo "Creating new $ENV_NAME environment with Python 3.12..."
conda create -n $ENV_NAME python=3.12 -y

# Activate the environment
conda activate $ENV_NAME

# Install required packages for future updates
echo "Installing packages..."
# conda install numpy pandas pyspark scikit-learn

echo "$ENV_NAME environment setup complete."