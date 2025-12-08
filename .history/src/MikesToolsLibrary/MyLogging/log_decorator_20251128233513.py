#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 23:35:13"
###############################################################################


# =================================================================
from typing import Callable
import inspect
import time
import traceback
from functools import wraps
import logging

# def log_decorator(func):

    # @wraps(func)
    # def wrapper(*args, **kwargs):
    #     logger = logging.getLogger("MikesToolsLibrary")  # or your chosen logger name
    #     logger.debug(f"Calling function: {func.__name__}")

    #     # Log arguments
    #     sig = inspect.signature(func)
    #     bound = sig.bind(*args, **kwargs)
    #     bound.apply_defaults()
    #     for name, value in bound.arguments.items():
    #         logger.debug(f"Arg {name} = {value!r}")

    #     try:
    #         start_time = time.perf_counter()
    #         result = func(*args, **kwargs)
    #         end_time = time.perf_counter()
    #         logger.debug(f"{func.__name__} returned {result!r}")
    #         logger.debug(f"Function {func.__name__} took {end_time - start_time:.6f} seconds")
    #         return result
    #     except Exception as e:
    #         logger.error(f"Exception in {func.__name__}: {e}")
    #         logger.error(traceback.format_exc())
    #         raise

    # return wrapper



def log_decorator(func) -> None:


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
                    logger.decorator(f"{name} is None or empty")
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
                    print("result is None or empty")
                elif result is None or (
                    isinstance(result, (list, dict)) and len(result) == 0
                ):
                    # logger.decorator("result is None or Empty")
                    print("result is None or Empty")
                else:
                    # logger.decorator("result=")
                    print("result=")
                    #logger.decorator(result)
            else:
                # logger.decorator(f"Return arg_valueue: {result}")
                print(f"Return arg_valueue: {result}")
            # logger.decorator("@-@                 ")
            print("@-@                 ")
            end_time = time.perf_counter()  # End timing
            # logger.decorator(
            #     f"Function {func.__name__} took {end_time - start_time:.6f} seconds"
            # )
            print(
                f"Function {func.__name__} took {end_time - start_time:.6f} seconds"
            )
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

