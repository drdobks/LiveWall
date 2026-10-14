"""Abstract base class for all wallpaper renderers."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseRenderer(ABC):
    """Base interface for wallpaper renderers.

    Each renderer displays a specific type of wallpaper content
    (video, image, shader, etc.) inside a given Win32 window handle.
    """

    def __init__(self, hwnd: int) -> None:
        """Initialise the renderer.

        Args:
            hwnd: Win32 window handle to render into.
        """
        self._hwnd = hwnd
        self._playing = False
        self._current_file: Optional[str] = None

    # -- lifecycle -----------------------------------------------------------

    @abstractmethod
    def start(self, filepath: str) -> None:
        """Begin rendering the given wallpaper file.

        Args:
            filepath: Path to the wallpaper asset.
        """
        ...

    @abstractmethod
    def stop(self) -> None:
        """Stop rendering and release resources."""
        ...

    @abstractmethod
    def pause(self) -> None:
        """Pause rendering (e.g., freeze video frame)."""
        ...

    @abstractmethod
    def resume(self) -> None:
        """Resume rendering after a pause."""
        ...

    # -- properties ----------------------------------------------------------

    @property
    def is_playing(self) -> bool:
        """Whether the renderer is actively playing."""
        return self._playing

    @property
    def current_file(self) -> Optional[str]:
        """Path of the currently loaded wallpaper, or *None*."""
        return self._current_file

    # TODO: Phase 2 -- add set_volume(), set_speed()
    # TODO: Phase 3 -- add set_uniform() for shader parameters
