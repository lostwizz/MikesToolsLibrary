#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomLevels.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 00:30:23"
###############################################################################


import logging
from logging import Logger
from MikesToolsLibrary.MyLogging.log_decorator import log_decorator


from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter

class CustomLevels:
    """Defines custom logging levels."""
    DEFAULT_TEXT_MSG = "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~"
    # -----------------------------------------------------------------
    def __init__(self):
        pass
        ##self.logger = logger

    # -----------------------------------------------------------------
    @classmethod
    def add_log_level(cls, level_name, level_num, method_name=None):
        if not method_name:
            method_name = level_name.lower()

        if hasattr(logging, level_name):
            raise AttributeError(f"{level_name} already defined in logging module")
        if hasattr(logging, method_name):
            raise AttributeError(f"{method_name} already defined in logging module")
        if hasattr(logging.getLoggerClass(), method_name):
            raise AttributeError(f"{method_name} already defined in logger class")

        def log_for_level(self, message, *args, **kwargs):
            stacklevel = kwargs.pop("stacklevel", 2)
            if not message:
                message = cls.DEFAULT_TEXT_MSG
            if self.isEnabledFor(level_num):
                self._log(level_num, message, args, **kwargs, stacklevel=stacklevel)

        def log_to_root(message, *args, **kwargs):
            logging.log(level_num, message, *args, **kwargs)

        logging.addLevelName(level_num, level_name)
        setattr(logging, level_name, level_num)
        setattr(logging.getLoggerClass(), method_name, log_for_level)
        setattr(logging, method_name, log_to_root)

    # -----------------------------------------------------------------
    @staticmethod
    @log_decorator
    def add_custom_level(level_name, level_num, method_name=None):
        return CustomLevels.add_log_level(level_name, level_num, method_name)


    # -----------------------------------------------------------------
    @classmethod
    def add(self, name :str, id: int, fmt: str) -> None:
        """
        Adds a new logging level with a custom format.
        :param name: Name of the logging level.
        :param id: Numeric ID of the logging level.
        :param fmt: Format string for the logging level.
        """
        self.add_log_level(name, id)
        # CustomFormatter.FORMATS[id]  = fmt + CustomFormatter.formatStr + CustomFormatter.reset
        CustomFormatter.COLORS[id]  = fmt

    # -----------------------------------------------------------------
    # def setupLogger( logger:logging, fileName:str, isTesting=False ) -> None:
    def addMyCustomLevelsLogger(self) -> None:
        """
        Sets up the logger with custom formatting and handlers.

        :param logger: The logger instance to set up.
        :param fileName: The name of the log file.
        :param isTesting: Boolean value to determine if the logger is in testing mode.


        This method configures the logger with custom formatting, handlers, and filters.
        It also sets the logging level and adds custom log levels.
        If isTesting is True, it shows example logging levels.

        Example usage:
            logger = logging.getLogger(__name__)
            CustomFormatter.setupLogger(logger, 'my_log_file.log', isTesting=True)
        """
        # self.theLogger = logger
        # self.theFilename = fileName

        self.add("QUERY",    55, "\x1b[1;35;40m")

        self.add( "TRACE", 100, "\x1b[00;97;45m")
        self.add("TRACEA", 101, "\x1b[1;32;104m")
        self.add("TRACEB", 102, "\x1b[1;37;43m" )
        self.add("TRACEC", 103, "\x1b[1;37;42m" )
        self.add("TRACED", 104, "\x1b[1;93;100m")
        self.add("TRACEE", 105, "\x1b[1;34;102m")
        self.add("TRACEF", 106, "\x1b[00;30;102m")
        self.add("TRACEG", 107, "\x1b[00;33;100m")
        self.add("TRACEH", 108, "\x1b[00;34;46m")
        self.add("TRACEI", 109, "\x1b[00;33;104m" )

        self.add("TRACEJ", 110, "\x1b[1;34;47m" )
        self.add("TRACEK", 111, "\x1b[65;93;100m" )
        self.add("TRACEL", 112, "\x1b[00;30;105m" )
        self.add("TRACEM", 113, "\x1b[00;94;43m" )
        self.add("TRACEN", 114, "\x1b[00;93;106m" )
        self.add("TRACEO", 115, "\x1b[0;35;43m" )
        self.add("TRACEP", 116, "\x1b[00;30;106m" )
        self.add("TRACEQ", 117, "\x1b[1;34;43m" )
        self.add("TRACER", 118, "\x1b[00;90;106m" )
        self.add("TRACES", 119, "\x1b[1;32;45m" )

        self.add("TRACET",  120, "\x1b[1;95;106m")
        self.add("TRACEU",  121, "\x1b[1;96;100m")
        self.add("TRACEV",  122, "\x1b[00;30;46m")
        self.add("TRACEW",  123, "\x1b[00;93;46m")
        self.add("TRACEX",  124, "\x1b[00;34;46m")
        self.add("TRACEY",  125, "\x1b[1;93;104m")
        self.add("TRACEZ",  126, "\x1b[1;93;105m")
        self.add("GREY",    201, "\x1b[1;90;40m")
        self.add("CYAN",    202, "\x1b[1;36;40m")
        self.add("PURPLE",  203, "\x1b[1;35;40m")
        self.add("GOLD",    204, "\x1b[0;33;40m")
        self.add("GREEN",   205, "\x1b[1;32;40m")
        self.add("YELLOW",  206, "\x1b[1;93;40m")
        self.add("LTBLUE",  207, "\x1b[1;34;40m")
        self.add("BLUE",    208, "\x1b[0;34;40m")
        self.add("WHITE",   209, "\x1b[1;37;40m")
        self.add("blkonoj", 210, "\x1b[7;33;40m")
        self.add("blkonyk", 211, "\x1b[7;93;40m")

        self.add("SAME",    250, "\x1b[0;34;40m")
        self.add("DIFF",    251, "\x1b[1;32;40m")
        self.add("LESS",    252, "\x1b[1;93;40m")
        self.add("MORE",    253, "\x1b[0;33;40m")
        self.add("IGNORE",  254, "\x1b[1;37;40m")


        self.add("MARK",  300, "\x1b[04;92;107m")
        self.add("MARK1", 301, "\x1b[04;92;107m")
        self.add("MARK2", 302, "\x1b[04;92;107m")
        self.add("MARK3", 303, "\x1b[04;92;107m")
        self.add("MARK4", 304, "\x1b[04;92;107m")
        self.add("MARK5", 305, "\x1b[04;92;107m")
        self.add("MARK6", 306, "\x1b[04;92;107m")
        self.add("MARK7", 307, "\x1b[04;92;107m")
        self.add("MARK8", 308, "\x1b[04;92;107m")
        self.add("MARK9", 309, "\x1b[04;92;107m")

        self.add("ToDo",  400, "\x1b[07;90;107m")
        self.add("ToDo1", 401, "\x1b[07;90;107m")
        self.add("ToDo2", 402, "\x1b[07;90;107m")
        self.add("ToDo3", 403, "\x1b[07;90;107m")
        self.add("ToDo4", 404, "\x1b[07;90;107m")
        self.add("ToDo5", 405, "\x1b[07;90;107m")
        self.add("ToDo6", 406, "\x1b[07;90;107m")
        self.add("ToDo7", 407, "\x1b[07;90;107m")
        self.add("ToDo8", 408, "\x1b[07;90;107m")
        self.add("ToDo9", 409, "\x1b[07;90;107m")

        self.add("Decorator",   500, "\x1b[00;90;103m")
        self.add("Decorator1",  501, "\x1b[00;32;103m")
        self.add("Decorator2",  502, "\x1b[00;30;103m")
        self.add("Decorator3",  503, "\x1b[00;34;103m")
        self.add("Decorator4",  504, "\x1b[00;36;103m")
        self.add("Decorator5",  505, "\x1b[00;95;103m")

        self.add("Decorator_error",  510, "\x1b[00;91;103m")

        self.add("rocket",         600, "\x1b[00;91;103m🚀")
        self.add("party",          601, "\x1b[00;91;103m🎉")
        self.add("cross",          602, "\x1b[00;91;103m❌")
        self.add("check",          603, "\x1b[00;91;103m✅")
        self.add("closedfolder",   604, "\x1b[00;91;103m📁")
        self.add("openfolder",     604, "\x1b[00;91;103m📂")
        self.add("tools",          605, "\x1b[00;91;103m🛠 ")
        self.add("explanationmark",606, "\x1b[00;91;103m❗️")
        self.add("warningsign",    607, "\x1b[00;91;103m⚠️")
        self.add("infosign",       608, "\x1b[00;91;103mℹ️")
        self.add("music",          609, "\x1b[00;91;103m🎵")
        self.add("magnifierleft",  610, "\x1b[00;91;103m🔍")
        self.add("magnifierright", 611, "\x1b[00;91;103m🔎")
        self.add("pipe",           612, "\x1b[00;91;103m🐛")
        self.add("microscope",     613, "\x1b[00;91;103m🔬")
        self.add("telescope",      614, "\x1b[00;91;103m🔭")
        self.add("fastforward",    615, "\x1b[00;91;103m⏩")

        self.add("appbegin",      700, "\x1b[00;96;107m")
        self.add("append",        701, "\x1b[00;96;107m")
        self.add("apppreamble",   702, "\x1b[00;96;107m")
        self.add("apppreend",     703, "\x1b[00;96;107m")
        self.add("apppostcln",    704, "\x1b[00;96;107m")
        self.add("apppostend",    705, "\x1b[00;96;107m")

        self.add("data1read",     710, "\x1b[00;96;107m")
        self.add("data1ins",      711, "\x1b[00;96;107m")
        self.add("data1upd",      712, "\x1b[00;96;107m")
        self.add("data1del",      713, "\x1b[00;96;107m")
        self.add("data1cmp",      714, "\x1b[00;96;107m")
        self.add("data1noop",     715, "\x1b[00;96;107m")
        self.add("data1where",    716, "\x1b[00;96;107m")
        self.add("data1info",     717, "\x1b[00;96;107m")
        self.add("data1flds",      718, "\x1b[00;96;107m")

        self.add("data2read",     720, "\x1b[00;96;107m")
        self.add("data2ins",      721, "\x1b[00;96;107m")
        self.add("data2upd",      722, "\x1b[00;96;107m")
        self.add("data2del",      723, "\x1b[00;96;107m")
        self.add("data2cmp",      724, "\x1b[00;96;107m")
        self.add("data2noop",     725, "\x1b[00;96;107m")
        self.add("data2where",    726, "\x1b[00;96;107m")
        self.add("data2info",     727, "\x1b[00;96;107m")
        self.add("data2flds",      728, "\x1b[00;96;107m")

        self.add("data3read",     730, "\x1b[00;96;107m")
        self.add("data3ins",      731, "\x1b[00;96;107m")
        self.add("data3upd",      732, "\x1b[00;96;107m")
        self.add("data3del",      733, "\x1b[00;96;107m")
        self.add("data3cmp",      734, "\x1b[00;96;107m")
        self.add("data3noop",     735, "\x1b[00;96;107m")
        self.add("data3where",    736, "\x1b[00;96;107m")
        self.add("data3info",     737, "\x1b[00;96;107m")
        self.add("data3flds",      738, "\x1b[00;96;107m")

        self.add("data4read",     740, "\x1b[00;96;107m")
        self.add("data4ins",      741, "\x1b[00;96;107m")
        self.add("data4upd",      742, "\x1b[00;96;107m")
        self.add("data4del",      743, "\x1b[00;96;107m")
        self.add("data4cmp",      744, "\x1b[00;96;107m")
        self.add("data4noop",     745, "\x1b[00;96;107m")
        self.add("data4where",    746, "\x1b[00;96;107m")
        self.add("data4info",     747, "\x1b[00;96;107m")
        self.add("data4flds",      748, "\x1b[00;96;107m")

        self.add("data5read",     750, "\x1b[00;96;107m")
        self.add("data5ins",      751, "\x1b[00;96;107m")
        self.add("data5upd",      752, "\x1b[00;96;107m")
        self.add("data5del",      753, "\x1b[00;96;107m")
        self.add("data5cmp",      754, "\x1b[00;96;107m")
        self.add("data5noop",     755, "\x1b[00;96;107m")
        self.add("data5where",    756, "\x1b[00;96;107m")
        self.add("data5info",     757, "\x1b[00;96;107m")
        self.add("data5flds",      758, "\x1b[00;96;107m")

        self.add("data6read",     760, "\x1b[00;96;107m")
        self.add("data6ins",      761, "\x1b[00;96;107m")
        self.add("data6upd",      762, "\x1b[00;96;107m")
        self.add("data6del",      763, "\x1b[00;96;107m")
        self.add("data6cmp",      764, "\x1b[00;96;107m")
        self.add("data6noop",     765, "\x1b[00;96;107m")
        self.add("data6where",    766, "\x1b[00;96;107m")
        self.add("data6info",     767, "\x1b[00;96;107m")
        self.add("data6flds",      768, "\x1b[00;96;107m")

        self.add("data7read",     770, "\x1b[00;96;107m")
        self.add("data7ins",      771, "\x1b[00;96;107m")
        self.add("data7upd",      772, "\x1b[00;96;107m")
        self.add("data7del",      773, "\x1b[00;96;107m")
        self.add("data7cmp",      774, "\x1b[00;96;107m")
        self.add("data7noop",     775, "\x1b[00;96;107m")
        self.add("data7where",    776, "\x1b[00;96;107m")
        self.add("data7info",     777, "\x1b[00;96;107m")
        self.add("data7flds",      778, "\x1b[00;96;107m")

        self.add("data8read",     780, "\x1b[00;96;107m")
        self.add("data8ins",      781, "\x1b[00;96;107m")
        self.add("data8upd",      782, "\x1b[00;96;107m")
        self.add("data8del",      783, "\x1b[00;96;107m")
        self.add("data8cmp",      784, "\x1b[00;96;107m")
        self.add("data8noop",     785, "\x1b[00;96;107m")
        self.add("data8where",    786, "\x1b[00;96;107m")
        self.add("data8info",     787, "\x1b[00;96;107m")
        self.add("data8flds",      788, "\x1b[00;96;107m")

        self.add("data9read",     790, "\x1b[00;96;107m")
        self.add("data9ins",      791, "\x1b[00;96;107m")
        self.add("data9upd",      792, "\x1b[00;96;107m")
        self.add("data9del",      793, "\x1b[00;96;107m")
        self.add("data9cmp",      794, "\x1b[00;96;107m")
        self.add("data9noop",     795, "\x1b[00;96;107m")
        self.add("data9where",    796, "\x1b[00;96;107m")
        self.add("data9info",     797, "\x1b[00;96;107m")
        self.add("data9flds",      798, "\x1b[00;96;107m")
