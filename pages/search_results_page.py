from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from urllib.parse import quote_plus
from pages.base_page import BasePage
from pages.navigation_bar import NavigationBar
from config.config import Config
import logging
import random

logger = logging.getLogger(__name__)

class SearchResultsPage(BasePage):
    """Page object for search results page on Twitch."""

    STREAMER_CARD: tuple = (By.CSS_SELECTOR, "button[class*='ScCoreLink'][class*='tw-link']")
    STREAM_TITLE: tuple = (By.CSS_SELECTOR, 'p[title]')

    def __init__(self, driver: WebDriver):
        """
        Initialize SearchResultsPage.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)
        self.url: str = Config.TWITCH_URL + "/search?term="

    @property
    def navigation_bar(self) -> NavigationBar:
        """Return a NavigationBar page object scoped to this driver."""
        return NavigationBar(self.driver)

    def navigate_to_search_page(self, search_term: str) -> None:
        """
        Navigate to Twitch search results page for a term.

        Args:
            search_term (str): The search keyword.
        """
        encoded_term = quote_plus(search_term)
        self.go_to_link(self.url + encoded_term)
        logger.info("Navigated to Twitch search page")

    def wait_for_search_results_load(self, timeout: int = 15) -> None:
        """
        Wait for search results to load completely.

        Args:
            timeout (int): Maximum time to wait in seconds.

        Raises:
            Exception: If search results don't load within the timeout.
        """
        self.wait_and_get_visible_element(self.STREAMER_CARD, timeout)
        logger.info("Search results loaded")

    def scroll_down_twice(self) -> None:
        """
        Scroll down twice as specified in requirements.
        """
        self.scroll(0, 800, 2, 2)

    def get_available_streamers(self) -> List[WebElement]:
        """
        Get all visible streamer cards on the page.

        Returns:
            List[WebElement]: List of clickable streamer card elements.

        Raises:
            Exception: If no streamer cards are found.
        """
        button_elements = self.get_clickable_elements(self.STREAMER_CARD)
        if not button_elements:
            raise Exception("No streamer cards found on the page")
        logger.info(f"Found {len(button_elements)} clickable button elements")
        return button_elements

    def get_streamer_info(self, streamer: WebElement) -> Dict[str, str]:
        """
        Get streamer information.

        Args:
            streamer (WebElement): Streamer card WebElement.

        Returns:
            Dict[str, str]: Information dictionary (currently only stream_title).
        """
        stream_title = streamer.find_element(*self.STREAM_TITLE).text
        return {"stream_title": stream_title}

    def select_random_streamer(self) -> Dict[str, str]:
        """
        Select a random streamer from the available ones and click it.

        Returns:
            Dict[str, str]: Streamer information.

        Raises:
            Exception: If no streamers found or clicking fails.
        """
        streamers = self.get_available_streamers()
        selected_streamer = random.choice(streamers)
        streamer_info = self.get_streamer_info(selected_streamer)
        try:
            selected_streamer.click()
            logger.info(f"Selected streamer: {streamer_info}")
            return streamer_info
        except Exception as e:
            logger.error(f"Failed to click on streamer: {str(e)}")
            raise
