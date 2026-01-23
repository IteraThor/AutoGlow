
[Timeline_1.webm](https://github.com/user-attachments/assets/b55219f3-77fe-43d2-a55a-753f5056551b)

<p align="center">
  <a href="https://discord.gg/pZAjmwV5kE">
    <img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?logo=discord&logoColor=white&style=for-the-badge" alt="Join our Discord">
  </a>
</p>

<!-- Sprachumschalter für README -->
<details>
  <summary>🇩🇪 <strong>Deutsch</strong> (Klicken zum Ausklappen)</summary>
  
  <br>
  
  <h1>AutoGlow: Eine minimalistische Status-Ampel für Autodarts</h1>

  <p>AutoGlow ist ein einfaches, lokales Skript, das den Echtzeit-Status deines Autodarts-Boards als simple „Ampel“ auf einem WLED-Strip anzeigt.</p>

  <h3>Features:</h3>
  <ul>
    <li><b>Kein WLAN nötig:</b> Läuft über die direkte USB-Verbindung.</li>
    <li><b>Plug & Play:</b> Keine Authentifizierung, keine Tokens.</li>
  </ul>

  <hr>

  <h3>Die „Ampel“-Funktion</h3>
  <ul>
    <li>🟢 <b>Status `Throw` (Du kannst Werfen):</b> Grün</li>
    <li>🟡 <b>Status `Takeout` (Du kannst die Darts ziehen):</b> Gelb</li>
    <li>🔴 <b>Status `Takeout in Progress` (Darts werden gezogen):</b> Rot</li>
  </ul>

<hr>

<h3>Was dieses Skript <u>NICHT</u> kann:</h3>
<ul>
<li>Keine Auswertung von Spielevents oder Scores.</li>
<li>Es weiß nicht, was im Spiel passiert.</li>
<li>Es verarbeitet ausschließlich den Board-Status: <code>throw</code> oder <code>takeout</code>.</li>
</ul>

<hr>

  <h3>Hardware:</h3>
  <ul>
    <li>PC mit Autodarts</li>
    <li>ESP32-Board mit WLED-Firmware</li>
    <li>LEDs und ein USB-Kabel</li>
  </ul>

  <hr>

  <h3>Installation & Autostart (Ein Befehl)</h3>

  <pre><code># 1. Projekt herunterladen
  git clone https://github.com/IteraThor/AutoGlow.git

  # 2. In den Projektordner wechseln
  cd AutoGlow

  # 3. Setup-Skript mit Admin-Rechten ausführen
  sudo bash setup.sh
  </code></pre>
</details>

<hr>

<details open>
  <summary>🇬🇧 <strong>English</strong> (Click to expand)</summary>
  
  <br>
  
  <h1>AutoGlow: A Minimal Status Light for Autodarts</h1>

  <p>AutoGlow is a simple, local script that displays your Autodarts board’s real-time status as a basic “traffic light” on a WLED strip.</p>

  <h3>Features:</h3>
  <ul>
    <li><b>No Wi-Fi needed:</b> Works via direct USB connection.</li>
    <li><b>Plug & Play:</b> No authentication, no tokens required.</li>
  </ul>

  <hr>

  <h3>The “Traffic Light” Function</h3>
  <ul>
    <li>🟢 <b>Status `Throw` (You can throw):</b> Green</li>
    <li>🟡 <b>Status `Takeout` (You can pull darts):</b> Yellow</li>
    <li>🔴 <b>Status `Takeout in Progress` (Darts being removed):</b> Red</li>
  </ul>

<hr>

<h3>What this script <u>CANNOT</u> do:</h3>
<ul>
<li>It does not analyze gameplay events or scores.</li>
<li>It has no awareness of what happens in the game itself.</li>
<li>It only tracks and processes whether the board is in <code>throw</code> or <code>takeout</code> state.</li>
</ul>

<hr>

  <h3>Hardware:</h3>
  <ul>
    <li>PC with Autodarts</li>
    <li>ESP32 board running WLED firmware</li>
    <li>LEDs and a USB cable</li>
  </ul>

  <hr>

  <h3>Installation & Autostart (One Command)</h3>

  <pre><code># 1. Clone the project
  git clone https://github.com/IteraThor/AutoGlow.git

  # 2. Enter the project folder
  cd AutoGlow

  # 3. Run setup script with admin privileges
  sudo bash setup.sh
  </code></pre>
</details>












