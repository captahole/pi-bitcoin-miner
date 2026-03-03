#!/bin/bash
# Setup autostart for the miner dashboard

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create desktop entry
cat > ~/.config/autostart/bitcoin-miner.desktop << EOF
[Desktop Entry]
Type=Application
Name=Bitcoin Miner Dashboard
Exec=python3 ${SCRIPT_DIR}/miner_dashboard.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

chmod +x ~/.config/autostart/bitcoin-miner.desktop

echo "Autostart configured! The dashboard will launch on boot."
echo "To disable: rm ~/.config/autostart/bitcoin-miner.desktop"
