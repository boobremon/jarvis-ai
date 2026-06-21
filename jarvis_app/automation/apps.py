"""
JARVIS Application Automation Module
Created by Sohail Karim

Handles opening applications, websites, and system commands.
"""

import os
import subprocess
import webbrowser
import shutil
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import platform

from jarvis_app.core.logger import get_logger


class AutomationEngine:
    """Handles application and system automation"""

    def __init__(self):
        self.logger = get_logger()
        self.system = platform.system()

        # Standard applications with common paths
        self._app_registry = self._build_app_registry()

        # Website shortcuts
        self._website_registry = {
            "google": "https://google.com",
            "youtube": "https://youtube.com",
            "github": "https://github.com",
            "stackoverflow": "https://stackoverflow.com",
            "chatgpt": "https://chat.openai.com",
            "claude": "https://claude.ai",
            "gmail": "https://mail.google.com",
            "spotify web": "https://open.spotify.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://linkedin.com",
            "reddit": "https://reddit.com",
            "amazon": "https://amazon.com",
            "netflix": "https://netflix.com",
            "facebook": "https://facebook.com",
            "instagram": "https://instagram.com",
            "whatsapp": "https://web.whatsapp.com",
            "discord web": "https://discord.com/app",
            "slack": "https://slack.com",
        }

        # Command aliases
        self._command_aliases = {
            "chrome": ["google chrome", "open chrome", "chrome browser"],
            "edge": ["microsoft edge", "open edge", "edge browser"],
            "vscode": ["visual studio code", "vs code", "code editor", "open code"],
            "steam": ["open steam", "gaming", "steam app"],
            "discord": ["open discord", "discord app"],
            "spotify": ["open spotify", "music player", "spotify player"],
            "notepad": ["open notepad", "text editor", "notepad app"],
            "calculator": ["open calculator", "calc", "calculator app"],
            "settings": ["open settings", "system settings", "windows settings"],
        }

    def _build_app_registry(self) -> Dict[str, List[str]]:
        """Build registry of known applications and their paths"""
        if self.system != "Windows":
            return {}

        program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        local_app_data = os.environ.get("LOCALAPPDATA", "")

        return {
            "chrome": [
                f"{program_files}\\Google\\Chrome\\Application\\chrome.exe",
                f"{program_files_x86}\\Google\\Chrome\\Application\\chrome.exe",
            ],
            "edge": [
                f"{program_files(x86)}\\Microsoft\\Edge\\Application\\msedge.exe",
                "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            ],
            "vscode": [
                f"{local_app_data}\\Programs\\Microsoft VS Code\\Code.exe",
                f"{program_files}\\Microsoft VS Code\\Code.exe",
            ],
            "steam": [
                "C:\\Program Files (x86)\\Steam\\steam.exe",
                "D:\\Steam\\steam.exe",
            ],
            "discord": [
                f"{local_app_data}\\Discord\\app-*\\Discord.exe",
                f"{local_app_data}\\Discord\\Update.exe --processStart Discord.exe",
            ],
            "spotify": [
                f"{local_app_data}\\Spotify\\Spotify.exe",
                f"{program_files}\\Spotify\\Spotify.exe",
            ],
            "notepad": ["notepad.exe"],
            "calculator": ["calc.exe"],
            "settings": ["start ms-settings:"],
            "file explorer": ["explorer.exe"],
            "cmd": ["cmd.exe"],
            "powershell": ["powershell.exe"],
            "terminal": ["wt.exe"],
            "task manager": ["taskmgr.exe"],
            "control panel": ["control.exe"],
            "device manager": ["devmgmt.msc"],
            "paint": ["mspaint.exe"],
            "wordpad": ["write.exe"],
        }

    def open_application(self, app_name: str) -> Tuple[bool, str]:
        """Open an application by name"""
        app_name_lower = app_name.lower().strip()

        # Check aliases
        for main_app, aliases in self._command_aliases.items():
            if app_name_lower in aliases or app_name_lower == main_app:
                app_name_lower = main_app
                break

        # Check if it's in the registry
        if app_name_lower in self._app_registry:
            paths = self._app_registry[app_name_lower]

            for path in paths:
                if self._try_open_path(path):
                    self.logger.command(f"open {app_name}", "SUCCESS")
                    return True, f"Opening {app_name}"

            self.logger.command(f"open {app_name}", "FAILED - Path not found")
            return False, f"Could not find {app_name} installation"

        # Try as a generic Windows command
        if self.system == "Windows":
            try:
                os.system(f"start {app_name}")
                self.logger.command(f"open {app_name}", "SUCCESS")
                return True, f"Opening {app_name}"
            except Exception:
                pass

        self.logger.command(f"open {app_name}", "FAILED - Unknown app")
        return False, f"Unknown application: {app_name}"

    def _try_open_path(self, path: str) -> bool:
        """Try to open an application path"""
        try:
            # Handle wildcard paths (like Discord app-* pattern)
            if "*" in path:
                parent_dir = Path(path).parent.parent
                if parent_dir.exists():
                    # Find matching executable
                    for item in parent_dir.glob("app-*"):
                        exe_path = item / "Discord.exe"
                        if exe_path.exists():
                            subprocess.Popen([str(exe_path)])
                            return True
                return False

            if path.startswith("start "):
                subprocess.Popen(path, shell=True)
                return True

            if os.path.exists(path):
                subprocess.Popen([path])
                return True

            # Try as raw command
            subprocess.Popen(path)
            return True

        except Exception:
            return False

    def open_website(self, site_name: str, query: str = None) -> Tuple[bool, str]:
        """Open a website by name or URL"""
        site_name_lower = site_name.lower().strip()

        # Check if it's a known website
        if site_name_lower in self._website_registry:
            url = self._website_registry[site_name_lower]
            if query:
                url = f"{url}/search?q={query}"
            webbrowser.open(url)
            self.logger.command(f"open {site_name}", "SUCCESS")
            return True, f"Opening {site_name}"

        # Check if it's a URL
        if site_name.startswith("http://") or site_name.startswith("https://"):
            webbrowser.open(site_name)
            self.logger.command(f"open {site_name}", "SUCCESS")
            return True, f"Opening {site_name}"

        # Assume it's a domain
        url = f"https://{site_name}"
        webbrowser.open(url)
        self.logger.command(f"open {site_name}", "SUCCESS")
        return True, f"Opening {site_name}"

    def search_google(self, query: str) -> Tuple[bool, str]:
        """Search Google for a query"""
        if not query:
            return False, "No search query provided"

        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        self.logger.command(f"google search: {query}", "SUCCESS")
        return True, f"Searching Google for '{query}'"

    def search_youtube(self, query: str) -> Tuple[bool, str]:
        """Search YouTube for a query"""
        if not query:
            return False, "No search query provided"

        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        self.logger.command(f"youtube search: {query}", "SUCCESS")
        return True, f"Searching YouTube for '{query}'"

    def execute_system_command(self, command: str) -> Tuple[bool, str]:
        """Execute system command"""
        command_lower = command.lower().strip()

        if self.system == "Windows":
            return self._execute_windows_command(command_lower)
        else:
            return self._execute_unix_command(command_lower)

    def _execute_windows_command(self, command: str) -> Tuple[bool, str]:
        """Execute Windows system command"""
        commands = {
            "shutdown": ("shutdown /s /t 0", "Shutting down"),
            "restart": ("shutdown /r /t 0", "Restarting"),
            "sign out": ("shutdown /l", "Signing out"),
            "lock": ("rundll32.exe user32.dll,LockWorkStation", "Locking PC"),
            "sleep": ("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", "Putting PC to sleep"),
            "hibernate": ("shutdown /h", "Hibernating"),
            "mute": ("nircmd.exe mutesysvolume 1", "Muted"),
            "unmute": ("nircmd.exe mutesysvolume 0", "Unmuted"),
        }

        for cmd_key, (cmd_exec, msg) in commands.items():
            if cmd_key in command:
                try:
                    os.system(cmd_exec)
                    self.logger.command(cmd_key, "SUCCESS")
                    return True, f"{msg}, Sir"
                except Exception as e:
                    self.logger.error(f"System command failed: {e}")
                    return False, f"Failed to execute {cmd_key}"

        return False, f"Unknown system command: {command}"

    def _execute_unix_command(self, command: str) -> Tuple[bool, str]:
        """Execute Unix system command"""
        commands = {
            "shutdown": ("shutdown now", "Shutting down"),
            "restart": ("reboot", "Restarting"),
            "lock": ("loginctl lock-session", "Locking"),
        }

        for cmd_key, (cmd_exec, msg) in commands.items():
            if cmd_key in command:
                try:
                    subprocess.run(cmd_exec, shell=True)
                    self.logger.command(cmd_key, "SUCCESS")
                    return True, f"{msg}, Sir"
                except Exception as e:
                    self.logger.error(f"System command failed: {e}")
                    return False, f"Failed to execute {cmd_key}"

        return False, f"Unknown system command: {command}"

    def set_volume(self, level: int) -> Tuple[bool, str]:
        """Set system volume (0-100)"""
        level = max(0, min(100, level))

        if self.system == "Windows":
            try:
                import winsound
                os.system(f"nircmd.exe setsysvolume {int(level * 655.35)}")
                return True, f"Volume set to {level} percent"
            except Exception:
                return False, "Volume control not available"
        else:
            return False, "Volume control only available on Windows"

    def open_file(self, file_path: str) -> Tuple[bool, str]:
        """Open a file with default application"""
        try:
            path = Path(file_path).expanduser()

            if not path.exists():
                return False, f"File not found: {file_path}"

            if self.system == "Windows":
                os.startfile(str(path))
            else:
                subprocess.run(["xdg-open", str(path)])

            self.logger.command(f"open file {file_path}", "SUCCESS")
            return True, f"Opening {path.name}"

        except Exception as e:
            self.logger.error(f"Open file error: {e}")
            return False, f"Could not open file: {e}"

    def search_files(self, query: str) -> List[Path]:
        """Search for files matching query"""
        results = []

        try:
            if self.system == "Windows":
                # Use Everything ES (if installed) or basic search
                home = Path.home()
                for ext in ["*"]:
                    for match in home.rglob(f"*{query}*"):
                        results.append(match)
                        if len(results) >= 20:
                            return results

        except Exception:
            pass

        return results

    def register_custom_app(self, name: str, path: str) -> None:
        """Register a custom application"""
        self._app_registry[name.lower()] = [path]
        self.logger.info(f"Registered custom app: {name} -> {path}")
