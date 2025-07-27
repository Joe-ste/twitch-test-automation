import os
from dotenv import load_dotenv

# Load environment variables from a .env file, if present
load_dotenv()

class Config:
    """Configuration class for test automation framework."""

    # --- Base URLs ---
    TWITCH_URL: str = "https://www.twitch.tv"
    
    # --- Browser Configuration ---
    BROWSER: str = os.getenv("BROWSER", "chrome").strip()
    HEADLESS: bool = os.getenv("HEADLESS", "true").strip().lower() == "true"
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10").strip())
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30").strip())

    # --- Mobile Emulator Configuration ---
    # Must match Chrome built-in device names, e.g., "iPhone X", "iPhone 12", "Pixel 5"
    MOBILE_DEVICE: str = os.getenv("MOBILE_DEVICE", "iPhone X").strip()

    # --- Screenshot Configuration ---
    SCREENSHOT_DIR: str = os.getenv("SCREENSHOT_DIR", "screenshots").strip()
    SCREENSHOT_FORMAT: str = os.getenv("SCREENSHOT_FORMAT", "png").strip()
    
    # --- Wait Configuration ---
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10").strip())
    POLLING_FREQUENCY: float = float(os.getenv("POLLING_FREQUENCY", "0.5").strip())
    
    # --- Report Configuration ---
    REPORT_DIR: str = os.getenv("REPORT_DIR", "reports").strip()

    # --- Add any other configs as needed ---