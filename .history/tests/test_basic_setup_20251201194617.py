import logging
import pytest
from MikesToolsLibrary.MyLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.MyLogging import FormatMode
from MikesToolsLibrary.MyLogging.log_decorator import log_decorator



import logging
import pytest


@pytest.fixture(autouse=True)
def reset_logger_state():
    LoggerSetup.reset_state()
    yield
    LoggerSetup.reset_state()


@pytest.fixture(autouse=True)
def reset_logging():
    """
    Reset logging state before each test to avoid global leakage.
    """
    # Remove all handlers from root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Reset custom levels if they were added
    for level_name in list(logging._nameToLevel.keys()):
        if level_name not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]:
            logging._nameToLevel.pop(level_name, None)

    # Reset loggerDict (optional, clears custom loggers)
    logging.Logger.manager.loggerDict.clear()

    yield


@pytest.fixture(autouse=True)
def logger():
    """Fixture to create a fresh logger for each test."""
    return LoggerSetup("TestLogger", level=logging.DEBUG).get_logger()

def test_custom_levels(logger):
    # Add a custom level
    LoggerSetup.add_level("NOTICE", 15, "\x1b[1;35;40m", "‼")
    LoggerSetup.add_special_levels(logger)

    # Verify the level exists
    assert logging._nameToLevel["NOTICE"] == 15
    # Verify logger has the new method
    assert hasattr(logger, "notice")

def test_exclude_level(caplog, logger):

    LoggerSetup.add_level("NOTICE", 15)
    LoggerSetup.add_special_levels(logger)

    with caplog.at_level("NOTICE"):
        logger.notice("test message")
    assert "test message" in caplog.text


    # Initially NOTICE should be enabled
    assert logger.isEnabledFor(logging._nameToLevel["NOTICE"])

    # Exclude NOTICE from console
    LoggerSetup.addLevelExclude(logging._nameToLevel["NOTICE"], FormatMode.CONSOLE)
    filters = LoggerSetup.showExcludeLevelFilter()
    assert logging._nameToLevel["NOTICE"] in filters.get(FormatMode.CONSOLE, [])

def test_decorator_function(logger):
    @log_decorator
    def sample(a, b):
        return a + b

    result = sample(2, 3)
    assert result == 5

def test_multiple_args(logger):
    # Just check that logger methods accept multiple args without crashing
    logger.info("Message", "a", "b", "c")
    assert logger.isEnabledFor(logging.INFO)