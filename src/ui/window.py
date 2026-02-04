"""Transparent window setup for the BTC widget."""

import tkinter as tk
from .colors import COLOR_BACKGROUND


def create_transparent_window() -> tk.Tk:
    """Create and configure a transparent, always-on-top window."""
    root = tk.Tk()
    root.title("BTC Price")

    # Remove window decorations (title bar, borders)
    root.overrideredirect(True)

    # Set window transparency (90% opacity)
    root.attributes('-alpha', 0.9)

    # Keep window always on top
    root.attributes('-topmost', True)

    # Set window size and position (top-right corner)
    window_width = 220
    window_height = 100
    screen_width = root.winfo_screenwidth()
    x_position = screen_width - window_width - 20
    y_position = 20
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Set background color
    root.configure(bg=COLOR_BACKGROUND)

    return root


class DraggableWindow:
    """Mixin to make a window draggable."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._drag_start_x = 0
        self._drag_start_y = 0

    def bind_drag_events(self, widget: tk.Widget):
        """Bind drag events to a widget."""
        widget.bind('<Button-1>', self._on_drag_start)
        widget.bind('<B1-Motion>', self._on_drag_motion)

    def _on_drag_start(self, event):
        """Record starting position for drag."""
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _on_drag_motion(self, event):
        """Move window during drag."""
        x = self.root.winfo_x() + (event.x - self._drag_start_x)
        y = self.root.winfo_y() + (event.y - self._drag_start_y)
        self.root.geometry(f"+{x}+{y}")
