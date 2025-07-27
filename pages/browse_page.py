from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
from pages.navigation_bar import NavigationBar
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class BrowsePage(BasePage):
    """Page object for search functionality on Twitch Browse page."""

    SEARCH_INPUT_SELECTOR: tuple[str, str] = (By.CSS_SELECTOR, "input[data-a-target='tw-input']")
    
    def __init__(self, driver: WebDriver):
        """
        Initialize the BrowsePage object.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)
        self.url: str = Config.TWITCH_URL + "/directory"

    @property
    def navigation_bar(self) -> NavigationBar:
        """
        Return a NavigationBar page object scoped to this driver.

        Returns:
            NavigationBar: Navigation bar object for this driver.
        """
        return NavigationBar(self.driver)
    
    def find_search_input(self, timeout: int = 10) -> WebElement:
        """
        Find the search input using the primary selector.

        Args:
            timeout (int): Maximum number of seconds to wait for the input.

        Returns:
            WebElement: The search input element if found.

        Raises:
            Exception: If no search input is found.
        """
        logger.info("🔍 Looking for search input...")
        try:
            search_input = self.wait_and_get_visible_element(self.SEARCH_INPUT_SELECTOR, timeout)
            logger.info(f"Found search input using selector: {self.SEARCH_INPUT_SELECTOR}")
            return search_input
        except Exception:
            logger.error("No search input found with any selector!")
            raise Exception("No search input found on Browse page.")

    def perform_search(self, search_term: str) -> None:
        """
        Perform a search with the given term.

        Args:
            search_term (str): The term to search for.

        Raises:
            Exception: If the search cannot be performed.
        """
        search_input = self.find_search_input()
        logger.info(f"Entering search term: '{search_term}'...")
        self.set_text_field(search_input, search_term)
