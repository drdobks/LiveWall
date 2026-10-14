import ctypes
from ctypes import wintypes
import threading
import win32con
import logging

logger = logging.getLogger("interaction.hotkey")
user32 = ctypes.windll.user32

class HotkeyManager(threading.Thread):
    def __init__(self, on_afk_callback=None, on_toggle_icons_callback=None):
        super().__init__(daemon=True)
        self.on_afk = on_afk_callback
        self.on_toggle_icons = on_toggle_icons_callback
        self.running = True

    def run(self):
        MOD_CONTROL = 0x0002
        MOD_SHIFT = 0x0004
        MOD_NOREPEAT = 0x4000

        VK_A = 0x41  # Tecla A
        VK_S = 0x53  # Tecla S

        # Registra Atalhos Globais
        res1 = user32.RegisterHotKey(None, 1, MOD_CONTROL | MOD_SHIFT | MOD_NOREPEAT, VK_A)
        res2 = user32.RegisterHotKey(None, 2, MOD_CONTROL | MOD_SHIFT | MOD_NOREPEAT, VK_S)

        if res1:
            logger.info("Atalho registrado: Ctrl + Shift + A (Modo AFK)")
        else:
            logger.error("Falha ao registrar Ctrl + Shift + A (ja em uso por outro app)")

        if res2:
            logger.info("Atalho registrado: Ctrl + Shift + S (Esconder Icones)")
        else:
            logger.error("Falha ao registrar Ctrl + Shift + S (ja em uso por outro app)")

        msg = wintypes.MSG()
        while self.running:
            res = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if res == 0 or res == -1:
                break

            if msg.message == win32con.WM_HOTKEY:
                if msg.wParam == 1 and self.on_afk:
                    logger.info(">>> ATALHO DETECTADO: Modo AFK <<<")
                    self.on_afk()
                elif msg.wParam == 2 and self.on_toggle_icons:
                    logger.info(">>> ATALHO DETECTADO: Toggle Icones <<<")
                    self.on_toggle_icons()

            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def stop(self):
        self.running = False
        user32.UnregisterHotKey(None, 1)
        user32.UnregisterHotKey(None, 2)