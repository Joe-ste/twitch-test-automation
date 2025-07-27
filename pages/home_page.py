from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from pages.navigation_bar import NavigationBar
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """Page object for Twitch homepage."""


    def __init__(self, driver: WebDriver):
        """
        Initialize the HomePage object.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)
        self.url:str = Config.TWITCH_URL

    def navigate_to_home_page(self) -> None:
        """
        Navigate to Twitch homepage.
        """
        self.go_to_link(self.url)
        logger.info("Navigated to Twitch homepage.")

    @property
    def navigation_bar(self) -> NavigationBar:
        """
        Return a NavigationBar page object scoped to this driver.

        Returns:
            NavigationBar: The navigation bar object.
        """
        return NavigationBar(self.driver)
