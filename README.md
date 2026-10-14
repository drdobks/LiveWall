# 🖥️ LiveWall — Lightweight Windows Live Wallpaper Engine

**LiveWall** is an ultra-lightweight, high-performance alternative to Wallpaper Engine, built entirely in Python 3.11+. It renders high-quality animated wallpapers (videos) directly onto the Windows desktop background with minimal CPU and RAM usage.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Key Features

- 🚀 **Hardware Acceleration:** Uses MPV native hardware decoding (GPU accelerated, ultra-low CPU/RAM overhead).
- 🖥️ **WorkerW Desktop Injection:** Seamlessly renders video behind desktop icons without blocking desktop interactions.
- ⌨️ **AFK / Cinema Mode (`Ctrl + Shift + A`):** Instantly brings the wallpaper to the top layer when you step away.
- 🎮 **Smart Game & App Monitor:** Automatically pauses video playback when games or heavy full-screen apps are active.
- 📌 **System Tray Control:** Discreet system tray icon (`pystray`) for quick access, settings, and toggles.

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Video Renderer:** `python-mpv` (`libmpv`)
- **Windows Integration:** `pywin32` / `comtypes`
- **UI & Tray Icon:** `pystray` & `Pillow`
- **System Monitoring:** `psutil`

---

## 📥 Getting Started

### Prerequisites
- Windows 10/11
- Python 3.11 or higher installed

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/drdobks/LiveWall.git

2. **Instal dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Add your wallpapers:**
Place your video files (```.mp4```) inside the ```wallpapers/videos/``` directory.

4. **Run LiveWall:**
```bash
python main.py

## 🗺️ Roadmap

- [x] **Phase 1 (MVP):** WorkerW injection, MPV hardware decoding, game detection, AFK shortcut.
- [x] **Phase 2:** GIF support, automated video playlists, Web/HTML wallpaper support.
- [x] **Phase 3:** Custom Shaders (ModernGL), audio-reactive wallpapers, mouse parallax.
- [x] **Phase 4:** Standalone `.exe` compilation (Nuitka) & Windows auto-start integration.


 👤 Author
Created with ❤️ by Eduardo (drdobks)

Instagram: @drdobks
GitHub: @drdobks
