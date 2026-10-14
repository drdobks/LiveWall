# 🖥️ LiveWall 

**LiveWall** is an ultra-lightweight, high-performance alternative to Wallpaper Engine, built entirely in Python. It allows you to use high-quality videos as live wallpapers on Windows without killing your RAM or CPU.

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **🚀 High Performance:** Uses hardware-accelerated video decoding (NVIDIA/AMD/Intel) via MPV.
- **📦 Ultra Lightweight:** Minimalist resource usage, perfect for gaming setups.
- **🖼️ Desktop Integration:** Injects video directly behind desktop icons (WorkerW method).
- **⌨️ AFK Mode:** Press `Ctrl + Shift + A` to bring the wallpaper to the front for an aesthetic idle screen.
- **🎮 Game Detection:** Automatically pauses video when full-screen games or heavy apps are running.

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Video Core:** MPV (libmpv)
- **API:** Win32 API (pywin32) for desktop injection.
- **UI/System Tray:** Pystray & Pillow.

## 🚀 How to Run

1. **Clone the repo:**
   ```bash
   git clone https://github.com/drdobks/LiveWall.git
