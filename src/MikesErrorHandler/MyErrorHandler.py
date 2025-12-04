#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################

__version__ = '0.0.0.0036'
__author__ = 'Mike Merrett'
__updated__ = '2025-07-28 16:29:08'
###############################################################################
# MyErrorHandler.py
'''
    - addd this to your code and cal
        # handle uncaught exceptions
    sys.excepthook = handle_exception

'''

import sys
import traceback
from MyLogging import (logger)

try:
    import arcpy
    arcpy_available = True
except ImportError:
    arcpy_available = False

# let the errors happen or use this:
#                  except Exception as e:
#                      handle_exception(e)
#-----------------------------------------------------------------
def error_handler( e):

    logger.critical("-------Exception --------")
    tb_str = "".join(traceback.format_exception(e))
    logger.error( tb_str)

    if sys.modules.get("arcpy"):
        if isinstance(e, arcpy.ExecuteError):
            logger.error(f"ArcPy Error: {e}")
            for idx in range(arcpy.GetMessageCount()):
                logger.error(f"ArcPy Message {idx}: {arcpy.GetMessage(idx)}")
    s = e
    logger.error(s)
    #logger.error( "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback) )

    logger.error("---end of general exception handler-------")

    raise(e)



#-----------------------------------------------------------------
## let the errors happen or use this:
##                  except Exception as e:
##                      handle_exception(e)
def handle_exception(exc_type, exc_value, exc_traceback):

    if  'PyPDF2' not in str(exc_value):
        logger.critical("-------UnCaught Exception --------")
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)) # type: ignore
        logger.error( tb_str)

        if sys.modules.get("arcpy"):
            if isinstance(exc_type, arcpy.ExecuteError): # type: ignore
                logger.error(f"ArcPy Error: {exc_type} {exc_value}")
                for idx in range(arcpy.GetMessageCount()): # type: ignore
                    logger.error(f"ArcPy Message {idx}: {arcpy.GetMessage(idx)}") # type: ignore
        s = exc_type
        logger.error(s)
        logger.tracea( f"{exc_type=}")
        logger.traceb( f"{exc_value=}")
        logger.tracec( f"{exc_traceback=}")

        logger.debug("---end of general exception handler-------")

        raise (exc_type)
    else:
        logger.critical(' that annoying pyPDF error -  it can be ignored (no idea where it is coming from)')





# -----------------------------------------------------------------
def giveArcpyResults(r: arcpy.Result, txt="") -> int:
    try:
        statusCode: dict[int, str] = {
            0: "New",
            1: "Submitted",
            2: "Waiting",
            3: "Executing",
            4: "Succeeded",
            5: "Failed",
            6: "Timed out",
            7: "Cancelling",
            8: "Cancelled",
            9: "Deleting",
            10: "Deleted",
        }

        if r.status != 4:
            logger.error(f"Result Status={r.status} - { statusCode[r.status]}")
            logger.error("something went wrong!!!")
            logger.error(f"{r.status=}")
        else:
            logger.info(f"{txt} - Result Status={r.status} - { statusCode[r.status]}")

        matchcount = arcpy.management.GetCount(r[0])
        logger.info( f" Record Count = {matchcount}")

        for idx in range(r.messageCount):
            output = r.getMessage(idx)
            logger.warning(f"Output {idx}: {output}")
            if isinstance(output, arcpy.Result):
                logger.debug("Recursing into output ]]]")
                giveArcpyResults(output, txt + ']')

        for idx in range(r.outputCount):
            output = r.getOutput(idx)
            logger.warning(f"Output {idx}: {output}")
            if isinstance(output, arcpy.Result):
                logger.debug("Recursing into output >>>")
                giveArcpyResults(output, txt + '>')

        return r.status
    except Exception:
        pass
    return -1