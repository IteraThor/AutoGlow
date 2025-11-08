<p align="center">
  <img src="https://raw.githubusercontent.com/IteraThor/AutoGlow/main/autglow_logo.png" alt="AutoGlow Logo" width="150">
</p>
<h1 align="center">AutoGlow</h1>
<p align="center">
  Eine minimalistische Status-Ampel für Autodarts (Linux).
  <br>
  A minimalist status light for Autodarts (Linux).
</p>

---

<details>
<summary><strong>🇬🇧 English Version</strong> (Click to expand)</summary>

### AutoGlow: A Minimalist Status Light for Autodarts (Linux)

AutoGlow is a simple script for Linux that displays the real-time status of your Autodarts board as a simple "traffic light" on a WLED strip.

#### What problem does it solve?

It solves the common issue where the board gets stuck in "Takeout" mode, and subsequent throws are not counted. With AutoGlow, you can see at a glance whether it's your turn to throw.

**Advantages:**
-   **No Wi-Fi needed:** Runs quickly and reliably over a direct USB connection.
-   **Plug & Play:** No authentication, no tokens. It just works.
-   **Low Power Consumption:** Perfect for small LED setups powered directly from the PC's USB port without an external power supply.

---

### The "Traffic Light" Function

-   🟢 **Status `Throw` (Your turn):** **Green**
-   🟡 **Status `Takeout` (Turn finished):** **Yellow**
-   🔴 **Status `Takeout in Progress` (Removing darts):** **Red**

---

### Prerequisites

**Hardware:**
-   A PC running a Debian/Ubuntu-based Linux distribution
-   An ESP32 board with WLED firmware & a USB cable
-   LEDs

**Software:**
-   A running Autodarts instance
-   In WLED: Set **Settings > Sync Interfaces > "JSON"** as "Serial output mode".

---

### Installation & Autostart (One Command)

Open a terminal, copy the following three commands, and execute them one by one. The script handles the complete setup, including automatically starting on system boot.

```bash
# 1. Clone the project
git clone https://github.com/IteraThor/AutoGlow.git

# 2. Change into the project directory
cd AutoGlow

# 3. Run the setup script with admin rights
sudo bash setup.sh





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

### Installation & Autostart (Ein Befehl)

Öffne ein Terminal, kopiere die folgenden drei Befehle und führe sie nacheinander aus. Das Skript richtet alles ein, inklusive des automatischen Starts beim System-Boot.

```bash
# 1. Projekt herunterladen
git clone https://github.com/IteraThor/AutoGlow.git

# 2. In den Projektordner wechseln
cd AutoGlow

# 3. Setup-Skript mit Admin-Rechten ausführen
sudo bash setup.sh
