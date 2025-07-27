from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class WebDriverFactory:
    """Factory class for creating and configuring Selenium WebDriver instances."""

    @staticmethod
    def get_driver(
        browser_name: str | None = None,
        headless: bool | None = None,
        mobile_device: str | None = None
    ) -> webdriver.Chrome:
        """
        Create and configure a Chrome WebDriver instance with optional mobile emulation.

        Args:
            browser_name (str, optional): Browser name ("chrome" only supported).
            headless (bool, optional): Whether to run browser in headless mode.
            mobile_device (str, optional): Mobile device name for Chrome emulation (e.g., "iPhone 12").

        Returns:
            webdriver.Chrome: Configured Chrome WebDriver instance.

        Raises:
            ValueError: If unsupported browser_name is specified.
        """
        browser_name = browser_name or Config.BROWSER
        headless = headless if headless is not None else Config.HEADLESS
        mobile_device = mobile_device or Config.MOBILE_DEVICE

        if browser_name.lower() == "chrome":
            return WebDriverFactory._create_chrome_driver(headless, mobile_device)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    @staticmethod
    def _create_chrome_driver(headless: bool, mobile_device: str) -> webdriver.Chrome:
        """
        Create a Chrome driver with optional mobile device emulation.

        Args:
            headless (bool): Headless mode.
            mobile_device (str): Chrome device emulation name, e.g., "iPhone 12".

        Returns:
            webdriver.Chrome: Chrome driver instance.
        """
        options = Options()
        if mobile_device:
            options.add_experimental_option("mobileEmulation", {"deviceName": mobile_device})

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        if headless:
            options.add_argument("--headless=new")  # Chrome 109+; use "--headless" for legacy

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        logger.info(f"Chrome driver created successfully (mobile emulation: {mobile_device})")
        return driver
