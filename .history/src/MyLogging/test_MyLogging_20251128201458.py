import runpy
import logging
from pathlib import Path

def _module_globals():
    # Locate MyLogging.py next to this test file
    path = Path(__file__).resolve().parent / "MyLogging.py"
    return runpy.run_path(str(path), init_globals={"Logger": logging.Logger})

def test_get_logger_returns_logging_logger_and_preserves_name(capsys):
    mg = _module_globals()
    # capture import-time prints
    captured = capsys.readouterr()
    assert "mike was here" in captured.out

    get_logger = mg["get_logger"]
    logger = get_logger("my.test.logger")
    captured = capsys.readouterr()  # capture prints from function call
    assert "mike was here 2" in captured.out

    assert isinstance(logger, logging.Logger)
    assert logger.name == "my.test.logger"

def test_get_logger_returns_same_logger_instance_for_same_name():
    mg = _module_globals()
    get_logger = mg["get_logger"]
    logger1 = get_logger("same.name")
    logger2 = get_logger("same.name")
    assert logger1 is logger2