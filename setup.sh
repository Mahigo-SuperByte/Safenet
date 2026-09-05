#!/usr/bin/env bash
# Automated setup script for Linux

echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-tk network-manager wireless-tools

echo "Setting permissions..."
chmod +x main.py

echo "Setup completed successfully! Run the app using: python3 main.py"
