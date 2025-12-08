#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 22:47:27"
###############################################################################
import logging
import sys

from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels
from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter


# from .CustomFormatter import CustomFormatter
# from .CustomLevels import CustomLevels

from .ExcludeLevelFilter import ExcludeLevelFilter



# =================================================================
from typing import Callable
import inspect
import time
import traceback
from functools import wraps

def log_decorator(func: Callable) -> Callable:
    """
    A decorator to log function calls, arguments, and return values.

    This decorator logs the function name, arguments, and return value using the logger set up by CustomFormatter.
    It also handles exceptions and logs them as errors.
    :param func: The function to be decorated.
    :return: The wrapped function with logging functionality.

        Example usage:
            @log_decorator
            def my_function(arg1, arg2):
                return arg1 + arg2
                    result = my_function(1, 2)
                    # This will log the function call, arguments, and return value.
                    #
                    #   The log messages will be formatted using the CustomFormatter class.
                    #               The logger will also handle exceptions and log them as errors.
                    #               The log messages will be colored based on their severity level.
    """


    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        #logger = CustomFormatter.theLogger  # Use the logger set up by CustomFormatter
        #logger.decorator("@+@                 ")
        #logger.decorator4(f"Calling function: {func.__name__}")
        print (f"Calling function: {func.__name__}")

        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for counter, (name, value) in enumerate(
            bound.arguments.items(), start=0
        ):
            if name == "self":
                # logger.decorator2("self = <something>")
                print("self = <something>")
                continue
            # logger.decorator1(f"{counter=}")
            print(f"{counter=}")

            if isinstance(value, (list, dict)) or callable(
                getattr(value, "dump", None)
            ):
                if value is None or (
                    isinstance(value, str) and value.strip() == ""
                ):
                    logger.decorator(f"{name} is None or empty")
                elif value is None or (
                    isinstance(value, (list, dict)) and len(value) == 0
                ):
                    # logger.decorator(f"{name} is None or empty")
                    print(f"{name} is None or empty")
                else:
                    # logger.decorator2(f"{name}=")
                    # logger.decorator(value)
                    print`(f"{name}=")
                    print`(value)
            else:
                # logger.decorator(f"Argument: {name} = {value}")
                print(f"Argument: {name} = {value}")

        ##logger.decorator(args)
        # logger.decorator3(f"{kwargs=}")
        print(f"{kwargs=}")

            # logger.decorator(f"Arguments: {args}, {kwargs}")
        try:
            start_time = time.perf_counter()  # Start timing
            result = func(*args, **kwargs)
            # logger.decorator4(f"     - after Calling function: {func.__name__}")
            print(f"     - after Calling function: {func.__name__}")
            if isinstance(result, (list, dict)) or callable(
                getattr(result, "dump", None)
            ):
                if result is None or (isinstance(result, str) and result.strip() == ""):
                    # logger.decorator("result is None or empty")
                    prin("result is None or empty")
                elif result is None or (
                    isinstance(result, (list, dict)) and len(result) == 0
                ):
                    logger.decorator("result is None or Empty")
                else:
                    logger.decorator("result=")
                    #logger.decorator(result)
            else:
                logger.decorator(f"Return arg_valueue: {result}")
            logger.decorator("@-@                 ")
            end_time = time.perf_counter()  # End timing
            logger.decorator(
                f"Function {func.__name__} took {end_time - start_time:.6f} seconds"
            )
            print("^")
            return result
        except Exception as e:
            logger.decorator_error(f"Exception in {func.__name__}: {e}")
            logger.decorator_error(traceback.format_exc())
            logger.decorator("@e@                 ")
            raise
    return wrapper




class LoggerSetup:
    """
    Unified logger setup:
    - Console handler with CustomFormatter (color, pretty-print)
    - File handler with plain text logs
    - Support for custom levels via add_custom_level
    - Optional filters (exclude certain levels)
    """

    # -----------------------------------------------------------------
    def __init__(
        self,
        name: str = "MikesToolsLibrary",
        level: int = logging.DEBUG,
        logfile: str = "app.log",
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Avoid duplicate handlers if re-instantiated
        if not self.logger.handlers:
            # Console handler
            # console_handler = logging.StreamHandler(sys.stdout)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            # console_handler.setFormatter(CustomFormatter("%(name)s | %(levelname)s | %(message)s"))
            # console_formatter = logging.Formatter(
            #     CustomFormatter.DEFAULT_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"
            # )

            console_formatter = CustomFormatter(CustomFormatter.DEFAULT_FORMAT, datefmt="%H:%M:%S")
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            ######
            # File handler
            file_handler = logging.FileHandler(logfile, encoding="utf-8")
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                CustomFormatter.DEFAULT_FILE_FORMAT,
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)



    # -----------------------------------------------------------------
    @staticmethod
    def add_SpecialLevels(self):
        if self.lvls is None:
            self.lvls = CustomLevels()
        self.lvls.setupLogger()


    # -----------------------------------------------------------------
    @staticmethod
    def add_level(self, level_name: str, level_num: int, method_name: str = None):
        """
        Add a custom logging level.
        :param level_name: Name of the logging level.
        :param level_num: Numeric value of the logging level.
        :param method_name: Optional method name for logger.
        """

        lvls = CustomLevels()
        lvls.add_log_level(level_name, level_num, method_name)


    # -----------------------------------------------------------------
    def get_logger(self) -> logging.Logger:
        return self.logger

    # -----------------------------------------------------------------
    @log_decorator
    def add_custom_level(level_name, level_num, method_name=None):
        return CustomLevels.add_log_level(level_name, level_num, method_name)


    # -----------------------------------------------------------------
    def add_filter(self, level_to_exclude: int):
        """
        Add a filter to exclude a specific level from console/file output.
        """
        for handler in self.logger.handlers:
            handler.addFilter(ExcludeLevelFilter(level_to_exclude))


