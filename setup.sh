#!/bin/bash
set -e

echo "###################################"
echo "#       AutoGlow Setup-Skript     #"
echo "###################################"
echo ""

# Prüfen, ob python3 verfügbar ist
if ! command -v python3 &> /dev/null
then
    echo "❌ FEHLER: Python 3 konnte nicht gefunden werden. Bitte installiere Python 3 und versuche es erneut."
    exit 1
fi

echo "--> Erstelle eine virtuelle Python-Umgebung im Ordner 'venv'..."
python3 -m venv venv

echo "--> Aktiviere die virtuelle Umgebung..."
source venv/bin/activate

echo "--> Installiere die benötigten Pakete (pyserial, websockets)..."
pip install -r requirements.txt

echo ""
echo "✅ Setup abgeschlossen!"
echo ""
echo "------------------------------------------------------------------"
echo "WICHTIG: Um das Skript zu starten, musst du ZUERST die"
echo "Umgebung mit folgendem Befehl aktivieren:"
echo ""
echo "   source venv/bin/activate"
echo ""
echo "Danach kannst du AutoGlow jederzeit starten mit:"
echo ""
echo "   python3 autodarts_wled_mini.py"
echo "------------------------------------------------------------------"