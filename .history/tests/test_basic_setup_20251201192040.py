import sys
import os
import logging
import unittest
from unittest.mock import patch, MagicMock
from basic_setup import main, checkCustomLevels, showLevelInfo, checkDecorator, checkLoggerLevel, checkTypesOutput, checkMultipleArgs, displayExcludeLevel

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_basic_setup.py - Unit tests for basic_setup.py main function
"""


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)



class TestMain(unittest.TestCase):
    """Test cases for main() function"""

    @patch('basic_setup.LoggerSetup')
    @patch('basic_setup.checkCustomLevels')
    @patch('basic_setup.showLevelInfo')
    @patch('basic_setup.checkDecorator')
    @patch('basic_setup.checkLoggerLevel')
    @patch('basic_setup.checkTypesOutput')
    @patch('basic_setup.checkMultipleArgs')
    @patch('basic_setup.displayExcludeLevel')
    def test_main_calls_all_functions(self, mock_display, mock_multi, mock_types,
                                        mock_level, mock_decorator, mock_show,
                                        mock_custom, mock_logger_setup):
        """Test that main() calls all expected functions"""
        mock_logger = MagicMock()
        mock_logger_setup.return_value.get_logger.return_value = mock_logger

        main()

        mock_logger_setup.assert_called_once_with("MikesToolsLibrary", level=logging.DEBUG, logfile="MikesToolsLibrary.log")
        mock_custom.assert_called_once()
        mock_show.assert_called_once()
        mock_decorator.assert_called_once()
        mock_level.assert_called_once()
        mock_types.assert_called_once()
        mock_multi.assert_called_once()
        mock_display.assert_called_once()

    @patch('basic_setup.LoggerSetup')
    def test_main_logger_initialization(self, mock_logger_setup):
        """Test that main() initializes logger correctly"""
        mock_logger = MagicMock()
        mock_logger_setup.return_value.get_logger.return_value = mock_logger

        with patch('basic_setup.checkCustomLevels'):
            with patch('basic_setup.showLevelInfo'):
                with patch('basic_setup.checkDecorator'):
                    with patch('basic_setup.checkLoggerLevel'):
                        with patch('basic_setup.checkTypesOutput'):
                            with patch('basic_setup.checkMultipleArgs'):
                                with patch('basic_setup.displayExcludeLevel'):
                                    main()

        mock_logger_setup.assert_called_once_with(
            "MikesToolsLibrary",
            level=logging.DEBUG,
            logfile="MikesToolsLibrary.log"
        )


if __name__ == "__main__":
    unittest.main()