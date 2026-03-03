#!/bin/bash
# Installation script for Raspberry Pi Bitcoin Miner

echo "Installing Bitcoin Miner Dashboard for Raspberry Pi 5..."

# Update system
sudo apt-get update

# Install Python dependencies
sudo apt-get install -y python3-pip python3-pyqt5

# Install Python packages
pip3 install -r requirements.txt

# Install cpuminer-multi (actual mining software)
echo "Installing cpuminer-multi..."
sudo apt-get install -y automake autoconf pkg-config libcurl4-openssl-dev libjansson-dev libssl-dev libgmp-dev make g++ git

cd /tmp
git clone https://github.com/tpruvot/cpuminer-multi
cd cpuminer-multi
./build.sh
sudo cp cpuminer /usr/local/bin/
cd ~

echo "Installation complete!"
echo "Configure your mining pool in miner_dashboard.py before starting."
