# AutoGlow: Eine minimalistische Status-Ampel für Autodarts

AutoGlow ist ein einfaches, lokales Skript, das den Echtzeit-Status deines Autodarts-Boards als simple "Ampel" auf einem WLED-Strip anzeigt.

**Features:**
-   **Kein WLAN nötig:** Läuft über die direkte USB-Verbindung.
-   **Plug & Play:** Keine Authentifizierung, keine Tokens.

---

### Die "Ampel"-Funktion

-   🟢 **Status `Throw` (Du kannst Werfen):** **Grün**
-   🟡 **Status `Takeout` (Du kannst die Darts ziehen):** **Gelb**
-   🔴 **Status `Takeout in Progress` (Darts werden gezogen):** **Rot**

---


**Hardware:**
-   PC (Linux) mit Autodarts
-   ESP32-Board mit WLED-Firmware
-   LEDs und ein USB-Kabel

---

### Installation & Nutzung

**1. Download & Installation**

Öffnen Sie ein Terminal und führen Sie diese drei Befehle aus:


```bash
# 1. Git herunterladen falls noch nicht gemacht:
sudo apt install git -y
# 1. Projekt herunterladen
git clone https://github.com/IteraThor/AutoGlow.git

# 2. In den Projektordner wechseln
cd AutoGlow

# 3. Benötigte Bibliotheken installieren
pip install -r requirements.txt

