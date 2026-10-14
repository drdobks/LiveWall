"""Configuration manager with JSON persistence and hot-reload.

Provides dot-notation access to nested config values and watches for
file modifications via Win32 ReadDirectoryChangesW.
"""

import copy
import json
import logging
import threading
import time
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

DEFAULT_CONFIG: dict = {
    "wallpaper": "wallpapers/videos/default.mp4",
    "playlist": [],
    "playlist_interval": 600,
    "afk": {
        "enabled": True,
        "hotkey": "ctrl+shift+a",
        "idle_seconds": 300,
        "wallpaper": "",
        "show_clock": True,
        "clock_format": "%H:%M",
    },
    "performance": {
        "max_fps": 60,
        "pause_fullscreen": True,
        "pause_games": True,
        "game_blacklist": ["steam.exe", "valorant.exe", "minecraft.exe"],
        "startup_delay": 5,
    },
    "display": {
        "multi_monitor": "mirror",
    },
    "silent_mode": False,
}


class ConfigManager:
    """Application configuration with file persistence and hot-reload.

    Supports dot-notation access (e.g., ``get('afk.idle_seconds')``),
    automatic file watching via Win32 ``ReadDirectoryChangesW``, and
    change-notification callbacks.
    """

    def __init__(self, config_path: str = "settings.json") -> None:
        self._path = Path(config_path).resolve()
        self._data: dict = {}
        self._callbacks: list[Callable[[dict], None]] = []
        self._watcher_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.load()

    # -- persistence ---------------------------------------------------------

    def load(self) -> dict:
        """Load configuration from disk, merging with defaults."""
        try:
            if self._path.exists():
                with open(self._path, "r", encoding="utf-8") as fh:
                    loaded = json.load(fh)
                self._data = self._deep_merge(
                    copy.deepcopy(DEFAULT_CONFIG), loaded
                )
            else:
                self._data = copy.deepcopy(DEFAULT_CONFIG)
                self.save()
            logger.info("Configuration loaded from %s", self._path)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to load config, using defaults: %s", exc)
            self._data = copy.deepcopy(DEFAULT_CONFIG)
        return self._data

    def save(self) -> None:
        """Persist current configuration to disk."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as fh:
            json.dump(self._data, fh, indent=4, ensure_ascii=False)

    # -- access --------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value using dot-notation (e.g., ``'afk.idle_seconds'``)."""
        parts = key.split(".")
        node: Any = self._data
        for part in parts:
            if isinstance(node, dict):
                node = node.get(part)
                if node is None:
                    return default
            else:
                return default
        return node

    def set(self, key: str, value: Any) -> None:
        """Set a value using dot-notation and persist to disk."""
        parts = key.split(".")
        node = self._data
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value
        self.save()

    @property
    def data(self) -> dict:
        """Return the full configuration dictionary."""
        return self._data

    @property
    def path(self) -> Path:
        """Return the resolved configuration file path."""
        return self._path

    # -- hot-reload ----------------------------------------------------------

    def on_change(self, callback: Callable[[dict], None]) -> None:
        """Register a callback invoked when the config file changes."""
        self._callbacks.append(callback)

    def start_watching(self) -> None:
        """Start background thread watching for config file modifications."""
        if self._watcher_thread and self._watcher_thread.is_alive():
            return
        self._stop_event.clear()
        self._watcher_thread = threading.Thread(
            target=self._watch_loop, daemon=True, name="ConfigWatcher"
        )
        self._watcher_thread.start()
        logger.info("Config file watcher started")

    def stop_watching(self) -> None:
        """Signal the watcher thread to stop."""
        self._stop_event.set()

    def _watch_loop(self) -> None:
        """Watch config directory via ReadDirectoryChangesW (blocking)."""
        import win32con
        import win32file

        directory = str(self._path.parent)
        try:
            handle = win32file.CreateFile(
                directory,
                win32con.FILE_LIST_DIRECTORY,
                (
                    win32con.FILE_SHARE_READ
                    | win32con.FILE_SHARE_WRITE
                    | win32con.FILE_SHARE_DELETE
                ),
                None,
                win32con.OPEN_EXISTING,
                win32con.FILE_FLAG_BACKUP_SEMANTICS,
                None,
            )
        except Exception as exc:
            logger.error("Failed to open directory for watching: %s", exc)
            return

        while not self._stop_event.is_set():
            try:
                results = win32file.ReadDirectoryChangesW(
                    handle, 4096, False,
                    win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
                    None, None,
                )
                for _action, filename in results:
                    if filename == self._path.name:
                        time.sleep(0.1)  # Let write complete
                        self.load()
                        for cb in self._callbacks:
                            try:
                                cb(self._data)
                            except Exception as exc:
                                logger.error("Config callback error: %s", exc)
                        logger.info("Config hot-reloaded")
            except Exception as exc:
                if not self._stop_event.is_set():
                    logger.error("Config watch error: %s", exc)
                break

    # -- helpers -------------------------------------------------------------

    @staticmethod
    def _deep_merge(base: dict, override: dict) -> dict:
        """Recursively merge *override* into *base*, returning *base*."""
        for key, value in override.items():
            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                ConfigManager._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
