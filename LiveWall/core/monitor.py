import win32gui
import win32api
import win32con
import win32process
import psutil
import threading
import time
import logging

logger = logging.getLogger("core.monitor")

class SystemMonitor(threading.Thread):
    def __init__(self, config, on_pause, on_resume):
        super().__init__(daemon=True)
        self.config = config
        self.on_pause = on_pause
        self.on_resume = on_resume
        self.running = True
        self.is_paused = False

    def run(self):
        while self.running:
            try:
                should_pause = self._check_fullscreen()
                if should_pause and not self.is_paused:
                    logger.info("Janela em tela cheia detectada. Pausando wallpaper...")
                    self.on_pause()
                    self.is_paused = True
                elif not should_pause and self.is_paused:
                    logger.info("Janela em tela cheia fechada. Retomando wallpaper...")
                    self.on_resume()
                    self.is_paused = False
            except Exception:
                pass
            time.sleep(2)

    def _check_fullscreen(self):
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return False
        
        try:
            # Ignora o proprio terminal e o Windows Explorer de pausar o video
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc_name = psutil.Process(pid).name().lower()
            if proc_name in ["cmd.exe", "powershell.exe", "explorer.exe", "conhost.exe", "python.exe", "py.exe"]:
                return False

            rect = win32gui.GetWindowRect(hwnd)
            screen_w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            screen_h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            
            # Se for janela cheia de jogo/app
            return (rect[2] - rect[0]) >= screen_w and (rect[3] - rect[1]) >= screen_h
        except Exception:
            return False

    def stop(self):
        self.running = False