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


def test_add_filter_excludes_specified_level(tmp_path):
    import io

    logfile = tmp_path / "filter.log"
    logger_setup = LoggerSetup(name="test.filter", logfile=str(logfile), level=logging.DEBUG)
    logger = logger_setup.get_logger()

    # Add a capture stream handler and set level to DEBUG
    capture_stream = io.StringIO()
    sh = logging.StreamHandler(capture_stream)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    # Ensure messages are captured without the filter
    logger.debug("debug message")
    logger.info("info message")
    out = capture_stream.getvalue()
    assert "debug message" in out
    assert "info message" in out

    # Clear the stream and add the filter for DEBUG
    capture_stream.truncate(0)
    capture_stream.seek(0)
    logger_setup.add_filter(logging.DEBUG)

    # Log again — DEBUG should be filtered out
    logger.debug("debug message")
    logger.info("info message")
    out = capture_stream.getvalue()
    assert "debug message" not in out
    assert "info message" in out