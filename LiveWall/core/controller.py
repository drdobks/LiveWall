import logging
import os
import win32gui
import win32con
import win32api
from renderers.video import VideoRenderer
from core.window import RenderWindow
from core.desktop import find_workerw, inject_window, toggle_desktop_icons
from core.monitor import SystemMonitor
from interaction.hotkey import HotkeyManager
from ui.tray import TrayIcon

logger = logging.getLogger("core.controller")

class Controller:
    def __init__(self, config_manager):
        self.config = config_manager
        self.render_window = None
        self.renderer = None
        self.monitor = None
        self.hotkey_manager = None
        self.tray = None
        self.workerw = None
        self.is_running = False
        self.is_afk = False

    def start(self):
        logger.info("Iniciando LiveWall Controller...")
        self.is_running = True
        self.workerw = find_workerw()

        # Cria janela de renderizacao
        self.render_window = RenderWindow()
        self.render_window.create()

        # Injeta no desktop
        inject_window(self.render_window.hwnd, self.workerw)

        # Inicia o video
        wallpaper_path = self.config.get("wallpaper", "")
        if os.path.exists(wallpaper_path):
            self.renderer = VideoRenderer(self.render_window.hwnd, wallpaper_path)
            self.renderer.play()

        # Registra atalhos
        self.hotkey_manager = HotkeyManager(
            on_afk_callback=self.toggle_afk,
            on_toggle_icons_callback=self.toggle_icons
        )
        self.hotkey_manager.start()

        # Monitor de tela cheia
        self.monitor = SystemMonitor(self.config, on_pause=self.pause, on_resume=self.resume)
        self.monitor.start()

        # Tray Icon
        self.tray = TrayIcon(self)
        self.tray.run()

    def toggle_afk(self):
        if not self.render_window or not self.render_window.hwnd:
            return

        screen_w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        if not self.is_afk:
            # MODO AFK: Tira do fundo e coloca em tela cheia por cima de tudo
            win32gui.SetParent(self.render_window.hwnd, 0)
            win32gui.SetWindowPos(
                self.render_window.hwnd, win32con.HWND_TOPMOST,
                0, 0, screen_w, screen_h, win32con.SWP_SHOWWINDOW
            )
            self.is_afk = True
            logger.info("MODO AFK ATIVADO: Video em Tela Cheia!")
        else:
            # MODO NORMAL: Volta para trás dos ícones
            inject_window(self.render_window.hwnd, self.workerw)
            self.is_afk = False
            logger.info("MODO AFK DESATIVADO: Video voltou ao fundo.")

    def toggle_icons(self):
        toggle_desktop_icons()

    def pause(self):
        if self.renderer and not self.is_afk:
            self.renderer.pause()

    def resume(self):
        if self.renderer:
            self.renderer.resume()

    def stop(self):
        self.is_running = False
        if self.hotkey_manager: self.hotkey_manager.stop()
        if self.monitor: self.monitor.stop()
        if self.renderer: self.renderer.stop()
        if self.render_window: self.render_window.destroy()
        logger.info("LiveWall finalizado.")