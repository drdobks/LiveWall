# LiveWall -- Lightweight Live Wallpaper Engine

A minimal, high-performance live wallpaper application for **Windows 10 / 11** that renders video behind the desktop icons using the WorkerW injection technique and mpv with NVDEC hardware decoding.

## Features (Phase 1 -- MVP)

| Feature | Description |
|---|---|
| **Desktop injection** | Renders behind desktop icons via WorkerW |
| **Video wallpaper** | mpv + NVDEC hardware decode, D3D11 output |
| **System tray** | Play/Pause, AFK, Exit with icon |
| **Fullscreen pause** | Auto-pauses when a fullscreen app is detected |
| **Game detection** | Pauses when a blacklisted process is in foreground |
| **AFK mode** | Fullscreen clock overlay (Ctrl+Shift+A or auto-idle) |
| **Idle detection** | Auto-AFK after configurable idle seconds |
| **Hot-reload config** | Edit `settings.json` while running |
| **Remember last** | Restores the last wallpaper on next launch |

## Requirements

- **Python** 3.11+
- **Windows** 10 / 11 (desktop composition / DWM must be enabled)
- **GPU** with NVDEC support (GTX 600+ series)
- **mpv** (libmpv) -- see below

## Installation

### 1. Clone / download this repository

```
git clone <repo-url> LiveWall
cd LiveWall
```

### 2. Install Python dependencies

```
pip install -r requirements.txt
```

### 3. Install mpv (libmpv)

The video renderer requires **libmpv**.  Two options:

**Option A -- mpv on PATH** (recommended)

1. Download mpv from <https://mpv.io/installation/> or <https://sourceforge.net/projects/mpv-player-windows/files/>
2. Extract and add the folder containing `mpv.exe` to your system PATH.

**Option B -- DLL beside the script**

1. From the same download, copy `mpv-2.dll` (or `libmpv-2.dll`) into the LiveWall root directory (next to `main.py`).

### 4. Add a wallpaper

Drop a `.mp4` (or other video) file into `wallpapers/videos/` and update `settings.json`:

```json
{
    "wallpaper": "wallpapers/videos/my_video.mp4"
}
```

## Usage

```
python main.py
```

The app will:
1. Wait for the configured startup delay (default 5 s).
2. Inject a render window behind the desktop icons.
3. Start playing the configured video wallpaper.
4. Show a system-tray icon with a context menu.

### Hotkeys

| Hotkey | Action |
|---|---|
| **Ctrl+Shift+A** | Toggle AFK mode (fullscreen clock overlay) |

### Tray menu

- **Play / Pause** -- toggle wallpaper playback
- **AFK Mode** -- toggle AFK overlay
- **Exit** -- save state and quit

## Configuration

Edit `settings.json` while the app is running -- changes are applied automatically.

```jsonc
{
    "wallpaper": "wallpapers/videos/default.mp4",
    "playlist": [],                    // Phase 2
    "playlist_interval": 600,          // Phase 2
    "afk": {
        "enabled": true,
        "hotkey": "ctrl+shift+a",
        "idle_seconds": 300,           // auto-AFK after 5 min idle
        "show_clock": true,
        "clock_format": "%H:%M"
    },
    "performance": {
        "max_fps": 60,
        "pause_fullscreen": true,
        "pause_games": true,
        "game_blacklist": ["steam.exe", "valorant.exe", "minecraft.exe"],
        "startup_delay": 5
    },
    "display": {
        "multi_monitor": "mirror"       // Phase 2
    },
    "silent_mode": false                // Phase 4
}
```

## Performance Targets

| State | RAM | CPU |
|---|---|---|
| Video playback | < 150 MB | < 2 % (NVDEC) |
| Idle / AFK | < 80 MB | < 1 % |

## Project Structure

```
LiveWall/
├── main.py                 # Entry point
├── requirements.txt
├── settings.json
├── core/
│   ├── desktop.py          # WorkerW injection
│   ├── window.py           # Render window management
│   ├── monitor.py          # Fullscreen / game detection
│   ├── controller.py       # App orchestrator
│   └── afk.py              # AFK overlay
├── renderers/
│   ├── base.py             # ABC
│   └── video.py            # mpv + NVDEC
├── interaction/
│   ├── hotkey.py           # Win32 RegisterHotKey
│   └── idle.py             # GetLastInputInfo
├── ui/
│   └── tray.py             # pystray
├── config/
│   └── manager.py          # JSON + hot-reload
└── wallpapers/
    ├── videos/
    ├── gifs/               # Phase 2
    ├── web/                # Phase 2
    └── shaders/            # Phase 3
```

## Troubleshooting

| Issue | Fix |
|---|---|
| "Progman not found" | Restart Explorer (`taskkill /f /im explorer.exe && start explorer.exe`) |
| "WorkerW not found" | Ensure DWM desktop composition is enabled (default on Win 10/11) |
| mpv / libmpv error | Ensure `mpv-2.dll` is on PATH or beside `main.py` |
| Hotkey not working | Another app may have registered Ctrl+Shift+A; change in `settings.json` |
| Black screen | Verify the video file path in `settings.json` is correct |

## Roadmap

- **Phase 2** -- GIF, WebView2, image slideshow, playlists, multi-monitor
- **Phase 3** -- GLSL shaders, GPU particles, audio-reactive, mouse parallax
- **Phase 4** -- Settings GUI, Nuitka build, auto-start, CPU throttling

## License

Personal use.  Not affiliated with Wallpaper Engine.
