import asyncio
import websockets
import json
import serial
import serial.tools.list_ports
import time

# =============================================================================
# BENUTZERKONFIGURATION: WLED-VERHALTEN
# =============================================================================
# Passen Sie hier das Verhalten der LEDs für jeden Autodarts-Status an.
# - Ein Status mit 'None' löst keine Aktion aus.
# - Farben werden im Format [R, G, B] angegeben (0-255).
# - "fx": 0  = Statische Farbe (Solid)
# - "tt": 0  = Sofortiger Übergang ohne Animation
# - "bri": 255 = Maximale Helligkeit
# 
# Dokumentation der WLED JSON API für mehr Optionen:
# https://kno.wled.ge/interfaces/json-api/
# =============================================================================

WLED_STATUS_CONFIG = {
    # Status: Spieler ist am Zug, bereit zu werfen
    "Throw": {
        "on": True, "bri": 255, "tt": 0,
        "seg": {"fx": 0, "col": [[0, 255, 0]]}  # Grün
    },
    
    # Status: Darts werden aus dem Board gezogen
    "Takeout in progress": {
        "on": True, "bri": 255, "tt": 0,
        "seg": {"fx": 0, "col": [[255, 255, 0]]}  # Gelb
    },

    # Status: Zug beendet, Darts wurden entfernt
    "Takeout": {
        "on": True, "bri": 255, "tt": 0,
        "seg": {"fx": 0, "col": [[255, 0, 0]]}  # Rot
    },

    # Status: System wird gestartet
    "Starting": None, # Aktuell keine Aktion definiert

    # Status: System wird gestoppt
    "Stopping": None, # Aktuell keine Aktion definiert

    # Status: System ist gestoppt / im Leerlauf
    "Stopped": {
        "on": False, "tt": 0 # LEDs ausschalten
    }
}

# =============================================================================
# KERNLOGIK (ab hier normalerweise keine Änderungen nötig)
# =============================================================================

# Globale Variable für die serielle Verbindung
ser = None

def find_esp32_port():
    """Sucht nach einem angeschlossenen ESP32 und gibt den Port zurück."""
    print("Suche nach einem angeschlossenen ESP32...")
    KNOWN_ESP32_VID_PIDS = [
        (0x10C4, 0xEA60), (0x1A86, 0x7523), (0x0403, 0x6001), (0x303A, 0x1001)
    ]
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid is not None and port.pid is not None:
            print(f"  - Prüfe Port: {port.device} (Hersteller: {port.manufacturer}, VID:PID={port.vid:04X}:{port.pid:04X})")
            if (port.vid, port.pid) in KNOWN_ESP32_VID_PIDS:
                print(f"✅ ESP32 gefunden auf Port: {port.device}")
                return port.device
        else:
            print(f"  - Ignoriere Port ohne VID/PID: {port.device}")
    print("❌ Kein bekannter ESP32 an einem seriellen Port gefunden.")
    return None

def send_wled_command(command_dict):
    """Konvertiert ein Python-Dict in JSON und sendet es an WLED via Serial."""
    if ser and ser.is_open:
        try:
            json_command = json.dumps(command_dict)
            print(f"--> Sende an WLED: {json_command}")
            ser.write((json_command + '\n').encode())
        except serial.SerialException as e:
            print(f"--> FEHLER: Konnte nicht an WLED senden. {e}")
            ser.close()

# -----------------------------------------------------------------------------
# Die Handler-Funktionen lesen jetzt nur noch die Konfiguration aus
# -----------------------------------------------------------------------------

async def handle_status_change(status):
    """Generischer Handler, der die Konfiguration für einen Status nachschlägt und ausführt."""
    print(f"--> [BLOCK] Logik für '{status}' wird ausgeführt.")
    command = WLED_STATUS_CONFIG.get(status)
    if command:
        send_wled_command(command)

status_handlers = {
    "Starting": lambda: handle_status_change("Starting"),
    "Stopped": lambda: handle_status_change("Stopped"),
    "Stopping": lambda: handle_status_change("Stopping"),
    "Throw": lambda: handle_status_change("Throw"),
    "Takeout in progress": lambda: handle_status_change("Takeout in progress"),
    "Takeout": lambda: handle_status_change("Takeout"),
}

# -----------------------------------------------------------------------------
# HAUPTFUNKTION FÜR WEBSOCKET-VERBINDUNG
# -----------------------------------------------------------------------------

async def autodarts_logger():
    """
    Stellt eine Verbindung zum Autodarts-WebSocket her, gibt Status-Updates aus
    und ruft den entsprechenden Handler-Block auf.
    """
    uri = "ws://localhost:3180/api/events"
    global ser

    esp_port = find_esp32_port()
    if esp_port:
        try:
            ser = serial.Serial(esp_port, 115200, timeout=1)
            time.sleep(2)
            print(f"--> Serielle Verbindung zu WLED auf {esp_port} erfolgreich.")
            send_wled_command({"on": False, "tt": 0})
        except serial.SerialException as e:
            print(f"--> FEHLER: Konnte Port {esp_port} nicht öffnen: {e}")
            ser = None

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print(f"\nVerbindung zu {uri} hergestellt. Warte auf Events...")
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        if data.get("type") == "state" and "status" in data.get("data", {}):
                            status = data["data"]["status"]
                            print(f"Status empfangen: {status}")

                            if status in status_handlers:
                                await status_handlers[status]()
                            else:
                                print(f"WARNUNG: Kein Handler für Status '{status}' definiert.")

                    except websockets.exceptions.ConnectionClosed:
                        print("Verbindung geschlossen. Versuche erneut zu verbinden...")
                        break
                    except json.JSONDecodeError:
                        pass
                    except Exception as e:
                        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

        except (OSError, websockets.exceptions.ConnectionClosedError) as e:
            print(f"Verbindung fehlgeschlagen: {e}. Nächster Versuch in 5 Sekunden...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Ein kritischer Fehler ist aufgetreten: {e}. Nächster Versuch in 5 Sekunden...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(autodarts_logger())
    except KeyboardInterrupt:
        print("\nSkript durch Benutzer beendet.")
        if ser and ser.is_open:
            send_wled_command({"on": False, "tt": 0})
            ser.close()

            print("--> Serielle Verbindung geschlossen.")
