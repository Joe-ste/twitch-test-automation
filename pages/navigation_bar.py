from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class NavigationBar(BasePage):
    """Page object for Twitch navigation bar actions."""

    CREATOR_BTN: tuple = (By.CSS_SELECTOR, "a[href='/']")
    BROWSE_BTN: tuple = (By.CSS_SELECTOR, "a[href='/directory']")
    ACTIVITY_BTN: tuple = (By.CSS_SELECTOR, "a[href='/activity']")
    PROFILE_BTN: tuple = (By.CSS_SELECTOR, "a[href='/home']")

    def __init__(self, driver: WebDriver):
        """
        Initialize NavigationBar.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        super().__init__(driver)

    def go_to_creator(self) -> None:
        """Navigate to creator page."""
        self.click_element(self.CREATOR_BTN)

    def go_to_browse(self) -> None:
        """Navigate to browse page."""
        self.click_element(self.BROWSE_BTN)

    def go_to_activity(self) -> None:
        """Navigate to activity page."""
        self.click_element(self.ACTIVITY_BTN)

    def go_to_profile(self) -> None:
        """Navigate to profile page."""
        self.click_element(self.PROFILE_BTN)
