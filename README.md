<!-- Sprachumschalter für README -->
<div align="center">
  <button id="lang-de" style="padding:6px 12px; margin-right:5px; background:#0078ff; color:white; border:none; border-radius:5px; cursor:pointer;">🇩🇪 Deutsch</button>
  <button id="lang-en" style="padding:6px 12px; background:#eee; border:none; border-radius:5px; cursor:pointer;">🇬🇧 English</button>
</div>

<br>

<div id="de">
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

<h3>Hardware:</h3>
<ul>
<li>PC (Linux) mit Autodarts</li>
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
</div>

<div id="en" style="display:none;">
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

<h3>Hardware:</h3>
<ul>
<li>PC (Linux) with Autodarts</li>
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
</div>

<script>
const deBtn = document.getElementById("lang-de");
const enBtn = document.getElementById("lang-en");
const de = document.getElementById("de");
const en = document.getElementById("en");

deBtn.onclick = () => {
  de.style.display = "block";
  en.style.display = "none";
  deBtn.style.background = "#0078ff";
  deBtn.style.color = "white";
  enBtn.style.background = "#eee";
  enBtn.style.color = "black";
};

enBtn.onclick = () => {
  de.style.display = "none";
  en.style.display = "block";
  enBtn.style.background = "#0078ff";
  enBtn.style.color = "white";
  deBtn.style.background = "#eee";
  deBtn.style.color = "black";
};
</script>
