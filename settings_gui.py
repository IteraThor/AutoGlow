import tkinter as tk
from tkinter import colorchooser, messagebox, ttk
import json
import os
import serial
import serial.tools.list_ports
import time

# --- FIX: Pfad relativ zum Skript-Verzeichnis setzen ---
# Das verhindert Fehler, wenn das Skript von woanders (z.B. SUIT) aufgerufen wird.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

WLED_EFFECTS = {
    "Solid": 0, "Blink": 1, "Breathe": 2, "Wipe": 3, "Scan": 45,
    "Rainbow": 9, "Chase": 28, "Fire": 66, "Strobe": 8,
    "Color Loop": 11, "Heartbeat": 101, "Pacifica": 104
}

EFFECT_ID_TO_NAME = {v: k for k, v in WLED_EFFECTS.items()}

def load_config():
    # Wir nutzen jetzt den absoluten Pfad CONFIG_FILE
    if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def find_esp32_port():
    KNOWN_VID_PIDS = [(0x10C4, 0xEA60), (0x1A86, 0x7523), (0x0403, 0x6001), (0x303A, 0x1001)]
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if (port.vid, port.pid) in KNOWN_VID_PIDS:
            return port.device
    return None

class AutoGlowGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoGlow Settings")
        self.root.configure(bg="#121212")
        self.config = load_config()
        self.check_vars = {}
        self.fx_dropdowns = {}
        self.color_btns = {}

        tk.Label(root, text="AutoGlow Config & Brightness", fg="white", bg="#121212", font=("Arial", 14, "bold")).pack(pady=10)

        # --- Global Brightness Slider ---
        bright_frame = tk.Frame(root, bg="#1e1e1e", pady=10)
        bright_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(bright_frame, text="Global Brightness:", fg="white", bg="#1e1e1e").pack(side="left", padx=10)
        
        current_bright = self.config.get("global_brightness", 255)
        self.bright_slider = tk.Scale(bright_frame, from_=0, to=255, orient="horizontal", bg="#1e1e1e", fg="white", highlightthickness=0)
        self.bright_slider.set(current_bright)
        self.bright_slider.pack(side="right", fill="x", expand=True, padx=10)

        self.list_frame = tk.Frame(root, bg="#121212")
        self.list_frame.pack(fill="both", expand=True, padx=20)

        for status, settings in self.config.items():
            if status == "global_brightness": continue
            
            row = tk.Frame(self.list_frame, bg="#1e1e1e", pady=5)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=status, fg="white", bg="#1e1e1e", width=15, anchor="w").pack(side="left", padx=10)

            var = tk.BooleanVar(value=settings.get("enabled", True))
            self.check_vars[status] = var
            tk.Checkbutton(row, variable=var, bg="#1e1e1e", activebackground="#1e1e1e", selectcolor="#333333").pack(side="right", padx=5)

            tk.Button(row, text="⚡", bg="#444444", fg="white", width=3, command=lambda s=status: self.test_effect(s)).pack(side="right", padx=5)

            # Farbe sicher abrufen (Fallback auf Weiß)
            col_data = settings.get("seg", {}).get("col", [[255, 255, 255]])
            if not col_data or not isinstance(col_data, list):
                col = [255, 255, 255]
            else:
                col = col_data[0]

            hex_color = f'#{col[0]:02x}{col[1]:02x}{col[2]:02x}'
            btn = tk.Button(row, bg=hex_color, width=3)
            btn.config(command=lambda s=status, b=btn: self.pick_color(s, b))
            btn.pack(side="right", padx=5)
            self.color_btns[status] = btn

            fx_id = settings.get("seg", {}).get("fx", 0)
            fx_var = tk.StringVar(value=EFFECT_ID_TO_NAME.get(fx_id, "Solid"))
            self.fx_dropdowns[status] = fx_var
            ttk.Combobox(row, textvariable=fx_var, values=list(WLED_EFFECTS.keys()), width=10, state="readonly").pack(side="right", padx=5)

        tk.Button(root, text="Save All Settings", bg="#007bff", fg="white", command=self.save, font=("Arial", 11, "bold")).pack(pady=20, fill="x", padx=20)

    def test_effect(self, status):
        port = find_esp32_port()
        if not port: return
        fx_name = self.fx_dropdowns[status].get()
        fx_id = WLED_EFFECTS.get(fx_name, 0)
        hex_col = self.color_btns[status].cget("bg").lstrip('#')
        rgb = [int(hex_col[i:i+2], 16) for i in (0, 2, 4)]
        
        brightness = self.bright_slider.get()
        command = {"on": True, "bri": brightness, "seg": {"fx": fx_id, "col": [rgb]}}
        
        try:
            with serial.Serial(port, 115200, timeout=1) as ser:
                time.sleep(1.5)
                ser.write((json.dumps(command) + '\n').encode())
        except: pass

    def pick_color(self, status, btn):
        color_res = colorchooser.askcolor(initialcolor=btn.cget("bg"))
        if color_res and color_res[1]: # Sicherstellen, dass eine Farbe gewählt wurde
            btn.config(bg=color_res[1])

    def save(self):
        new_config = {"global_brightness": self.bright_slider.get()}
        for status, var in self.check_vars.items():
            fx_name = self.fx_dropdowns[status].get()
            hex_col = self.color_btns[status].cget("bg").lstrip('#')
            rgb = [int(hex_col[i:i+2], 16) for i in (0, 2, 4)]
            new_config[status] = {
                "on": True, "bri": 255, "tt": 0, "enabled": var.get(),
                "seg": {"fx": WLED_EFFECTS.get(fx_name, 0), "col": [rgb]}
            }
        # Auch hier nutzen wir den absoluten Pfad
        with open(CONFIG_FILE, "w") as f:
            json.dump(new_config, f, indent=4)
        messagebox.showinfo("Success", "Settings saved!")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("550x600")
    style = ttk.Style(); style.theme_use('clam')
    app = AutoGlowGUI(root)
    root.mainloop()
