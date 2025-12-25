#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py




"""
__version__ = "0.1.2.00322-322-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-13 20:44:03"
###############################################################################


# =================================================================
from typing import Callable
import sys
import inspect
import time
import traceback
from functools import wraps
import logging

# import MikesToolsLibrary.MyLogging.LoggerSetup as LoggerSetup


###############################################################################
def log_decorator(func) -> None:
    # from typing import TYPE_CHECKING
    # if TYPE_CHECKING:
    #     from MikesToolsLibrary.MyLogging.LoggerSetup import LoggerSetup


    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> None:

        # logger = LoggerSetup.get_logger("MikesToolsLibrary")
        logger = logging.getLogger("MikesToolsLibrary")

        logger.decorator("@+@                 ")
        logger.decorator(f"Calling function: {func.__name__}")

        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for argno, (name, value) in enumerate(bound.arguments.items(), start=0):
            if name == "self":
                logger.decorator2("self = <something>")
                continue
            logger.decorator1(f"{argno=}")

            if isinstance(value, (list, dict)) or callable(
                getattr(value, "dump", None)
            ):
                if value is None or (isinstance(value, str) and value.strip() == ""):
                    logger.decorator4(f"{name} is None or empty")
                elif value is None or (
                    isinstance(value, (list, dict)) and len(value) == 0
                ):
                    logger.decorator4(f"{name} is None or empty")
                else:
                    logger.decorator2(f"{name}=")
                    logger.decorator4(value)
            else:
                logger.decorator4(f"    Argument: {name} = {value}")

        ##logger.decorator(args)
        logger.decorator3(f"{kwargs=}")

        # logger.decorator(f"Arguments: {args}, {kwargs}")
        try:
            start_time = time.perf_counter()  # Start timing
            result = func(*args, **kwargs)
            logger.decorator4(f"     - after Calling function: {func.__name__}")
            if isinstance(result, (list, dict)) or callable(
                getattr(result, "dump", None)
            ):
                if result is None or (isinstance(result, str) and result.strip() == ""):
                    logger.decorator("result is None or empty")
                elif result is None or (
                    isinstance(result, (list, dict)) and len(result) == 0
                ):
                    logger.decorator("result is None or Empty")
                else:
                    logger.decorator("result=")
                    # logger.decorator(result)
            else:
                logger.decorator(f"Return arg_valueue: {result}")
            logger.decorator("@-@                 ")
            end_time = time.perf_counter()  # End timing
            logger.decorator(
                f"Function {func.__name__} took {end_time - start_time:.6f} seconds"
            )
            # print("^")
            return result
        except Exception as e:
            logger.decorator_error(f"Exception in {func.__name__}: {e}")
            logger.decorator_error(traceback.format_exc())
            logger.decorator("@e@                 ")
            raise

    return wrapper

###############################################################################
def log_decoratorPlain(func) -> None:

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        # logger = CustomFormatter.theLogger  # Use the logger set up by CustomFormatter
        # logger.decorator("@+@                 ")
        # logger.decorator4(f"Calling function: {func.__name__}")
        print(f"Calling function: {func.__name__}")

        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for argno, (name, value) in enumerate(bound.arguments.items(), start=0):
            if name == "self":
                # logger.decorator2("self = <something>")
                print("self = <something>")
                continue
            # logger.decorator1(f"{counter=}")
            print(f"{argno=}")

            if isinstance(value, (list, dict)) or callable(
                getattr(value, "dump", None)
            ):
                if value is None or (isinstance(value, str) and value.strip() == ""):
                    # logger.decorator(f"{name} is None or empty")
                    print(f"{name} is None or empty")
                elif value is None or (
                    isinstance(value, (list, dict)) and len(value) == 0
                ):
                    # logger.decorator(f"{name} is None or empty")
                    print(f"{name} is None or empty")
                else:
                    # logger.decorator2(f"{name}=")
                    # logger.decorator(value)
                    print(f"{name}=")
                    print(value)
            else:
                # logger.decorator(f"Argument: {name} = {value}")
                # print(f"   Argument: {name} = {repr(value)}")
                print(f"   Argument: {name} = {value}")

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
                    print("result is None or empty")
                elif result is None or (
                    isinstance(result, (list, dict)) and len(result) == 0
                ):
                    # logger.decorator("result is None or Empty")
                    print("result is None or Empty")
                else:
                    # logger.decorator("result=")
                    print("result=")
                    # logger.decorator(result)
            else:
                # logger.decorator(f"Return arg_valueue: {result}")
                print(f"Return arg_valueue: {result}")
            # logger.decorator("@-@                 ")
            print("@-@                 ")
            end_time = time.perf_counter()  # End timing
            # logger.decorator(
            #     f"Function {func.__name__} took {end_time - start_time:.6f} seconds"
            # )
            print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds")
            print("^")
            return result
        except Exception as e:
            # logger.decorator_error(f"Exception in {func.__name__}: {e}")
            # logger.decorator_error(traceback.format_exc())
            # logger.decorator("@e@                 ")
            print(f"Exception in {func.__name__}: {e}")
            print(traceback.format_exc())
            print("@e@                 ")
            raise

    return wrapper



# -----------------------------------------------------------------
if __name__ == '__main__':
    """
    This is the main function that runs when the script is executed directly.
    It sets up the logger and demonstrates the usage of the CustomFormatter class.
    """
    print("You should not run this file directly, it is a module to be imported.")
    sys.exit(-99)
