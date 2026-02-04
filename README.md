# BTC Price Widget

A lightweight, transparent Windows widget displaying real-time BTC/USDT price.

![Widget Preview](https://img.shields.io/badge/BTC-Real--Time-orange)

## Features

- Real-time price updates via Binance WebSocket
- 24-hour price change percentage (color-coded green/red)
- 24-hour high/low prices
- Transparent, always-on-top window
- Draggable (click anywhere to move)
- Right-click to exit
- Auto-start on Windows boot

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Auto-Start

Enable auto-start on Windows boot:
```bash
python autostart.py --add
```

Disable auto-start:
```bash
python autostart.py --remove
```

Check status:
```bash
python autostart.py --status
```

## Requirements

- Python 3.10+
- Windows OS
- Internet connection

## Dependencies

- `requests` - Initial price fetch
- `websocket-client` - Real-time updates
