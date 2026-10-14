import win32gui
import win32con
import win32api
import logging

logger = logging.getLogger("core.afk")

class AFKManager:
    def __init__(self, config_manager, wallpaper_path=""):
        self.config = config_manager
        self.wallpaper_path = wallpaper_path
        self.is_active = False
        self.overlay_hwnd = None

    def toggle(self):
        if self.is_active: self.deactivate()
        else: self.activate()

    def activate(self):
        if self.is_active: return
        self.is_active = True

        # CORREÇÃO AQUI: win32api
        width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        wnd_class = win32gui.WNDCLASS()
        wnd_class.hInstance = win32gui.GetModuleHandle(None)
        wnd_class.lpszClassName = "LiveWallAFKOverlay"
        wnd_class.lpfnWndProc = {win32con.WM_KEYDOWN: self._on_input, win32con.WM_LBUTTONDOWN: self._on_input}

        try: win32gui.RegisterClass(wnd_class)
        except: pass

        self.overlay_hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW,
            "LiveWallAFKOverlay", "LiveWall AFK",
            win32con.WS_POPUP | win32con.WS_VISIBLE,
            0, 0, width, height, 0, 0, wnd_class.hInstance, None
        )

    def deactivate(self):
        if self.overlay_hwnd:
            win32gui.DestroyWindow(self.overlay_hwnd)
            self.overlay_hwnd = None
        self.is_active = False

    def _on_input(self, hwnd, msg, wparam, lparam):
        self.deactivate()
        return 0