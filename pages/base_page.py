from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import Config
import time
import logging

logger = logging.getLogger(__name__)

class BasePage:
    """Base class for all Page Objects in the UI automation framework."""

    def __init__(self, driver: WebDriver):
        """
        Initialize BasePage with a Selenium WebDriver.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        self.driver: WebDriver = driver

    def go_to_link(self, url: str) -> None:
        """
        Navigate browser to the specified URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)

    def wait_for_element_to_be_invisible(
        self, locator: tuple[str, str], timeout: int | float | None = None
    ) -> bool:
        """
        Wait until the element is invisible.

        Args:
            locator (tuple[str, str]): Locator tuple (By, value).
            timeout (int | float | None): Max wait time in seconds.

        Returns:
            bool: True if the element becomes invisible within the timeout.

        Raises:
            TimeoutException: If element does not become invisible in time.
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_and_get_present_element(
        self, locator: tuple[str, str], timeout: int | float | None = None
    ) -> WebElement:
        """
        Wait until element is present in the DOM.

        Args:
            locator (tuple[str, str]): Locator tuple (By, value).
            timeout (int | float | None): Max wait time in seconds.

        Returns:
            WebElement: The located element.
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_and_get_visible_element(
        self, locator: tuple[str, str], timeout: int | float | None = None
    ) -> WebElement:
        """
        Wait until element is visible.

        Args:
            locator (tuple[str, str]): Locator tuple (By, value).
            timeout (int | float | None): Max wait time in seconds.

        Returns:
            WebElement: The visible element.
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_and_get_clickable_element(
        self, locator: tuple[str, str], timeout: int | float | None = None
    ) -> WebElement:
        """
        Wait until element is visible and enabled (clickable).

        Args:
            locator (tuple[str, str]): Locator tuple (By, value).
            timeout (int | float | None): Max wait time in seconds.

        Returns:
            WebElement: The clickable element.
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_and_get_present_elements(
        self, locator: tuple[str, str], timeout: int | float | None = None
    ) -> list[WebElement]:
        """
        Wait until all matching elements are present in the DOM.

        Args:
            locator (tuple[str, str]): Locator tuple (By, value).
            timeout (int | float | None): Max wait time in seconds.

        Returns:
            list[WebElement]: List of present elements.
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def get_visible_elements(
        self, locator: tuple[str, str], timeout: int | float | None = None
    ) -> list[WebElement]:
        """
        Get all visible elements matching the locator.

        Args:
            locator (tuple[str, str]): Locator tuple (By, value).
            timeout (int | float | None): Max wait time in seconds.

        Returns:
            list[WebElement]: List of visible elements.
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        present_elements = self.wait_and_get_present_elements(locator, wait_time)
        return [element for element in present_elements if element.is_displayed()]

    def get_clickable_elements(
        self, locator: tuple[str, str], timeout: int | float | None = None
    ) -> list[WebElement]:
        """
        Get all elements matching locator that are visible, enabled, and in viewport.

        Args:
            locator (tuple[str, str]): Locator tuple (By, value).
            timeout (int | float | None): Max wait time in seconds.

        Returns:
            list[WebElement]: List of clickable elements.
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        present_elements = self.wait_and_get_present_elements(locator, wait_time)
        return [
            el for el in present_elements
            if el.is_displayed() and el.is_enabled() and self.is_element_in_viewport(el)
        ]

    def click_element(
        self, element: tuple[str, str] | WebElement, timeout: int | float | None = None
    ) -> None:
        """
        Click an element, waiting until it's clickable if a locator is given.

        Args:
            element (tuple[str, str] | WebElement): Element locator or WebElement.
            timeout (int | float | None): Wait timeout in seconds.

        Raises:
            Exception: If element cannot be clicked.
        """
        try:
            el = self.wait_and_get_clickable_element(element, timeout) if isinstance(element, tuple) else element
            el.click()
            logger.info(f"Clicked element: {el}")
        except Exception as e:
            logger.error(f"Failed to click element {element}: {str(e)}")
            raise

    def set_text_field(
        self, element: tuple[str, str] | WebElement, text: str, timeout: int | float | None = None
    ) -> None:
        """
        Clear and type into a text field, then press RETURN.

        Args:
            element (tuple[str, str] | WebElement): Element locator or WebElement.
            text (str): Text to enter.
            timeout (int | float | None): Wait timeout in seconds.

        Raises:
            Exception: If text cannot be entered.
        """
        el = self.wait_and_get_visible_element(element, timeout) if isinstance(element, tuple) else element
        try:
            el.clear()
            el.send_keys(text)
            el.send_keys(Keys.RETURN)
            logger.info(f"Sent keys '{text}' to element: {el}")
        except Exception as e:
            logger.error(f"Failed to send keys to element {el}: {str(e)}")
            raise

    def is_element_in_viewport(self, element: WebElement) -> bool:
        """
        Check if element is fully within the viewport.

        Args:
            element (WebElement): Element to check.

        Returns:
            bool: True if element is in viewport, False otherwise.
        """
        rect = self.driver.execute_script("""
            var r = arguments[0].getBoundingClientRect();
            return {left: r.left, top: r.top, right: r.right, bottom: r.bottom};
        """, element)
        window_width: int = self.driver.execute_script("return window.innerWidth;")
        window_height: int = self.driver.execute_script("return window.innerHeight;")
        return (
            rect['top'] >= 0 and
            rect['left'] >= 0 and
            rect['bottom'] <= window_height and
            rect['right'] <= window_width
        )

    def scroll(
        self,
        x_pixels: int = 0,
        y_pixels: int = 0,
        steps: int = 1,
        duration: float = 0
    ) -> None:
        """
        Scroll by specified pixels horizontally and/or vertically, optionally with steps and duration.

        Args:
            x_pixels (int): Pixels to scroll horizontally.
            y_pixels (int): Pixels to scroll vertically.
            steps (int): Steps to divide scroll.
            duration (float): Total duration in seconds.
        """
        x_per_step = x_pixels / steps
        y_per_step = y_pixels / steps
        sleep_per_step = duration / steps if steps > 0 else 0

        for _ in range(steps):
            self.driver.execute_script(f"window.scrollBy({x_per_step}, {y_per_step});")
            if sleep_per_step > 0:
                time.sleep(sleep_per_step)
        logger.info(
            f"Scrolled by ({x_pixels}, {y_pixels}) pixels over {steps} steps in {duration}s"
        )

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            str: The current URL.
        """
        return self.driver.current_url

    def get_page_title(self) -> str:
        """
        Get the current page title.

        Returns:
            str: The page title.
        """
        return self.driver.title
