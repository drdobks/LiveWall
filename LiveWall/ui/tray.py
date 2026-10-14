import pystray
from PIL import Image, ImageDraw
import threading
import logging

logger = logging.getLogger("ui.tray")

class TrayIcon:
    def __init__(self, controller):
        self.controller = controller
        self.icon = None

    def create_image(self):
        # Cria um icone para a barra de tarefas (fundo escuro com circulo azul)
        image = Image.new('RGB', (64, 64), color=(30, 30, 30))
        d = ImageDraw.Draw(image)
        d.ellipse((16, 16, 48, 48), fill=(0, 120, 215))
        return image

    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem("LiveWall Rodando", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Modo AFK (Ctrl+Shift+A)", lambda: self.controller.toggle_afk()),
            pystray.MenuItem("Icones ON/OFF (Ctrl+Shift+S)", lambda: self.controller.toggle_icons()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Sair", lambda: self.stop())
        )

        self.icon = pystray.Icon("LiveWall", self.create_image(), "LiveWall", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()
        logger.info("Icone da bandeja iniciado com sucesso.")

    def stop(self):
        logger.info("Encerrando pelo menu da bandeja...")
        if self.icon:
            self.icon.stop()
        self.controller.stop()