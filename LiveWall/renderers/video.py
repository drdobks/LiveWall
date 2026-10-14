import mpv
import logging
import os

logger = logging.getLogger("renderers.video")

class VideoRenderer:
    def __init__(self, hwnd, file_path):
        self.hwnd = hwnd
        self.file_path = os.path.abspath(file_path)
        self.player = None
        self._init_player()

    def _init_player(self):
        try:
            # Configura o MPV para renderizar dentro da Janela do Windows (HWND)
            # Otimizado para NVIDIA GTX 1070 (Aceleração por Hardware D3D11)
            self.player = mpv.MPV(
                wid=str(self.hwnd),
                vo="gpu",
                gpu_api="d3d11",
                hwdec="auto",
                loop_file="inf",
                keep_open=True
            )
            logger.info(f"MPV Player inicializado na janela: {self.hwnd}")
        except Exception as e:
            logger.error(f"Erro ao inicializar MPV: {e}")

    def play(self):
        """Inicia a reproducao do video"""
        if self.player and os.path.exists(self.file_path):
            logger.info(f"Reproduzindo video: {self.file_path}")
            self.player.play(self.file_path)
        else:
            logger.error(f"Arquivo de video nao encontrado: {self.file_path}")

    def pause(self):
        """Pausa o video (economiza GPU/CPU)"""
        if self.player:
            self.player.pause = True
            logger.info("Video pausado.")

    def resume(self):
        """Retoma a reproducao do video"""
        if self.player:
            self.player.pause = False
            logger.info("Video retomado.")

    def stop(self):
        """Para o player e libera a GPU"""
        if self.player:
            try:
                self.player.terminate()
            except Exception:
                pass
            self.player = None
            logger.info("Video parado.")