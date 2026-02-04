"""Add or remove BTC Widget from Windows startup."""

import os
import sys
import winreg

APP_NAME = "BTCWidget"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONW_PATH = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, "main.py")


def get_startup_command() -> str:
    """Get the command to run the widget silently."""
    return f'"{PYTHONW_PATH}" "{MAIN_SCRIPT}"'


def add_to_startup():
    """Add the widget to Windows startup via registry."""
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, get_startup_command())
    winreg.CloseKey(key)
    print(f"Added {APP_NAME} to startup.")


def remove_from_startup():
    """Remove the widget from Windows startup."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        print(f"Removed {APP_NAME} from startup.")
    except FileNotFoundError:
        print(f"{APP_NAME} is not in startup.")


def is_in_startup() -> bool:
    """Check if the widget is in startup."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--add":
            add_to_startup()
        elif sys.argv[1] == "--remove":
            remove_from_startup()
        elif sys.argv[1] == "--status":
            status = "enabled" if is_in_startup() else "disabled"
            print(f"Auto-start is {status}.")
        else:
            print("Usage: python autostart.py [--add|--remove|--status]")
    else:
        # Toggle
        if is_in_startup():
            remove_from_startup()
        else:
            add_to_startup()
