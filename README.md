[Timeline_1.webm](https://github.com/user-attachments/assets/b55219f3-77fe-43d2-a55a-753f5056551b)

<p align="center">
  <a href="https://discord.gg/pZAjmwV5kE">
    <img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?logo=discord&logoColor=white&style=for-the-badge" alt="Join our Discord">
  </a>
</p>

<details open>
  <summary>🇬🇧 <strong>English</strong> (Click to expand)</summary>
  
  <br>
  
  <h1>AutoGlow: Status Light for Autodarts (USB & GUI Edition)</h1>

  <p>AutoGlow is a simple, local script that displays your Autodarts board’s real-time status via direct USB connection on a WLED strip.</p>

  <h3>Features:</h3>
  <ul>
    <li><b>Graphical Interface (GUI):</b> Easily adjust colors, effects, and brightness.</li>
    <li><b>Global Brightness:</b> Dim all LEDs simultaneously using a slider.</li>
    <li><b>No Wi-Fi needed:</b> Works via direct USB connection.</li>
    <li><b>Plug & Play:</b> No authentication, no tokens required.</li>
  </ul>

  <hr>

  <h3>The “Traffic Light” Function</h3>
  <ul>
    <li>🟢 <b>Status `Throw`:</b> Green</li>
    <li>🟡 <b>Status `Takeout`:</b> Yellow</li>
    <li>🔴 <b>Status `Takeout in Progress`:</b> Red</li>
    <li>🔵 <b>Status `Starting` / `Calibrating`:</b> Blue / Purple</li>
    <li>💗 <b>Status `Stopped`:</b> Pink</li>
  </ul>

<hr>

<h3>Changing Settings (GUI)</h3>
<p>Use the graphical interface to customize your setup. <b>Important:</b> The background service must be stopped to free up the USB port for testing.</p>

<pre><code>
# 1. Stop the service temporarily
sudo systemctl stop autoglow.service

# 2. Start the settings GUI
sudo python3 settings_gui.py

# 3. Restart the service after saving
sudo systemctl start autoglow.service
</code></pre>

<hr>

  <h3>Installation & Autostart</h3>

  <pre><code>
  # 1. Clone the project
  git clone https://github.com/IteraThor/AutoGlow.git
  # 2. Enter the project folder
  cd AutoGlow
  # 3. Run setup script
  sudo bash setup.sh
  </code></pre>
</details>

<hr>

<details>
  <summary>🇩🇪 <strong>Deutsch</strong> (Klicken zum Ausklappen)</summary>
  
  <br>
  
  <h1>AutoGlow: Status-Ampel für Autodarts (USB & GUI Edition)</h1>

  <p>AutoGlow ist ein einfaches, lokales Skript, das den Echtzeit-Status deines Autodarts-Boards über eine direkte USB-Verbindung auf einem WLED-Strip anzeigt.</p>

  <h3>Features:</h3>
  <ul>
    <li><b>Grafische Oberfläche (GUI):</b> Farben, Effekte und Helligkeit bequem per Maus anpassen.</li>
    <li><b>Globale Helligkeit:</b> Alle LEDs gleichzeitig über einen Schieberegler dimmen.</li>
    <li><b>Kein WLAN nötig:</b> Läuft über die direkte USB-Verbindung.</li>
    <li><b>Plug & Play:</b> Keine Authentifizierung, keine Tokens.</li>
  </ul>

  <hr>

  <h3>Die „Ampel“-Funktion</h3>
  <ul>
    <li>🟢 <b>Status `Throw`:</b> Grün</li>
    <li>🟡 <b>Status `Takeout`:</b> Gelb</li>
    <li>🔴 <b>Status `Takeout in Progress`:</b> Rot</li>
    <li>🔵 <b>Status `Starting` / `Calibrating`:</b> Blau / Lila</li>
    <li>💗 <b>Status `Stopped`:</b> Pink</li>
  </ul>

<hr>

<h3>Einstellungen ändern (GUI)</h3>
<p>Um Farben oder Effekte anzupassen, nutze die grafische Oberfläche. <b>Wichtig:</b> Der Hintergrund-Dienst muss gestoppt sein, damit der USB-Port für Tests frei ist.</p>

<pre><code>
# 1. Dienst kurz stoppen
sudo systemctl stop autoglow.service

# 2. Einstellungen starten
sudo python3 settings_gui.py

# 3. Nach dem Speichern Dienst wieder starten
sudo systemctl start autoglow.service
</code></pre>

<hr>

  <h3>Installation & Autostart</h3>

  <pre><code>
  # 1. Projekt herunterladen
  git clone https://github.com/IteraThor/AutoGlow.git
  # 2. In den Projektordner wechseln
  cd AutoGlow
  # 3. Setup-Skript ausführen
  sudo bash setup.sh
  </code></pre>
</details>

