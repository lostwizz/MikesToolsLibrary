import logging
from MikesToolsLibrary.MyLogging.LoggerSetup import LoggerSetup


def test_get_logger_returns_logging_logger_and_preserves_name():
    logger = LoggerSetup(name="my.test.logger").get_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "my.test.logger"

def test_get_logger_returns_same_logger_instance_for_same_name():
    logger1 = LoggerSetup(name="same.name").get_logger()
    logger2 = LoggerSetup(name="same.name").get_logger()
    assert logger1 is logger2


def test_add_custom_level_registers_new_level():
    logger_setup = LoggerSetup(name="test.levels")
    # Choose a non-standard level number not used by logging
    level_name = "UNITTESTLVL"
    level_num = 42
    method_name = "unittestlvl"

    # Call the method and assert it doesn't raise
    logger_setup.add_custom_level(level_name, level_num, method_name)

    # Now verify the logging module has the new level
    assert logging.getLevelName(level_num) == level_name
    assert hasattr(logging, level_name)
    assert hasattr(logging.getLoggerClass(), method_name)


def test_add_special_levels_registers_query_level():
    logger_setup = LoggerSetup(name="test.specials")
    # Ensure some known level like QUERY (55) gets registered
    logger_setup.add_special_levels()
    assert logging.getLevelName(55) == "QUERY"