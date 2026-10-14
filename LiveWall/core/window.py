import win32gui
import win32con
import win32api
import logging

logger = logging.getLogger("core.window")

class RenderWindow:
    def __init__(self):
        self.hwnd = None
        self.class_name = "LiveWallRenderWindow"

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        # WM_NCHITTEST: Informa ao Windows que a janela e totalmente transparente ao mouse
        # Isso REMOVE o cursor de carregando/ocupado imediatamente!
        if msg == win32con.WM_NCHITTEST:
            return win32con.HTTRANSPARENT
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def create(self):
        wnd_class = win32gui.WNDCLASS()
        wnd_class.hInstance = win32gui.GetModuleHandle(None)
        wnd_class.lpszClassName = self.class_name
        wnd_class.lpfnWndProc = self._wnd_proc
        wnd_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)

        try:
            win32gui.RegisterClass(wnd_class)
        except Exception:
            pass

        width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        # WS_EX_TRANSPARENT + WS_EX_NOACTIVATE: Faz a janela nao roubar o foco do mouse
        self.hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_NOACTIVATE,
            self.class_name,
            "LiveWall Render Window",
            win32con.WS_POPUP | win32con.WS_VISIBLE,
            0, 0, width, height,
            0, 0, wnd_class.hInstance, None
        )

        logger.info(f"RenderWindow transparente criada: {self.hwnd} ({width}x{height})")
        return self.hwnd

    def destroy(self):
        if self.hwnd:
            win32gui.DestroyWindow(self.hwnd)
            self.hwnd = None