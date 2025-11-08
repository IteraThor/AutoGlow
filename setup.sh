#!/bin/bash
set -e

echo "#############################################"
echo "#       AutoGlow Setup & Autostart          #"
echo "#############################################"
echo ""

# Prüfen, ob das Skript mit sudo ausgeführt wird
if [ "$EUID" -ne 0 ]; then
  echo "❌ FEHLER: Bitte führe dieses Skript mit sudo aus:"
  echo "   sudo bash setup.sh"
  exit 1
fi

echo "--> Prüfe Systemvoraussetzungen..."

# Prüfen, ob python3 und git verfügbar sind
if ! command -v python3 &> /dev/null || ! command -v git &> /dev/null; then
    echo "--> Installiere benötigte Pakete (git, python3-venv)..."
    apt update && apt install -y git python3-venv
fi

# Ermittle den ursprünglichen Benutzer, der sudo aufgerufen hat
if [ -n "$SUDO_USER" ]; then
    ORIGINAL_USER=$SUDO_USER
else
    echo "❌ FEHLER: Konnte den ursprünglichen Benutzer nicht ermitteln. Bitte mit 'sudo' ausführen."
    exit 1
fi

# Ermittle den absoluten Pfad zum Projektordner
# WICHTIG: Funktioniert nur, wenn das Skript aus dem Projektordner heraus ausgeführt wird.
PROJECT_DIR=$(pwd)
if [ ! -f "$PROJECT_DIR/autodarts_wled_mini.py" ]; then
    echo "❌ FEHLER: Bitte führe das Skript aus dem AutoGlow-Projektordner heraus aus."
    exit 1
fi

echo "--> Erstelle eine virtuelle Python-Umgebung..."
# Als der ursprüngliche Benutzer ausführen, um Berechtigungsprobleme zu vermeiden
sudo -u "$ORIGINAL_USER" python3 -m venv "$PROJECT_DIR/venv"

echo "--> Installiere Python-Pakete in die virtuelle Umgebung..."
sudo -u "$ORIGINAL_USER" "$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

echo "--> Erstelle systemd Service-Datei für den Autostart..."

# Schreibe die Konfiguration für den systemd-Dienst
cat > /etc/systemd/system/autoglow.service << EOL
[Unit]
Description=AutoGlow Service for Autodarts WLED Sync
After=network.target

[Service]
User=$ORIGINAL_USER
Group=$ORIGINAL_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python3 $PROJECT_DIR/autodarts_wled_mini.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

echo "--> Aktiviere und starte den AutoGlow-Dienst..."
systemctl daemon-reload
systemctl enable autoglow.service
systemctl start autoglow.service

echo ""
echo "✅ Setup und Autostart erfolgreich eingerichtet!"
echo ""
echo "------------------------------------------------------------------"
echo "AutoGlow läuft jetzt im Hintergrund und startet bei jedem"
echo "Systemstart automatisch."
echo ""
echo "Nützliche Befehle:"
echo "  - Status überprüfen:   sudo systemctl status autoglow.service"
echo "  - Live-Logs ansehen:    journalctl -u autoglow.service -f"
echo "  - Dienst neu starten:   sudo systemctl restart autoglow.service"
echo "  - Dienst stoppen:       sudo systemctl stop autoglow.service"
echo "------------------------------------------------------------------"