import logging
import pytest
from unittest.mock import MagicMock, patch
from MikesToolsLibrary.MyLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.examples.basic_setup import checkCustomLevels

@pytest.fixture
def mock_logger(monkeypatch):
    # Create a mock logger with all expected methods
    logger = MagicMock(spec=logging.Logger)
    logger.blkonyk = MagicMock()
    logger.notice = MagicMock()
    # Patch the global 'logger' in the module under test
    monkeypatch.setattr("MikesToolsLibrary.examples.basic_setup.logger", logger)
    return logger

@pytest.fixture
def mock_logger_setup(monkeypatch):
    # Patch LoggerSetup.add_level and add_special_levels
    monkeypatch.setattr(LoggerSetup, "add_level", MagicMock())
    monkeypatch.setattr(LoggerSetup, "add_special_levels", MagicMock())

def test_checkCustomLevels_calls_logger_methods(mock_logger, mock_logger_setup):
    checkCustomLevels()
    # Check info called for process complete
    mock_logger.info.assert_any_call("Process complete ✓ — all good 🚀")
    # Check custom level and special levels added
    LoggerSetup.add_level.assert_called_with("NOTICE", 15, "\x1b[1;35;40m", "‼")
    LoggerSetup.add_special_levels.assert_called_with(mock_logger)
    # Check all log methods called
    mock_logger.blkonyk.assert_called_once_with("blkonyk message here")
    mock_logger.debug.assert_called_once_with("Debugging details")
    mock_logger.info.assert_any_call("Info message")
    mock_logger.warning.assert_called_once_with("Warning message")
    mock_logger.error.assert_called_once_with("Error occurred")
    mock_logger.critical.assert_called_once_with("Critical issue")
    assert mock_logger.notice.call_count == 2
    mock_logger.notice.assert_any_call("This is a NOTICE message-a")
    mock_logger.notice.assert_any_call("This is a NOTICE message-b")