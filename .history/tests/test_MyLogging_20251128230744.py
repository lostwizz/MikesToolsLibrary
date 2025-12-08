import logging
import sys
from pathlib import Path

# Ensure `src` is on sys.path so we import the local package during testing
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from MikesToolsLibrary.MyLogging.LoggerSetup import LoggerSetup


def test_get_logger_returns_logging_logger_and_preserves_name():
    logger = LoggerSetup(name="my.test.logger").get_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "my.test.logger"

def test_get_logger_returns_same_logger_instance_for_same_name():
    logger1 = LoggerSetup(name="same.name").get_logger()
    logger2 = LoggerSetup(name="same.name").get_logger()
    assert logger1 is logger2