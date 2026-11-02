import asyncio
import websockets
import json
import serial
import serial.tools.list_ports
import time
import os
import logging
import urllib.request

STATE_URL = "http://localhost:3180/api/state"

# =============================================================================
# LOGGING & CONFIGURATION
# =============================================================================

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(PROJECT_DIR, "config.json")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AutoGlow")

DEFAULT_CONFIG = {
    "global_brightness": 255,
    "manual_port": "",
    "Throw": {"on": True, "bri": 255, "tt": 0, "seg": {"fx": 0, "col": [[0, 255, 0]]}, "enabled": True},
    "Takeout in progress": {"on": True, "bri": 255, "tt": 0, "seg": {"fx": 0, "col": [[255, 0, 0]]}, "enabled": True},
    "Takeout": {"on": True, "bri": 255, "tt": 0, "seg": {"fx": 0, "col": [[255, 255, 0]]}, "enabled": True},
    "Starting": {"on": True, "bri": 255, "tt": 0, "seg": {"fx": 0, "col": [[0, 0, 255]]}, "enabled": True},
    "Stopped": {"on": True, "bri": 255, "tt": 0, "seg": {"fx": 0, "col": [[255, 0, 255]]}, "enabled": True},
    "Calibrating": {"on": True, "bri": 255, "tt": 0, "seg": {"fx": 0, "col": [[128, 0, 128]]}, "enabled": True},
    "Error": {"on": True, "bri": 255, "tt": 0, "seg": {"fx": 1, "col": [[255, 0, 0]]}, "enabled": True}
}

def load_config():
    if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return DEFAULT_CONFIG

# =============================================================================
# CORE LOGIC
# =============================================================================

ser = None

def find_esp32_port():
    config = load_config()
    manual = config.get("manual_port")
    if manual and os.path.exists(manual):
        logger.info(f"Using manual port: {manual}")
        return manual

    KNOWN_VID_PIDS = [(0x10C4, 0xEA60), (0x1A86, 0x7523), (0x0403, 0x6001), (0x303A, 0x1001)]
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if (port.vid, port.pid) in KNOWN_VID_PIDS:
            return port.device
    return None

def send_wled_command(command_dict):
    global ser
    if ser and ser.is_open:
        try:
            # Clean command (remove internal flags)
            wled_msg = {k: v for k, v in command_dict.items() if k != "enabled"}
            ser.write((json.dumps(wled_msg) + '\n').encode())
        except Exception as e:
            logger.error(f"Serial write error: {e}")
            ser.close()

def _norm(name):
    return str(name).strip().lower().replace("_", " ").replace("-", " ")

def resolve_status_key(config, status):
    """Map a status from Autodarts (any casing, e.g. 'takeout in progress',
    'Takeout_In_Progress') to the matching config key ('Takeout in progress')."""
    if status in config:
        return status
    wanted = _norm(status)
    for key, val in config.items():
        if isinstance(val, dict) and _norm(key) == wanted:
            return key
    return None

def extract_status(data):
    """Pull the board status out of an Autodarts event, old or new format."""
    if not isinstance(data, dict):
        return None
    inner = data.get("data")
    if isinstance(inner, dict) and inner.get("status"):
        return inner["status"]
    if data.get("status"):
        return data["status"]
    return None

_last_status = None

async def handle_status_change(status):
    global _last_status
    config = load_config()
    key = resolve_status_key(config, status)
    status_config = config.get(key) if key else None
    global_bri = config.get("global_brightness", 255)

    if status_config and status_config.get("enabled", True):
        if key == _last_status:
            return
        _last_status = key
        logger.info(f"Status change: {key} (Bri: {global_bri})")
        command = status_config.copy()
        command.pop("enabled", None)
        command["bri"] = global_bri
        send_wled_command(command)
    else:
        logger.info(f"Status '{status}' is disabled or not in config.json.")

async def play_startup_animation():
    """Plays a short rainbow effect on startup for 3 seconds."""
    logger.info("Playing startup animation...")
    anim = {"on": True, "bri": 255, "seg": {"fx": 9, "sx": 128, "ix": 128}}
    send_wled_command(anim)
    await asyncio.sleep(3)
    await handle_status_change("Throw")

def _fetch_state():
    with urllib.request.urlopen(STATE_URL, timeout=2) as r:
        return json.loads(r.read().decode())

async def poll_state():
    """Fallback: newer Autodarts versions don't always push status changes
    over the websocket, so poll the REST state as well."""
    loop = asyncio.get_running_loop()
    while True:
        try:
            state = await loop.run_in_executor(None, _fetch_state)
            status = extract_status(state)
            if status:
                await handle_status_change(status)
        except Exception as e:
            logger.debug(f"State poll failed: {e}")
        await asyncio.sleep(1)

async def autodarts_logger():
    uri = "ws://localhost:3180/api/events"
    asyncio.create_task(poll_state())
    global ser
    esp_port = find_esp32_port()
    
    if esp_port:
        try:
            ser = serial.Serial(esp_port, 115200, timeout=1)
            await asyncio.sleep(2) # Non-blocking settle time
            logger.info(f"Serial connection established on {esp_port}.")
            asyncio.create_task(play_startup_animation())
        except Exception as e:
            logger.error(f"Failed to open serial port {esp_port}: {e}")

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                logger.info(f"Connected to Autodarts at {uri}")
                while True:
                    message = await websocket.recv()
                    try:
                        data = json.loads(message)
                    except ValueError:
                        logger.debug(f"Non-JSON message: {message[:200]}")
                        continue
                    status = extract_status(data)
                    if status:
                        await handle_status_change(status)
                    else:
                        logger.debug(f"Ignored event: {message[:300]}")
        except Exception as e:
            logger.warning(f"WebSocket connection failed: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(autodarts_logger())
    except KeyboardInterrupt:
        if ser and ser.is_open:
            ser.close()
        logger.info("Script terminated by user.")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
