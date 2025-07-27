import os
import re
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class ScreenshotUtils:
    """Utility class for taking and managing screenshots."""

    @staticmethod
    def take_screenshot(
        driver: WebDriver,
        name: str | None = None,
        directory: str | None = None
    ) -> str:
        """
        Take a screenshot and save it to the specified directory.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            name (str | None): Optional base name for the screenshot file.
            directory (str | None): Optional directory to save the screenshot.

        Returns:
            str: Absolute path to the saved screenshot.

        Raises:
            Exception: If the screenshot cannot be saved.
        """
        try:
            screenshot_dir = directory or Config.SCREENSHOT_DIR
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = re.sub(r'\W+', '_', name) if name else "screenshot"
            filename = f"{safe_name}_{timestamp}.{Config.SCREENSHOT_FORMAT}"
            screenshot_path = os.path.join(screenshot_dir, filename)

            driver.save_screenshot(screenshot_path)
            abs_path = os.path.abspath(screenshot_path)
            logger.info(f"Screenshot saved: {abs_path}")
            return abs_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            raise

    @staticmethod
    def take_screenshot_on_failure(
        driver: WebDriver,
        test_name: str
    ) -> str:
        """
        Take a screenshot when a test fails.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            test_name (str): Name of the failing test.

        Returns:
            str: Absolute path to the saved screenshot.
        """
        failure_dir = os.path.join(Config.SCREENSHOT_DIR, "failures")
        return ScreenshotUtils.take_screenshot(driver, f"FAIL_{test_name}", failure_dir)
