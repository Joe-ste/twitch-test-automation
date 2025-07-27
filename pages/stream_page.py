from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from pages.navigation_bar import NavigationBar
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class StreamPage(BasePage):
    """Page object for a Twitch streamer page."""

    # Locators for streamer page UI elements
    VIDEO_SOURCE: tuple = (By.CSS_SELECTOR, '[data-a-target="video-ref"] video[src]')
    LOADING_SPINNER: tuple = (By.CSS_SELECTOR, ".tw-loading-spinner")
    CONTENT_CLASSIFICATION_GATE_OVERLAY: tuple = (By.CSS_SELECTOR, "[data-a-target='content-classification-gate-overlay']")
    CONTENT_CLASSIFICATION_GATE_OVERLAY_START_WATCHING_BUTTON: tuple = (By.CSS_SELECTOR, "[data-a-target='content-classification-gate-overlay-start-watching-button']")

    def __init__(self, driver: WebDriver):
        """
        Initialize StreamPage.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)
        self.url: str = Config.TWITCH_URL

    @property
    def navigation_bar(self) -> NavigationBar:
        """Return a NavigationBar page object scoped to this driver."""
        return NavigationBar(self.driver)

    def navigate_to_streamer_page(self, streamer_name: str) -> None:
        """
        Navigate to a Twitch streamer page by streamer name.

        Args:
            streamer_name (str): The Twitch username of the streamer (without slash).

        Raises:
            Exception: If navigation fails.
        """
        self.go_to_link(self.url + "/" + streamer_name.lstrip("/"))
        logger.info(f"Navigated to Twitch streamer page: {streamer_name}")

    def handle_streamer_popups(self, timeout: int = 5) -> None:
        """
        Handle popups specific to streamer pages (e.g., mature content overlays).

        Args:
            timeout (int, optional): Max wait time for popup to appear.

        Note:
            Will silently ignore if overlay does not appear.
        """
        try:
            self.wait_and_get_visible_element(self.CONTENT_CLASSIFICATION_GATE_OVERLAY, timeout)
            self.click_element(self.CONTENT_CLASSIFICATION_GATE_OVERLAY_START_WATCHING_BUTTON)
            logger.info("Content classification gate overlay handled - clicked 'Start Watching'")
        except Exception:
            logger.debug("No content classification gate overlay found.")

    def wait_for_video_load(self, timeout: int = 10) -> None:
        """
        Wait for the video player to load on the stream page.

        Args:
            timeout (int, optional): Max wait time for video load.

        Raises:
            Exception: If loading spinner does not disappear or video player does not load.
        """
        self.wait_for_element_to_be_invisible(self.LOADING_SPINNER, timeout)
        self.wait_and_get_visible_element(self.VIDEO_SOURCE, timeout)
        logger.info("Video player loaded successfully")
