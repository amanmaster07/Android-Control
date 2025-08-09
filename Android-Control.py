#!/usr/bin/env python3
import os
import json
import subprocess
import shlex

# Helper function
def run_cmd(cmd):
    try:
        p = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
        if p.stdout.strip():
            try:
                return json.loads(p.stdout)  # Parse JSON if possible
            except:
                return p.stdout.strip()
        else:
            return p.stderr.strip()
    except Exception as e:
        return f"Error: {e}"

# Menu items: {option_number: ("Label", "command")}
menu = {
    1: ("Battery Status", "termux-battery-status"),
    2: ("Set Brightness (0-255)", None),
    3: ("Call Log", "termux-call-log"),
    4: ("Camera Info", "termux-camera-info"),
    5: ("Take Photo", None),
    6: ("Clipboard Get", "termux-clipboard-get"),
    7: ("Clipboard Set", None),
    8: ("Contact List", "termux-contact-list"),
    9: ("GPS Location", "termux-location"),
    10: ("Play Media File", None),
    11: ("Record Audio", None),
    12: ("Send Notification", None),
    13: ("Sensor List", "termux-sensor -l"),
    14: ("Read Sensors", None),
    15: ("SMS List", "termux-sms-list"),
    16: ("Send SMS", None),
    17: ("Make Call", None),
    18: ("Toast Message", None),
    19: ("Torch On", "termux-torch on"),
    20: ("Torch Off", "termux-torch off"),
    21: ("Text to Speech", None),
    22: ("Vibrate", None),
    23: ("Get Volume", "termux-volume"),
    24: ("Set Volume", None),
    25: ("Wallpaper Change", None),
    26: ("WiFi Info", "termux-wifi-connectioninfo"),
    27: ("Enable WiFi", "termux-wifi-enable true"),
    28: ("Disable WiFi", "termux-wifi-enable false"),
    0: ("Exit", None)
}

while True:
    print("\n=== Termux API Control Menu ===")
    for k, v in menu.items():
        print(f"{k}. {v[0]}")

    try:
        choice = int(input("\nSelect option: "))
    except:
        print("Invalid choice")
        continue

    if choice not in menu:
        print("Invalid option number.")
        continue

    if choice == 0:
        print("Exiting...")
        break

    label, cmd = menu[choice]

    # Special cases where user input needed
    if label.startswith("Set Brightness"):
        level = input("Enter brightness (0-255): ")
        result = run_cmd(f"termux-brightness {level}")
    elif label == "Take Photo":
        path = input("Enter save path (/sdcard/photo.jpg): ")
        result = run_cmd(f"termux-camera-photo {path}")
    elif label == "Clipboard Set":
        text = input("Enter text to copy: ")
        result = subprocess.run(["termux-clipboard-set"], input=text, text=True)
        result = "Copied to clipboard."
    elif label == "Play Media File":
        path = input("Enter media file path: ")
        result = run_cmd(f"termux-media-player play {path}")
    elif label == "Record Audio":
        path = input("Enter save path (/sdcard/record.mp3): ")
        result = run_cmd(f"termux-microphone-record -f {path}")
    elif label == "Send Notification":
        title = input("Title: ")
        content = input("Content: ")
        result = run_cmd(f"termux-notification -t \"{title}\" -c \"{content}\"")
    elif label == "Read Sensors":
        sensor = input("Enter sensor name (e.g., accelerometer): ")
        result = run_cmd(f"termux-sensor -s {sensor} -n 1")
    elif label == "Send SMS":
        number = input("Enter number: ")
        text = input("Enter message: ")
        result = run_cmd(f"termux-sms-send -n {number} \"{text}\"")
    elif label == "Make Call":
        number = input("Enter number: ")
        result = run_cmd(f"termux-telephony-call {number}")
    elif label == "Toast Message":
        text = input("Enter toast text: ")
        result = run_cmd(f"termux-toast \"{text}\"")
    elif label == "Text to Speech":
        text = input("Enter text to speak: ")
        result = run_cmd(f"termux-tts-speak \"{text}\"")
    elif label == "Vibrate":
        ms = input("Enter milliseconds: ")
        result = run_cmd(f"termux-vibrate -d {ms}")
    elif label == "Set Volume":
        stream = input("Enter stream (music, ring, system, call, notification): ")
        level = input("Enter level: ")
        result = run_cmd(f"termux-volume {stream} {level}")
    elif label == "Wallpaper Change":
        path = input("Enter image path: ")
        result = run_cmd(f"termux-wallpaper -f {path}")
    else:
        result = run_cmd(cmd)

    print("\n--- Result ---")
    print(result)
