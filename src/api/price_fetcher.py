"""Binance API client for fetching BTC price data."""

import json
import threading
import websocket
import requests

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/24hr"
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@ticker"


def fetch_btc_price() -> dict | None:
    """
    Fetch BTC/USDT price and 24h change from Binance API (REST).

    Returns:
        dict with 'price' (float) and 'change_percent' (float), or None on error.
    """
    try:
        response = requests.get(
            BINANCE_API_URL,
            params={"symbol": "BTCUSDT"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return {
            "price": float(data["lastPrice"]),
            "change_percent": float(data["priceChangePercent"]),
            "high_24h": float(data["highPrice"]),
            "low_24h": float(data["lowPrice"])
        }
    except (requests.RequestException, KeyError, ValueError):
        return None


class BinanceWebSocket:
    """Real-time price updates via Binance WebSocket."""

    def __init__(self, on_price_update):
        self.on_price_update = on_price_update
        self.ws = None
        self.thread = None
        self.running = False

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            price_data = {
                "price": float(data["c"]),  # Current price
                "change_percent": float(data["P"]),  # Price change percent
                "high_24h": float(data["h"]),  # High price
                "low_24h": float(data["l"])  # Low price
            }
            self.on_price_update(price_data)
        except (json.JSONDecodeError, KeyError, ValueError):
            pass

    def _on_error(self, ws, error):
        pass

    def _on_close(self, ws, close_status_code, close_msg):
        if self.running:
            # Reconnect after 3 seconds
            threading.Timer(3.0, self.start).start()

    def _on_open(self, ws):
        pass

    def start(self):
        """Start the WebSocket connection."""
        self.running = True
        self.ws = websocket.WebSocketApp(
            BINANCE_WS_URL,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the WebSocket connection."""
        self.running = False
        if self.ws:
            self.ws.close()
