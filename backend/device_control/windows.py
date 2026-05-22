"""
Windows Device Controller
Controls Fhish's PC
"""

import subprocess
import os
import pyautogui
from datetime import datetime
from typing import Optional


class WindowsController:
    """Windows automation using pyautogui and subprocess."""

    @staticmethod
    def screenshot() -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jane_screenshot_{timestamp}.png"
        path = os.path.join(os.path.expanduser("~"), "Pictures", "Jane", filename)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        screenshot = pyautogui.screenshot()
        screenshot.save(path)

        print(f"📸 Screenshot saved: {path}")
        return path

    @staticmethod
    def open_application(app_name: str) -> bool:
        app_map = {
            "chrome": "chrome", "browser": "chrome", "firefox": "firefox",
            "edge": "msedge", "notepad": "notepad", "spotify": "spotify",
            "discord": "discord", "code": "code", "vscode": "code",
            "explorer": "explorer", "cmd": "cmd", "terminal": "wt",
            "calculator": "calc", "settings": "ms-settings:",
            "task manager": "taskmgr", "paint": "mspaint",
            "word": "winword", "excel": "excel", "powerpoint": "powerpnt",
        }

        try:
            command = app_map.get(app_name.lower(), app_name)
            subprocess.Popen(command, shell=True)
            print(f"🖥️ Opened: {app_name}")
            return True

        except Exception as e:
            print(f"❌ Failed to open {app_name}: {e}")
            return False

    @staticmethod
    def type_text(text: str, interval: float = 0.05):
        pyautogui.typewrite(text, interval=interval)
        print(f"⌨️ Typed: {text[:50]}{'...' if len(text) > 50 else ''}")

    @staticmethod
    def press_key(key: str):
        pyautogui.press(key)

    @staticmethod
    def volume_up():
        pyautogui.press("volumeup", presses=5)
        print("🔊 Volume up")

    @staticmethod
    def volume_down():
        pyautogui.press("volumedown", presses=5)
        print("🔉 Volume down")

    @staticmethod
    def mute():
        pyautogui.press("volumemute")
        print("🔇 Mute toggled")

    @staticmethod
    def play_pause():
        pyautogui.press("playpause")
        print("⏯️ Play/Pause")

    @staticmethod
    def next_track():
        pyautogui.press("nexttrack")
        print("⏭️ Next track")

    @staticmethod
    def previous_track():
        pyautogui.press("prevtrack")
        print("⏮️ Previous track")

    @staticmethod
    def minimize_window():
        pyautogui.keyDown('win')
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
        pyautogui.keyUp('win')

    @staticmethod
    def maximize_window():
        pyautogui.keyDown('win')
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
        pyautogui.keyUp('win')

    @staticmethod
    def lock_pc():
        pyautogui.keyDown('win')
        pyautogui.keyDown('l')
        pyautogui.keyUp('l')
        pyautogui.keyUp('win')
        print("🔒 PC locked")

    @staticmethod
    def get_clipboard() -> str:
        import pyperclip
        return pyperclip.paste()

    @staticmethod
    def set_clipboard(text: str):
        import pyperclip
        pyperclip.copy(text)
        print("📋 Clipboard updated")
