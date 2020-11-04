import pytest
from syrupy.extensions.image import PNGImageSnapshotExtension


#
# Skip slow tests (marked with pytest.mark.slow) by default
# Copied from https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
#


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


#
# Configure splinter for browser tests
#


@pytest.fixture(scope="session")
def splinter_headless():
    return True


@pytest.fixture(scope="session")
def splinter_screenshot_getter_png():
    def getter(browser, path):
        browser.full_screen()
        browser.driver.save_screenshot(path)

    return getter


@pytest.fixture(scope="session")
def splinter_webdriver():
    return "chrome"


#
# Create syrupy extension for easy visual regression tests
#


class WebdriverBrowserScreenshotSyrupyExtension(PNGImageSnapshotExtension):
    def diff_lines(self, serialized_data, snapshot_data):
        # diffing images as binary data takes a long time and isn't useful,
        # don't do it
        yield "images differ"

    def serialize(self, browser, **kwargs):
        orig_window_size = browser.driver.get_window_size()
        browser.full_screen()
        screenshot = browser.driver.get_screenshot_as_png()
        browser.recover_screen(orig_window_size)
        return super().serialize(screenshot)


@pytest.fixture
def snapshot_browser_screenshot(snapshot):
    return snapshot.use_extension(WebdriverBrowserScreenshotSyrupyExtension)
