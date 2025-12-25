#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_LoggerSetup.py

Simple tests for LoggerSetup class.
"""

import logging
import tempfile
import os
from pathlib import Path

import pytest

from collections import defaultdict

# Import the module to test
from MikesToolsLibrary.MikesLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.MikesLogging.LoggingMode import LoggingMode
from MikesToolsLibrary.MikesLogging.ExcludeLevelFilter import ExcludeLevelFilter


def reset_logging_state():
    """Reset global logging state for tests."""
    # Clear handlers from any existing logger
    if LoggerSetup._logger:
        LoggerSetup._logger.handlers.clear()
    LoggerSetup._logger = None
    ExcludeLevelFilter.Filters = defaultdict(set)
    ExcludeLevelFilter._instance = None


def test_logger_setup_instantiation():
    """Test that LoggerSetup can be instantiated without errors."""
    reset_logging_state()

    # Create a temporary log file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        logfile = tmp.name

    try:
        setup = LoggerSetup(
            name="TestLogger",
            level=logging.DEBUG,
            logfile=logfile,
            modes=LoggingMode.CONSOLE
        )
        assert setup.logger is not None
        assert setup.logger.name == "TestLogger"
        assert setup.logger.level == logging.DEBUG
        assert len(setup.logger.handlers) > 0  # Should have at least console handler
        print("✓ LoggerSetup instantiation test passed")
    finally:
        try:
            os.unlink(logfile)
        except PermissionError:
            pass  # File still open by handler


def test_get_logger():
    """Test the get_logger class method."""
    # Reset singleton for clean test
    LoggerSetup._logger = None

    logger1 = LoggerSetup.get_logger("TestGetLogger")
    logger2 = LoggerSetup.get_logger("TestGetLogger")

    assert logger1 is logger2  # Should be the same instance (singleton)
    assert logger1.name == "TestGetLogger"
    print("✓ get_logger singleton test passed")


def test_turn_off_level():
    """Test turning off a log level."""
    # Reset singleton
    LoggerSetup._logger = None

    logger = LoggerSetup.get_logger("TestTurnOff")

    # Initially, DEBUG should be logged
    assert logger.isEnabledFor(logging.DEBUG)

    # Turn off DEBUG for console
    LoggerSetup.turnOffLevel(logging.DEBUG, LoggingMode.CONSOLE)

    x = LoggerSetup.showExcludeLevelFilter()

    print(f"--- enabled filters --- {x=} {x['ALL']}")

    # Assert that the dictionary contains 'ALL': [10]
    assert 'ALL' in x
    assert x['ALL'] == [10]


    # Check that the filter was applied (this is basic; real test would need more setup)
    # For simplicity, just check no exception was raised
    print("✓ turnOffLevel test passed (no exceptions)")


def test_include_username_and_ip():
    """Test including username and IP in logs."""
    # Reset singleton
    LoggerSetup._logger = None

    logger = LoggerSetup.get_logger("TestUserIP")

    # This should add extra fields; test that it runs without error
    LoggerSetup.includeUserNameAndIP("TestUser", "127.0.0.1")

    # Log a message to ensure it works
    logger.info("Test message with user/IP")



    assert False
    print("✓ includeUserNameAndIP test passed")


def test_show_all_levels():
    """Test showing all levels."""
    # Reset singleton
    LoggerSetup._logger = None

    logger = LoggerSetup.get_logger("TestShowLevels")

    # This should print levels; just check no exception
    LoggerSetup.show_all_levels()
    print("✓ show_all_levels test passed")


@pytest.mark.skip(reason="Not implemented yet - need to test SMTP logging")
def test_smtp_logging():
    """Test SMTP handler setup (not implemented yet)."""
    # This test is skipped until SMTP logging is fully tested
    pass


def test_file_logging_setup():
    """Test file handler setup."""
    # Reset singleton
    LoggerSetup._logger = None

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        logfile = tmp.name

    try:
        setup = LoggerSetup(
            name="TestFileLogger",
            modes=LoggingMode.FILE,
            logfile=logfile
        )
        assert setup.logger is not None
        # Check that file handler was added
        file_handlers = [h for h in setup.logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) == 1
        assert file_handlers[0].baseFilename == logfile
        print("✓ File logging setup test passed")
    finally:
        logging.shutdown()   # Close handlers before deleting
        os.unlink(logfile)


def test_rotating_file_setup():
    """Test rotating file handler setup."""
    # Reset singleton
    LoggerSetup._logger = None

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        logfile = tmp.name

    try:
        setup = LoggerSetup(
            name="TestRotatingLogger",
            modes=LoggingMode.ROTATINGFN,
            logfile=logfile,
            maxBytes=1000,
            backupCount=2
        )
        assert setup.logger is not None
        # Check for RotatingFileHandler
        from logging.handlers import RotatingFileHandler
        rotating_handlers = [h for h in setup.logger.handlers if isinstance(h, RotatingFileHandler)]
        assert len(rotating_handlers) == 1
        assert rotating_handlers[0].maxBytes == 1000
        assert rotating_handlers[0].backupCount == 2
        print("✓ Rotating file setup test passed")
    finally:
        logging.shutdown()  # Close handlers before deleting
        os.unlink(logfile)


def test_turn_off_range():
    """Test turning off a range of levels."""
    reset_logging_state()

    logger = LoggerSetup.get_logger("TestRange")

    # Turn off levels 20-30 for ALL
    LoggerSetup.turnOffRange(20, 31, LoggingMode.ALL)

    filters = LoggerSetup.showExcludeLevelFilter()
    print(f" {filters=}")
    # Should have levels 20-30 in ALL
    excluded = list(range(20, 31))  # 20 to 30 inclusive
    print (f" {excluded=}")

    assert set(filters.get('CONSOLE', [])) == set(excluded)
    assert set(filters.get('ROTATINGFN', [])) == set(excluded)
    assert set(filters.get('TIMEDROTATOR', [])) == set(excluded)
    assert set(filters.get('SMTP', [])) == set(excluded)
    assert set(filters.get('FILE', [])) == set(excluded)
    print("✓ turnOffRange test passed")


def test_force_rollover():
    """Test force rollover for rotating handlers."""
    reset_logging_state()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        logfile = tmp.name

    try:
        setup = LoggerSetup(
            name="TestRollover",
            modes=LoggingMode.ROTATINGFN,
            logfile=logfile
        )
        # Force rollover
        LoggerSetup.force_rollover(LoggingMode.ROTATINGFN)
        # Just check no exception; real test would check file rotation
        print("✓ force_rollover test passed")
    finally:
        logging.shutdown()
        os.unlink(logfile)


def test_show_color_sampler():
    """Test showing color sampler (just check no exception)."""
    # Reset singleton
    LoggerSetup._logger = None

    LoggerSetup.get_logger("TestColor")
    LoggerSetup.showColorSampler()
    print("✓ showColorSampler test passed")


if __name__ == "__main__":
    test_logger_setup_instantiation()
    test_get_logger()
    test_turn_off_level()
    test_include_username_and_ip()
    test_show_all_levels()
    test_file_logging_setup()
    test_rotating_file_setup()
    test_turn_off_range()
    test_force_rollover()
    test_show_color_sampler()
    print("\nAll tests passed! 🎉")