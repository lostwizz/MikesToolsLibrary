#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 00:33:24"
###############################################################################
import logging

from MikesToolsLibrary.MyLogging.log_decorator import log_decorator


from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels
from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter


# from .CustomFormatter import CustomFormatter
# from .CustomLevels import CustomLevels

from .ExcludeLevelFilter import ExcludeLevelFilter





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
        self.lvls = None

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
    @classmethod
    def add_special_levels(self):
        """Add the predefined custom log levels by delegating to CustomLevels."""
        CustomLevels.addMyCustomLevels()

    # -----------------------------------------------------------------
    @classmethod
    def add_level(cls, level_name: str, level_num: int, colorFmt: str = None):
        """
        Add a custom logging level.
        :param level_name: Name of the logging level.
        :param level_num: Numeric value of the logging level.
        :param method_name: Optional method name for logger.
        """

        CustomLevels.add(level_name, level_num, colorFmt)


    # -----------------------------------------------------------------
    def get_logger(self) -> logging.Logger:
        return self.logger

    # -----------------------------------------------------------------

    def add_custom_level(self, level_name, level_num, method_name=None):
        """Add a custom level via the CustomLevels helper class."""
        return CustomLevels.add(level_name, level_num, method_name)


    # -----------------------------------------------------------------
    def add_filter(self, level_to_exclude: int):
        """
        Add a filter to exclude a specific level from console/file output.
        """
        for handler in self.logger.handlers:
            handler.addFilter(ExcludeLevelFilter(level_to_exclude))

    # -----------------------------------------------------------------

    def show_all_levels():

        logger.debug('This message should go to the log file level 10')
        logger.info('So should this level 20')
        logger.warning('And this, too level 30')
        ### logger.warn('And this, too just warn not warning')
        logger.error('test error level level 40')
        logger.critical('test critical error level 50')

        logger.query('test of query 55')

        logger.trace( 'test of trace 100')
        logger.tracea('test of trace 101')
        logger.traceb('test of trace 102')
        logger.tracec('test of trace 103')
        logger.traced('test of trace 104')
        logger.tracee('test of trace 105')
        logger.tracef('test of trace 106')
        logger.traceg('test of trace 107')
        logger.traceh('test of trace 108')
        logger.tracei('test of trace 109')

        logger.tracej('test of trace 110')
        logger.tracek('test of trace 111')
        logger.tracel('test of trace 112')
        logger.tracem('test of trace 113')
        logger.tracen('test of trace 114')
        logger.traceo('test of trace 115')
        logger.tracep('test of trace 116')
        logger.traceq('test of trace 117')
        logger.tracer('test of trace 118')
        logger.traces('test of trace 119')

        logger.tracet('test of trace 120')
        logger.traceu('test of trace 121')
        logger.tracev('test of trace 122')
        logger.tracew('test of trace 123')
        logger.tracex('test of trace 124')
        logger.tracey('test of trace 125')
        logger.tracez('test of trace 126')

        logger.grey('test of grey 201')
        logger.cyan('test of cyan 202')
        logger.purple('test of purple 203')
        logger.gold('test of gold 204')
        logger.green('test of green 205')
        logger.yellow('test of yellow 206')
        logger.ltblue('test of light blue 207')
        logger.blue('test of blue 208')
        logger.white('test of white 209')
        logger.blkonoj('test of black on orangec 210')
        logger.blkonyk('test of black on yellow 211')

        logger.same(' test of same 250')
        logger.diff(' test of diff 251')
        logger.less(' test of less 252')
        logger.more(' test of more 253')
        logger.ignore(' test of ignore 254')

        logger.mark ("test of mark 300")
        logger.mark1("test of mark 301")
        logger.mark2("test of mark 302")
        logger.mark3("test of mark 303")
        logger.mark4("test of mark 304")
        logger.mark5("test of mark 305")
        logger.mark6("test of mark 306")
        logger.mark7("test of mark 307")
        logger.mark8("test of mark 308")
        logger.mark9("test of mark 309")
        logger.mark()
        logger.mark1()

        logger.todo ("test of todo 400")
        logger.todo1("test of todo 401")
        logger.todo2("test of todo 402")
        logger.todo3("test of todo 403")
        logger.todo4("test of todo 404")
        logger.todo5("test of todo 405")
        logger.todo6("test of todo 406")
        logger.todo7("test of todo 407")
        logger.todo8("test of todo 408")
        logger.todo9("test of todo 409")
        logger.todo()
        logger.todo9()

        logger.decorator( "test of decorator 500")
        logger.decorator1("test of decorator 501")
        logger.decorator2("test of decorator 502")
        logger.decorator3("test of decorator 503")
        logger.decorator4("test of decorator 504")
        logger.decorator5("test of decorator 505")
        logger.decorator_error("test of decorator 510")

        logger.rocket         ("test of rocket        600")
        logger.party          ("test of party         601")
        logger.cross          ("test of cross         602")
        logger.check          ("test of check         603")
        logger.closedfolder   ("test of closedfolder  604")
        logger.openfolder     ("test of openfolder    604")
        logger.tools          ("test of tools         605")
        logger.explanationmark("test of explanationmark 606")
        logger.warningsign    ("test of warning       607")
        logger.infosign       ("test of infosign      608")
        logger.music          ("test of music         609")
        logger.magnifierleft  ("test of magnifierLeft 610")
        logger.magnifierright ("test of magnifierRight 611")
        logger.pipe           ("test of pipe          612")
        logger.microscope     ("test of microscope    613")
        logger.telescope      ("test of telescope     614")

        logger.appbegin       ('test of appbegin    700' )
        logger.append         ('test of append      701'   )
        logger.apppreamble    ('test of apppreamble 702')
        logger.apppreend      ('test of apppreend   703')
        logger.apppostcln     ('test of apppostcln  704')
        logger.apppostend     ('test of apppostend  705')

        logger.data1read      ('test of data1read  710')
        logger.data1ins       ('test of data1ins   711' )
        logger.data1upd       ('test of data1upd   712' )
        logger.data1del       ('test of data1del   713' )
        logger.data1cmp       ('test of data1cmp   714')
        logger.data1noop      ('test of data1noop  715')
        logger.data1where     ('test of data1where 716')
        logger.data1info      ('test of data1info  717')

        logger.data2read      ('test of data2read' )
        logger.data2ins       ('test of data2ins' )
        logger.data2upd       ('test of data2upd' )
        logger.data2del       ('test of data2del' )
        logger.data2cmp       ('test of data2cmp')
        logger.data2noop      ('test of data2noop')
        logger.data2where     ('test of data2where')
        logger.data2info      ('test of data2info')

        logger.data3read      ('test of data3read')
        logger.data3ins       ('test of data3ins' )
        logger.data3upd       ('test of data3upd' )
        logger.data3del       ('test of data3del' )
        logger.data3cmp       ('test of data3cmp')
        logger.data3noop      ('test of data3noop')
        logger.data3where     ('test of data3where')
        logger.data3info      ('test of data3info')

        logger.data4read      ('test of data4read')
        logger.data4ins       ('test of data4ins' )
        logger.data4upd       ('test of data4upd' )
        logger.data4del       ('test of data4del' )
        logger.data4cmp       ('test of data4cmp')
        logger.data4noop      ('test of data4noop')
        logger.data4where     ('test of data4where')
        logger.data4info      ('test of data4info')

        logger.data5read      ('test of data5read')
        logger.data5ins       ('test of data5ins' )
        logger.data5upd       ('test of data5upd' )
        logger.data5del       ('test of data5del' )
        logger.data5cmp       ('test of data5cmp')
        logger.data5noop      ('test of data5noop')
        logger.data5where     ('test of data5where')
        logger.data5info      ('test of data5info')

        logger.data6read      ('test of data6read')
        logger.data6ins       ('test of data6ins' )
        logger.data6upd       ('test of data6upd' )
        logger.data6del       ('test of data6del' )
        logger.data6cmp       ('test of data6cmp')
        logger.data6noop      ('test of data6noop')
        logger.data6where     ('test of data6where')
        logger.data6info      ('test of data6info')

        logger.data7read      ('test of data7read')
        logger.data7ins       ('test of data7ins' )
        logger.data7upd       ('test of data7upd' )
        logger.data7del       ('test of data7del' )
        logger.data7cmp       ('test of data7cmp')
        logger.data7noop      ('test of data7noop')
        logger.data7where     ('test of data7where')
        logger.data7info      ('test of data7info')

        logger.data8read      ('test of data8read')
        logger.data8ins       ('test of data8ins' )
        logger.data8upd       ('test of data8upd' )
        logger.data8del       ('test of data8del' )
        logger.data8cmp       ('test of data8cmp')
        logger.data8noop      ('test of data8noop')
        logger.data8where     ('test of data8where')
        logger.data8info      ('test of data8info')

        logger.data9read      ('test of data9read')
        logger.data9ins       ('test of data9ins' )
        logger.data9upd       ('test of data9upd' )
        logger.data9del       ('test of data9del' )
        logger.data9cmp       ('test of data9cmp')
        logger.data9noop      ('test of data9noop')
        logger.data9where     ('test of data9where')
        logger.data9info      ('test of data9info 797')



