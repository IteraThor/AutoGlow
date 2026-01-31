#!/bin/bash
set -e

echo "#############################################"
echo "#       AutoGlow Setup & Autostart          #"
echo "#############################################"
echo ""

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "❌ ERROR: Please run this script with sudo:"
  echo "   sudo bash setup.sh"
  exit 1
fi

echo "--> Checking system requirements..."

# Check if python3 and git are available
if ! command -v python3 &> /dev/null || ! command -v git &> /dev/null; then
    echo "--> Installing required packages (git, python3-venv)..."
    apt update && apt install -y git python3-venv
fi

# Determine the original user
if [ -n "$SUDO_USER" ]; then
    ORIGINAL_USER=$SUDO_USER
else
    echo "❌ ERROR: Could not determine the original user."
    exit 1
fi

# Assign USB permissions (dialout group)
echo "--> Granting USB permissions to user $ORIGINAL_USER..."
usermod -a -G dialout "$ORIGINAL_USER"

# Dynamically determine the project path
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if [ ! -f "$PROJECT_DIR/autodarts_wled_mini.py" ]; then
    echo "❌ ERROR: autodarts_wled_mini.py not found in $PROJECT_DIR."
    exit 1
fi

echo "--> Creating a virtual Python environment..."
sudo -u "$ORIGINAL_USER" python3 -m venv "$PROJECT_DIR/venv"

echo "--> Installing Python packages..."
sudo -u "$ORIGINAL_USER" "$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

echo "--> Creating systemd service file..."

# Write configuration with -u flag for unbuffered logs
cat > /etc/systemd/system/autoglow.service << EOL
[Unit]
Description=AutoGlow Service for Autodarts WLED Sync
After=network.target

[Service]
User=$ORIGINAL_USER
Group=$ORIGINAL_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python3 -u $PROJECT_DIR/autodarts_wled_mini.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

echo "--> Activating and starting AutoGlow service..."
systemctl daemon-reload
systemctl enable autoglow.service
systemctl start autoglow.service

echo ""
echo "✅ Setup successfully completed!"
echo "The service is now using the path: $PROJECT_DIR"
echo "NOTE: If USB access fails, please log out and back in or run 'newgrp dialout'."
