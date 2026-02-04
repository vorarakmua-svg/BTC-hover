"""Main BTC Widget application class."""

import tkinter as tk
from .api.price_fetcher import fetch_btc_price, BinanceWebSocket
from .ui.window import create_transparent_window, DraggableWindow
from .ui.colors import COLOR_BACKGROUND, COLOR_PRICE_TEXT, get_change_color


class BTCWidget:
    """A transparent widget displaying real-time BTC price."""

    def __init__(self):
        self.root = create_transparent_window()
        self.draggable = DraggableWindow(self.root)
        self.pending_data = None

        self._create_ui()
        self._bind_events()

        # Load initial price via REST API
        self._load_initial_price()

        # Start WebSocket for real-time updates
        self.ws = BinanceWebSocket(self._on_price_update)
        self.ws.start()

        # Check for pending updates from WebSocket
        self._check_updates()

    def _create_ui(self):
        """Create the widget UI elements."""
        # Main container frame
        self.frame = tk.Frame(self.root, bg=COLOR_BACKGROUND)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Price row (price + percentage on same line)
        self.price_row = tk.Frame(self.frame, bg=COLOR_BACKGROUND)
        self.price_row.pack(anchor="w")

        # Price display
        self.price_label = tk.Label(
            self.price_row,
            text="Loading...",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_PRICE_TEXT,
            bg=COLOR_BACKGROUND
        )
        self.price_label.pack(side=tk.LEFT)

        # Percentage change display
        self.change_label = tk.Label(
            self.price_row,
            text="",
            font=("Segoe UI", 11),
            fg=COLOR_PRICE_TEXT,
            bg=COLOR_BACKGROUND
        )
        self.change_label.pack(side=tk.LEFT, padx=(8, 0))

        # 24h High/Low display
        self.highlow_label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI", 9),
            fg="#888888",
            bg=COLOR_BACKGROUND
        )
        self.highlow_label.pack(anchor="w")

    def _bind_events(self):
        """Bind mouse and keyboard events."""
        # Make window draggable by clicking anywhere
        for widget in [self.root, self.frame, self.price_row,
                       self.price_label, self.change_label, self.highlow_label]:
            self.draggable.bind_drag_events(widget)

        # Right-click context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Exit", command=self._exit)

        self.root.bind('<Button-3>', self._show_context_menu)
        self.frame.bind('<Button-3>', self._show_context_menu)

    def _show_context_menu(self, event):
        """Display the right-click context menu."""
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def _load_initial_price(self):
        """Load initial price via REST API."""
        data = fetch_btc_price()
        if data:
            self._display_price(data)

    def _on_price_update(self, data):
        """Callback for WebSocket price updates (called from another thread)."""
        self.pending_data = data

    def _check_updates(self):
        """Check for pending WebSocket updates and apply them (runs on main thread)."""
        if self.pending_data:
            self._display_price(self.pending_data)
            self.pending_data = None
        self.root.after(50, self._check_updates)  # Check every 50ms

    def _display_price(self, data):
        """Update the display with new price data."""
        price = data["price"]
        change = data["change_percent"]
        high_24h = data["high_24h"]
        low_24h = data["low_24h"]

        # Format price with commas
        price_text = f"${price:,.2f}"
        change_color = get_change_color(change)
        self.price_label.config(text=price_text, fg=change_color)

        # Format and color the change percentage
        sign = "+" if change >= 0 else ""
        change_text = f"{sign}{change:.2f}%"
        self.change_label.config(text=change_text, fg=change_color)

        # Update 24h high/low
        highlow_text = f"H: ${high_24h:,.0f}  L: ${low_24h:,.0f}"
        self.highlow_label.config(text=highlow_text)

    def _exit(self):
        """Clean up and exit."""
        self.ws.stop()
        self.root.quit()

    def run(self):
        """Start the widget main loop."""
        self.root.mainloop()
