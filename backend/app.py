
import threading
import time
import logging
import sys
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pynput import mouse, keyboard

# --- macOS Stealth Mode (only for standalone backend, not packaged app) ---
# When running as packaged app, pywebview handles AppKit
if not getattr(sys, 'frozen', False) and 'webview' not in sys.modules:
    try:
        import AppKit
        ns_app = AppKit.NSApplication.sharedApplication()
        ns_app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyProhibited)
    except:
        pass

# Setup logging (reduced for production)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Determine app directory
if os.environ.get('APP_RESOURCE_DIR'):
    APP_DIR = os.environ['APP_RESOURCE_DIR']
elif getattr(sys, 'frozen', False):
    # Fallback for frozen: Contents/MacOS -> Contents -> Contents/Resources
    exe_dir = os.path.dirname(sys.executable)
    APP_DIR = os.path.join(os.path.dirname(exe_dir), 'Resources')
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_DIR = os.path.join(APP_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

# Serve the main HTML page
@app.route('/static/index.html')
def serve_index():
    return send_from_directory(STATIC_DIR, 'index.html')

mouse_ctrl = mouse.Controller()
keyboard_ctrl = keyboard.Controller()
clicking = False
click_thread = None
hotkey_listener = None

# Global state for window tracking
current_app_name = "Unknown"
workspace = None

def window_tracker():
    """Separate thread to track the active window every 0.3s."""
    global current_app_name, workspace
    
    # Lazy import AppKit safely
    if workspace is None:
        try:
            from AppKit import NSWorkspace
            workspace = NSWorkspace.sharedWorkspace()
        except ImportError:
            logging.warning("AppKit not found, window tracking disabled")
            return
        except Exception as e:
            logging.error(f"Failed to initialize NSWorkspace: {e}")
            return

    while True:
        try:
            if workspace:
                # activeApplication() returns dict with NSApplicationName key
                active = workspace.activeApplication()
                if active:
                    current_app_name = active.get('NSApplicationName', 'Unknown')
        except Exception as e:
            logging.error(f"Window tracker error: {e}")
            # Prevent log spam if it fails continuously
            time.sleep(1)
        time.sleep(0.3)

# Start tracker immediately
tracker_thread = threading.Thread(target=window_tracker, daemon=True)
tracker_thread.start()

# Configuration
config = {
    "interval": 0.5,
    "target_app": "JX3_Client",
    "mode": "keyboard",
    "button": "left",
    "key": "q",
    "start_hotkey": "f9",
    "stop_hotkey": "f10"
}

def clicker_loop():
    global clicking
    logging.info(f"Clicker started. Mode: {config['mode']}, Key: {config['key']}, Target: {config['target_app']}")
    while clicking:
        # Check if active app matches target_app
        target = config["target_app"].strip()
        current = current_app_name
        
        logging.info(f"[DEBUG] Current window: '{current}', Target: '{target}'")
        
        if target and target != "所有软件" and target != "":
            current_lower = current.lower()
            target_lower = target.lower()
            
            # Smart JX3 matching
            is_jx3_current = "jx3" in current_lower or "剑网3" in current_lower or "剑网三" in current_lower
            is_jx3_target = "jx3" in target_lower or "剑网3" in target_lower or "剑网三" in target_lower
            
            match = False
            if is_jx3_target and is_jx3_current:
                match = True
            elif target_lower in current_lower:
                match = True
            elif current_lower in target_lower:
                match = True
                
            if not match:
                logging.info(f"[DEBUG] No match, skipping click")
                time.sleep(0.2)
                continue
        
        # Perform action
        try:
            if config["mode"] == "mouse":
                btn = mouse.Button.left if config["button"] == "left" else mouse.Button.right
                mouse_ctrl.click(btn, 1)
                logging.info(f"[DEBUG] Mouse clicked: {config['button']}")
            else:
                key_str = config["key"].lower()
                if key_str == 'space': k = keyboard.Key.space
                elif key_str == 'enter': k = keyboard.Key.enter
                elif key_str == 'tab': k = keyboard.Key.tab
                elif key_str == 'esc': k = keyboard.Key.esc
                elif key_str.startswith('f') and len(key_str) > 1:
                    k = getattr(keyboard.Key, key_str, key_str)
                else:
                    k = key_str
                
                logging.info(f"[DEBUG] Pressing key: {k}")
                keyboard_ctrl.press(k)
                time.sleep(0.02)
                keyboard_ctrl.release(k)
        except Exception as e:
            logging.error(f"Click error: {e}")

        time.sleep(max(0.01, config["interval"]))
    logging.info("Clicker stopped")

def on_press(key):
    global clicking, click_thread
    try:
        k = ""
        if hasattr(key, 'name') and key.name: k = key.name.lower()
        elif hasattr(key, 'char') and key.char: k = key.char.lower()
        
        start_key = config.get("start_hotkey", "f9").lower()
        stop_key = config.get("stop_hotkey", "f10").lower()
        
        if k == start_key or f"<{k}>" == start_key:
            if not clicking:
                clicking = True
                click_thread = threading.Thread(target=clicker_loop)
                click_thread.daemon = True
                click_thread.start()
        elif k == stop_key or f"<{k}>" == stop_key:
            clicking = False
    except:
        pass

def start_hotkeys():
    """Initializes the listener once. Config updates don't need to restart it."""
    global hotkey_listener
    if not hotkey_listener:
        try:
            hotkey_listener = keyboard.Listener(on_press=on_press)
            hotkey_listener.daemon = True
            hotkey_listener.start()
            logging.info("Global hotkey listener initialized.")
        except Exception as e:
            logging.error(f"Listener error: {e}")

# Initial start
threading.Thread(target=lambda: time.sleep(1) or start_hotkeys(), daemon=True).start()

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "clicking": clicking,
        "config": config,
        "active_app": current_app_name
    })

@app.route('/start', methods=['POST'])
def start_clicking():
    global clicking, click_thread
    data = request.json
    config.update({
        "interval": float(data.get("interval", 1.0)),
        "target_app": data.get("target_app", ""),
        "mode": data.get("mode", "mouse"),
        "button": data.get("button", "left"),
        "key": data.get("key", "f"),
        "start_hotkey": data.get("start_hotkey", "f9"),
        "stop_hotkey": data.get("stop_hotkey", "f10")
    })
    
    if not clicking:
        clicking = True
        click_thread = threading.Thread(target=clicker_loop)
        click_thread.daemon = True
        click_thread.start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop_clicking():
    global clicking
    clicking = False
    return jsonify({"status": "stopped"})

@app.route('/apps', methods=['GET'])
def get_apps():
    if not workspace: return jsonify({"apps": []})
    apps = workspace.runningApplications()
    app_names = sorted(list(set([app.localizedName() for app in apps if app.localizedName()])))
    return jsonify({"apps": app_names})

@app.route('/check_permissions', methods=['GET'])
def check_permissions():
    """Check if the app has necessary macOS permissions."""
    can_listen = False
    can_control = False
    
    # Test keyboard listener
    try:
        import Quartz
        # Try to create an event tap - this will fail without accessibility permission
        tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,
            Quartz.kCGHeadInsertEventTap,
            Quartz.kCGEventTapOptionListenOnly,
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown),
            lambda *args: None,
            None
        )
        if tap:
            can_listen = True
            can_control = True
    except:
        pass
    
    return jsonify({
        "accessibility": can_listen,
        "input_monitoring": can_control,
        "message": "" if (can_listen and can_control) else "请在「系统设置 → 隐私与安全性 → 辅助功能」和「输入监控」中启用连点器"
    })

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
    app.run(port=5005)
