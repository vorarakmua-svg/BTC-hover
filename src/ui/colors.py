"""Color constants for the BTC widget."""

COLOR_POSITIVE = "#00FF00"  # Green for positive change
COLOR_NEGATIVE = "#FF4444"  # Red for negative change
COLOR_NEUTRAL = "#FFFFFF"   # White for zero/neutral
COLOR_BACKGROUND = "#1a1a1a"  # Dark background
COLOR_PRICE_TEXT = "#FFFFFF"  # White for price text


def get_change_color(change_percent: float) -> str:
    """Return appropriate color based on price change percentage."""
    if change_percent > 0:
        return COLOR_POSITIVE
    elif change_percent < 0:
        return COLOR_NEGATIVE
    return COLOR_NEUTRAL
