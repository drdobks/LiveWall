import win32gui
import win32con
import logging

logger = logging.getLogger("core.desktop")

def find_workerw():
    progman = win32gui.FindWindow("Progman", None)
    if not progman:
        return 0

    win32gui.SendMessageTimeout(progman, 0x052C, 0x0000000D, 0, win32con.SMTO_NORMAL, 1000)
    worker_w = None

    def enum_windows_callback(hwnd, extra):
        nonlocal worker_w
        shelldll = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
        if shelldll:
            worker_w = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)
            return False
        return True

    win32gui.EnumWindows(enum_windows_callback, None)
    return worker_w if worker_w else progman

def inject_window(target_hwnd, parent_hwnd=None):
    if not parent_hwnd:
        parent_hwnd = find_workerw()

    if parent_hwnd:
        win32gui.SetParent(target_hwnd, parent_hwnd)
        rect = win32gui.GetWindowRect(parent_hwnd)
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        win32gui.SetWindowPos(
            target_hwnd, 0, 0, 0, w, h,
            win32con.SWP_NOZORDER | win32con.SWP_SHOWWINDOW
        )
        return True
    return False

def get_desktop_icon_hwnd():
    """Localiza a lista de icones SysListView32 no Windows 10/11"""
    progman = win32gui.FindWindow("Progman", None)
    shelldll = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
    
    if not shelldll:
        def enum_cb(hwnd, extra):
            nonlocal shelldll
            found = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
            if found:
                shelldll = found
                return False
            return True
        win32gui.EnumWindows(enum_cb, None)

    if shelldll:
        listview = win32gui.FindWindowEx(shelldll, 0, "SysListView32", None)
        return listview if listview else shelldll
    return None

def toggle_desktop_icons():
    """Esconde ou mostra apenas os icones do Desktop"""
    icon_hwnd = get_desktop_icon_hwnd()
    if icon_hwnd:
        is_visible = win32gui.IsWindowVisible(icon_hwnd)
        cmd = win32con.SW_HIDE if is_visible else win32con.SW_SHOW
        win32gui.ShowWindow(icon_hwnd, cmd)
        logger.info(f"Icones do Desktop: {'OCULTOS' if is_visible else 'VISIVEIS'}")
        return not is_visible
    else:
        logger.warning("Janela de icones nao encontrada.")
        return False