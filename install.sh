#!/bin/bash

# Function to install pip
install_pip() {
    echo "Installing pip..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y curl python3.13 ollama python3.13-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3.13 curl ollama python3.13-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3.13 curl ollama python3.13-pip
    elif command -v yay &> /dev/null; then
          yay -S python python-pip curl ollama --noconfirm
    elif command -v pacman &> /dev/null; then
        sudo pacman -Syu curl python python-pip ollama --noconfirm
    else
        echo "Package manager not supported. Please install pip manually."
        exit 1
    fi
}

# Detect Linux distribution and install dependencies
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "Detected Linux distribution: $NAME"
    install_pip
    # Find the number of CPU threads
    CPU_THREADS=$(nproc)
    echo "Detected CPU threads: $CPU_THREADS"
    # Replace the hardcoded value in the Makefile
    sed -i "s/zx/$CPU_THREADS/g" modelfile
    ollama create jeff-ai -f ./modelfile
else
    echo "Cannot detect Linux distribution. Please install pip and ollama manually."
    exit 1
fi
echo "Installation completed."