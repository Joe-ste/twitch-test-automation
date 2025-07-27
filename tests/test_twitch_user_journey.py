import logging
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from utils.screenshot_utils import ScreenshotUtils as ScreenshotUtilsType
from pages.home_page import HomePage
from pages.browse_page import BrowsePage
from pages.search_results_page import SearchResultsPage
from pages.stream_page import StreamPage

logger = logging.getLogger(__name__)

class TestTwitchUserJourney:
    """
    UI Test: Simulate a typical Twitch user journey
    Steps: Browse > Search > View results > Scroll > Watch stream > Screenshot
    """

    @pytest.mark.parametrize("search_term", ["StarCraft II"], ids=["Search: StarCraft II"])
    def test_browse_search_and_watch_streamer(
        self,
        driver: WebDriver,
        screenshot_utils: ScreenshotUtilsType,
        home_page: HomePage,
        browse_page: BrowsePage,
        search_results_page: SearchResultsPage,
        stream_page: StreamPage,
        search_term: str,
    ) -> None:
        """
        Test scenario: End-to-end Twitch user workflow.
        1. Navigate to Browse page
        2. Search for a term
        3. Wait for results
        4. Scroll results
        5. Select and open a streamer
        6. Wait for stream to load
        7. Take screenshot
        """
        logger.info("Starting Twitch user journey test")

        # Step 1: Navigate to Browse
        home_page.navigate_to_home_page()
        home_page.navigation_bar.go_to_browse()
        logger.info("Navigated to Browse")

        # Step 2: Perform search
        browse_page.perform_search(search_term)
        logger.info("Search performed successfully")

        # Step 3: Wait for search results
        search_results_page.wait_for_search_results_load()
        logger.info("Search results loaded")

        # Step 4: Scroll down twice
        search_results_page.scroll_down_twice()
        logger.info("Scrolled down twice")

        # Step 5: Select and click a random streamer
        streamer_info = search_results_page.select_random_streamer()
        logger.info(f"Selected streamer: {streamer_info}")

        # Step 6: Handle popups and wait for video
        stream_page.handle_streamer_popups()
        stream_page.wait_for_video_load()
        logger.info("Streamer page loaded")

        # Step 7: Take screenshot of success state
        screenshot_path = screenshot_utils.take_screenshot(
            driver,
            name="browse_search_and_watch_streamer",
            directory="screenshots/success"
        )
        logger.info(f"Screenshot saved: {screenshot_path}")
