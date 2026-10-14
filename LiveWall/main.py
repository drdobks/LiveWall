import os
import sys
import glob
import time
import logging
import win32gui

# Configura caminho do MPV
if sys.platform == "win32":
    app_dir = os.path.abspath(os.path.dirname(__file__))
    if hasattr(os, "add_dll_directory"):
        try:
            os.add_dll_directory(app_dir)
        except Exception:
            pass
    os.environ["PATH"] = app_dir + os.pathsep + os.environ.get("PATH", "")

from config.manager import ConfigManager
from core.controller import Controller

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%H:%M:%S"
)

def find_any_video(videos_dir):
    extensions = ['*.mp4', '*.webm', '*.mkv', '*.avi', '*.mov']
    for ext in extensions:
        files = glob.glob(os.path.join(videos_dir, ext))
        if files:
            return files[0]
    return None

def main():
    print("========================================")
    print("      LIVEWALL - INICIANDO APP          ")
    print("========================================")
    
    config = ConfigManager()
    videos_dir = os.path.abspath(os.path.join("wallpapers", "videos"))
    wallpaper_path = config.get("wallpaper", "")
    full_wallpaper_path = os.path.abspath(wallpaper_path)
    
    if not os.path.exists(full_wallpaper_path):
        found_video = find_any_video(videos_dir)
        if found_video:
            config.set("wallpaper", os.path.relpath(found_video))
            full_wallpaper_path = found_video

    print(f"[1/3] Carregando video: {os.path.basename(full_wallpaper_path)}")
    print(f"[2/3] Injetando janela no Desktop...")
    controller = Controller(config)
    controller.start()
    
    print(f"[3/3] LiveWall RODANDO COM SUCESSO!")
    print("========================================")
    print("Atalhos disponiveis:")
    print(" -> Ctrl + Shift + A : Modo AFK")
    print(" -> Ctrl + Shift + S : Esconder/Mostrar Icones")
    print("========================================")
    
    # MENSAGEM DO WIN32: Mantem o Windows responsivo e remove a bolinha de carregamento do mouse!
    try:
        while controller.is_running:
            win32gui.PumpWaitingMessages()
            time.sleep(0.02)
    except KeyboardInterrupt:
        controller.stop()

if __name__ == "__main__":
    main()