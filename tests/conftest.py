import pytest
import logging
import os
from typing import Generator
from selenium.webdriver.remote.webdriver import WebDriver

from utils.webdriver_factory import WebDriverFactory
from utils.screenshot_utils import ScreenshotUtils as ScreenshotUtilsType
from config.config import Config

from pages.home_page import HomePage as HomePageType
from pages.stream_page import StreamPage as StreamPageType
from pages.browse_page import BrowsePage as BrowsePageType
from pages.search_results_page import SearchResultsPage as SearchResultsPageType

def pytest_configure(config):
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/test_execution.log"
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.hasHandlers():
        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"
        ))
        root_logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"
        ))
        root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def test_session() -> Generator[None, None, None]:
    logger.info("==== Test session start ====")
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(Config.REPORT_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    yield
    logger.info("==== Test session completed ====")

@pytest.fixture(scope="function")
def driver(request) -> Generator[WebDriver, None, None]:
    driver = None
    test_name = request.node.name
    try:
        driver = WebDriverFactory.get_driver()
        logger.info(f"WebDriver created for test: {test_name}")
        yield driver
    except Exception as e:
        logger.error(f"Driver error in test {test_name}: {e}")
        if driver:
            try:
                ScreenshotUtilsType.take_screenshot_on_failure(driver, test_name)
            except Exception as screenshot_error:
                logger.error(f"Failed to take error screenshot: {str(screenshot_error)}")
        raise
    finally:
        if driver:
            try:
                driver.quit()
                logger.info(f"WebDriver closed for test: {test_name}")
            except Exception as e:
                logger.warning(f"Error closing WebDriver for test {test_name}: {e}")

@pytest.fixture(scope="function")
def home_page(driver: WebDriver) -> HomePageType:
    return HomePageType(driver)

@pytest.fixture(scope="function")
def stream_page(driver: WebDriver) -> StreamPageType:
    return StreamPageType(driver)

@pytest.fixture(scope="function")
def browse_page(driver: WebDriver) -> BrowsePageType:
    return BrowsePageType(driver)

@pytest.fixture(scope="function")
def search_results_page(driver: WebDriver) -> SearchResultsPageType:
    return SearchResultsPageType(driver)

@pytest.fixture(scope="function")
def screenshot_utils() -> ScreenshotUtilsType:
    return ScreenshotUtilsType

def pytest_runtest_logreport(report):
    if report.when == "call":
        if report.passed:
            logger.info(f"Test PASSED: {report.nodeid}")
        elif report.failed:
            logger.error(f"Test FAILED: {report.nodeid}")
            if report.longrepr:
                logger.error(f"Failure details: {report.longrepr}")
        elif report.skipped:
            logger.warning(f"Test SKIPPED: {report.nodeid}")
