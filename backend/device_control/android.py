"""
Android Device Controller via ADB
"""

import subprocess
import time
from typing import Tuple, Optional


class AndroidController:
    """Android automation via ADB."""

    ADB_PATH = "adb"

    @classmethod
    def _run_adb(cls, command: list) -> Tuple[bool, str]:
        full_cmd = [cls.ADB_PATH] + command
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()

        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except FileNotFoundError:
            return False, "ADB not found. Install Android SDK platform-tools."
        except Exception as e:
            return False, str(e)

    @classmethod
    def check_connection(cls) -> bool:
        success, output = cls._run_adb(["devices"])
        if success and "device" in output:
            lines = output.strip().split('\n')[1:]
            for line in lines:
                if 'device' in line and not line.startswith('*'):
                    print(f"📱 Android connected: {line.split()[0]}")
                    return True
        print("📱 No Android device found. Enable USB debugging and connect.")
        return False

    @classmethod
    def tap(cls, x: int, y: int):
        success, output = cls._run_adb(["shell", "input", "tap", str(x), str(y)])
        if success:
            print(f"📱 Tapped at ({x}, {y})")
        return success

    @classmethod
    def swipe(cls, x1: int, y1: int, x2: int, y2: int, duration: int = 300):
        success, _ = cls._run_adb([
            "shell", "input", "swipe",
            str(x1), str(y1), str(x2), str(y2), str(duration)
        ])
        return success

    @classmethod
    def type_text(cls, text: str):
        safe_text = text.replace(" ", "%s")
        success, _ = cls._run_adb(["shell", "input", "text", safe_text])
        if success:
            print(f"📱 Typed: {text[:50]}")
        return success

    @classmethod
    def press_key(cls, keycode: str):
        key_map = {
            "home": "KEYCODE_HOME", "back": "KEYCODE_BACK",
            "menu": "KEYCODE_MENU", "power": "KEYCODE_POWER",
            "volume_up": "KEYCODE_VOLUME_UP",
            "volume_down": "KEYCODE_VOLUME_DOWN",
            "camera": "KEYCODE_CAMERA", "enter": "KEYCODE_ENTER",
        }

        keycode = key_map.get(keycode.lower(), keycode)
        success, _ = cls._run_adb(["shell", "input", "keyevent", keycode])
        return success

    @classmethod
    def take_screenshot(cls) -> Optional[str]:
        device_path = "/sdcard/jane_screenshot.png"
        success, _ = cls._run_adb(["shell", "screencap", "-p", device_path])

        if success:
            local_path = "jane_android_screenshot.png"
            cls._run_adb(["pull", device_path, local_path])
            print(f"📱 Screenshot saved: {local_path}")
            return local_path
        return None

    @classmethod
    def get_screen_size(cls) -> Tuple[int, int]:
        success, output = cls._run_adb(["shell", "wm", "size"])
        if success:
            try:
                size_str = output.split(":")[1].strip()
                width, height = map(int, size_str.split("x"))
                return width, height
            except:
                pass
        return (1080, 1920)

    @classmethod
    def open_app(cls, package_name: str):
        success, _ = cls._run_adb([
            "shell", "monkey", "-p", package_name, "-c", 
            "android.intent.category.LAUNCHER", "1"
        ])
        if success:
            print(f"📱 Opened: {package_name}")
        return success

    @classmethod
    def list_apps(cls) -> list:
        success, output = cls._run_adb([
            "shell", "pm", "list", "packages", "-3"
        ])
        if success:
            apps = [line.replace("package:", "") for line in output.split('\n') if line]
            return apps
        return []

    @classmethod
    def reboot(cls):
        cls._run_adb(["reboot"])
        print("📱 Rebooting Android...")

    @classmethod
    def shutdown(cls):
        cls._run_adb(["shell", "reboot", "-p"])
