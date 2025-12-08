#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomLevels.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-27 00:02:20"
###############################################################################

class CustomLevels:
    """Defines custom logging levels."""

    # Define custom logging levels
    VERBOSE = 15
    NOTICE = 25
    ALERT = 45



    @staticmethod
    def add_custom_levels_to_logging(logging_module):
        """Adds custom levels to the logging module."""
        logging_module.addLevelName(CustomLevels.VERBOSE, "VERBOSE")
        logging_module.addLevelName(CustomLevels.NOTICE, "NOTICE")
        logging_module.addLevelName(CustomLevels.ALERT, "ALERT")

        def verbose(self, message, *args, **kws):
            if self.isEnabledFor(CustomLevels.VERBOSE):
                self._log(CustomLevels.VERBOSE, message, args, **kws)

        def notice(self, message, *args, **kws):
            if self.isEnabledFor(CustomLevels.NOTICE):
                self._log(CustomLevels.NOTICE, message, args, **kws)

        def alert(self, message, *args, **kws):
            if self.isEnabledFor(CustomLevels.ALERT):
                self._log(CustomLevels.ALERT, message, args, **kws)

        logging_module.Logger.verbose = verbose
        logging_module.Logger.notice = notice
        logging_module.Logger.alert = alert


    # -----------------------------------------------------------------
    def add_log_level(level_name, level_num, method_name=None) -> None:
        """
        Adds a new logging level to the logging module and logger class.
        :param level_name: Name of the new logging level.
        :param level_num: Numeric value of the new logging level.
        :param method_name: Optional method name for the new logging level.


        This method dynamically adds a new logging level to the logging module and logger class.
        It also creates a method for logging at the new level.
        If the level name or method name already exists, an AttributeError is raised.


        Example usage:
            CustomFormatter.add_log_level('CUSTOM_LEVEL', 25, 'custom_log')
            logger = logging.getLogger(__name__)
            logger.custom_log('This is a custom log message at level 25')
        """
        if not method_name:
            method_name = level_name.lower()

        if hasattr(logging, level_name):
            raise AttributeError('{} already defined in logging module'.format(level_name))
        if hasattr(logging, method_name):
            raise AttributeError('{} already defined in logging module'.format(method_name))
        if hasattr(logging.getLoggerClass(), method_name):
            raise AttributeError('{} already defined in logger class'.format(method_name))

        # This method was inspired by the answers to Stack Overflow post
        # http://stackoverflow.com/q/2183233/2988730,
        # # # def log_for_level(self, message, *args, **kwargs):
            # # # if self.isEnabledFor(level_num):
                # # # self._log(level_num, message, args, **kwargs)
        def log_for_level(self, message=None, *args, **kwargs):
            stacklevel = kwargs.pop("stacklevel", 2)  # Default to 2 levels up
            if not message:
                message = CustomFormatter.DEFAULT_TEXT_MSG
            if self.isEnabledFor(level_num):
                self._log(level_num, message, args, kwargs, stacklevel=stacklevel)

        def log_to_root(message, *args, **kwargs):
            logging.log(level_num, message, *args, **kwargs)

        logging.addLevelName(level_num, level_name)
        setattr(logging, level_name, level_num)
        setattr(logging.getLoggerClass(), method_name, log_for_level)
        setattr(logging, method_name, log_to_root)


    # -----------------------------------------------------------------
    def add(name :str, id: int, fmt: str) -> None:
        """
        Adds a new logging level with a custom format.
        :param name: Name of the logging level.
        :param id: Numeric ID of the logging level.
        :param fmt: Format string for the logging level.
        """
        CustomFormatter.add_log_level(name, id)
        CustomFormatter.FORMATS[id]  = fmt + CustomFormatter.formatStr + CustomFormatter.reset

    # -----------------------------------------------------------------
    def setupLogger( logger:logging, fileName:str, isTesting=False ) -> None:
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
        CustomFormatter.theLogger = logger
        CustomFormatter.theFilename = fileName

        CustomFormatter.add("QUERY",    55, "\x1b[1;35;40m")

        CustomFormatter.add( "TRACE", 100, "\x1b[00;97;45m")
        CustomFormatter.add("TRACEA", 101, "\x1b[1;32;104m")
        CustomFormatter.add("TRACEB", 102, "\x1b[1;37;43m" )
        CustomFormatter.add("TRACEC", 103, "\x1b[1;37;42m" )
        CustomFormatter.add("TRACED", 104, "\x1b[1;93;100m")
        CustomFormatter.add("TRACEE", 105, "\x1b[1;34;102m")
        CustomFormatter.add("TRACEF", 106, "\x1b[00;30;102m")
        CustomFormatter.add("TRACEG", 107, "\x1b[00;33;100m")
        CustomFormatter.add("TRACEH", 108, "\x1b[00;34;46m")
        CustomFormatter.add("TRACEI", 109, "\x1b[00;33;104m" )

        CustomFormatter.add("TRACEJ", 110, "\x1b[1;34;47m" )
        CustomFormatter.add("TRACEK", 111, "\x1b[65;93;100m" )
        CustomFormatter.add("TRACEL", 112, "\x1b[00;30;105m" )
        CustomFormatter.add("TRACEM", 113, "\x1b[00;94;43m" )
        CustomFormatter.add("TRACEN", 114, "\x1b[00;93;106m" )
        CustomFormatter.add("TRACEO", 115, "\x1b[0;35;43m" )
        CustomFormatter.add("TRACEP", 116, "\x1b[00;30;106m" )
        CustomFormatter.add("TRACEQ", 117, "\x1b[1;34;43m" )
        CustomFormatter.add("TRACER", 118, "\x1b[00;90;106m" )
        CustomFormatter.add("TRACES", 119, "\x1b[1;32;45m" )

        CustomFormatter.add("TRACET",  120, "\x1b[1;95;106m")
        CustomFormatter.add("TRACEU",  121, "\x1b[1;96;100m")
        CustomFormatter.add("TRACEV",  122, "\x1b[00;30;46m")
        CustomFormatter.add("TRACEW",  123, "\x1b[00;93;46m")
        CustomFormatter.add("TRACEX",  124, "\x1b[00;34;46m")
        CustomFormatter.add("TRACEY",  125, "\x1b[1;93;104m")
        CustomFormatter.add("TRACEZ",  126, "\x1b[1;93;105m")
        CustomFormatter.add("GREY",    201, "\x1b[1;90;40m")
        CustomFormatter.add("CYAN",    202, "\x1b[1;36;40m")
        CustomFormatter.add("PURPLE",  203, "\x1b[1;35;40m")
        CustomFormatter.add("GOLD",    204, "\x1b[0;33;40m")
        CustomFormatter.add("GREEN",   205, "\x1b[1;32;40m")
        CustomFormatter.add("YELLOW",  206, "\x1b[1;93;40m")
        CustomFormatter.add("LTBLUE",  207, "\x1b[1;34;40m")
        CustomFormatter.add("BLUE",    208, "\x1b[0;34;40m")
        CustomFormatter.add("WHITE",   209, "\x1b[1;37;40m")
        CustomFormatter.add("blkonoj", 210, "\x1b[7;33;40m")
        CustomFormatter.add("blkonyk", 211, "\x1b[7;93;40m")

        CustomFormatter.add("SAME",    250, "\x1b[0;34;40m")
        CustomFormatter.add("DIFF",    251, "\x1b[1;32;40m")
        CustomFormatter.add("LESS",    252, "\x1b[1;93;40m")
        CustomFormatter.add("MORE",    253, "\x1b[0;33;40m")
        CustomFormatter.add("IGNORE",  254, "\x1b[1;37;40m")


        CustomFormatter.add("MARK",  300, "\x1b[04;92;107m")
        CustomFormatter.add("MARK1", 301, "\x1b[04;92;107m")
        CustomFormatter.add("MARK2", 302, "\x1b[04;92;107m")
        CustomFormatter.add("MARK3", 303, "\x1b[04;92;107m")
        CustomFormatter.add("MARK4", 304, "\x1b[04;92;107m")
        CustomFormatter.add("MARK5", 305, "\x1b[04;92;107m")
        CustomFormatter.add("MARK6", 306, "\x1b[04;92;107m")
        CustomFormatter.add("MARK7", 307, "\x1b[04;92;107m")
        CustomFormatter.add("MARK8", 308, "\x1b[04;92;107m")
        CustomFormatter.add("MARK9", 309, "\x1b[04;92;107m")

        CustomFormatter.add("ToDo",  400, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo1", 401, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo2", 402, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo3", 403, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo4", 404, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo5", 405, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo6", 406, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo7", 407, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo8", 408, "\x1b[07;90;107m")
        CustomFormatter.add("ToDo9", 409, "\x1b[07;90;107m")

        CustomFormatter.add("Decorator",   500, "\x1b[00;90;103m")
        CustomFormatter.add("Decorator1",  501, "\x1b[00;32;103m")
        CustomFormatter.add("Decorator2",  502, "\x1b[00;30;103m")
        CustomFormatter.add("Decorator3",  503, "\x1b[00;34;103m")
        CustomFormatter.add("Decorator4",  504, "\x1b[00;36;103m")
        CustomFormatter.add("Decorator5",  505, "\x1b[00;95;103m")

        CustomFormatter.add("Decorator_error",  510, "\x1b[00;91;103m")

        CustomFormatter.add("rocket",         600, "\x1b[00;91;103m🚀")
        CustomFormatter.add("party",          601, "\x1b[00;91;103m🎉")
        CustomFormatter.add("cross",          602, "\x1b[00;91;103m❌")
        CustomFormatter.add("check",          603, "\x1b[00;91;103m✅")
        CustomFormatter.add("closedfolder",   604, "\x1b[00;91;103m📁")
        CustomFormatter.add("openfolder",     604, "\x1b[00;91;103m📂")
        CustomFormatter.add("tools",          605, "\x1b[00;91;103m🛠 ")
        CustomFormatter.add("explanationmark",606, "\x1b[00;91;103m❗️")
        CustomFormatter.add("warningsign",    607, "\x1b[00;91;103m⚠️")
        CustomFormatter.add("infosign",       608, "\x1b[00;91;103mℹ️")
        CustomFormatter.add("music",          609, "\x1b[00;91;103m🎵")
        CustomFormatter.add("magnifierleft",  610, "\x1b[00;91;103m🔍")
        CustomFormatter.add("magnifierright", 611, "\x1b[00;91;103m🔎")
        CustomFormatter.add("pipe",           612, "\x1b[00;91;103m🐛")
        CustomFormatter.add("microscope",     613, "\x1b[00;91;103m🔬")
        CustomFormatter.add("telescope",      614, "\x1b[00;91;103m🔭")
        CustomFormatter.add("fastforward",    615, "\x1b[00;91;103m⏩")

        CustomFormatter.add("appbegin",      700, "\x1b[00;96;107m")
        CustomFormatter.add("append",        701, "\x1b[00;96;107m")
        CustomFormatter.add("apppreamble",   702, "\x1b[00;96;107m")
        CustomFormatter.add("apppreend",     703, "\x1b[00;96;107m")
        CustomFormatter.add("apppostcln",    704, "\x1b[00;96;107m")
        CustomFormatter.add("apppostend",    705, "\x1b[00;96;107m")

        CustomFormatter.add("data1read",     710, "\x1b[00;96;107m")
        CustomFormatter.add("data1ins",      711, "\x1b[00;96;107m")
        CustomFormatter.add("data1upd",      712, "\x1b[00;96;107m")
        CustomFormatter.add("data1del",      713, "\x1b[00;96;107m")
        CustomFormatter.add("data1cmp",      714, "\x1b[00;96;107m")
        CustomFormatter.add("data1noop",     715, "\x1b[00;96;107m")
        CustomFormatter.add("data1where",    716, "\x1b[00;96;107m")
        CustomFormatter.add("data1info",     717, "\x1b[00;96;107m")
        CustomFormatter.add("data1flds",      718, "\x1b[00;96;107m")

        CustomFormatter.add("data2read",     720, "\x1b[00;96;107m")
        CustomFormatter.add("data2ins",      721, "\x1b[00;96;107m")
        CustomFormatter.add("data2upd",      722, "\x1b[00;96;107m")
        CustomFormatter.add("data2del",      723, "\x1b[00;96;107m")
        CustomFormatter.add("data2cmp",      724, "\x1b[00;96;107m")
        CustomFormatter.add("data2noop",     725, "\x1b[00;96;107m")
        CustomFormatter.add("data2where",    726, "\x1b[00;96;107m")
        CustomFormatter.add("data2info",     727, "\x1b[00;96;107m")
        CustomFormatter.add("data2flds",      728, "\x1b[00;96;107m")

        CustomFormatter.add("data3read",     730, "\x1b[00;96;107m")
        CustomFormatter.add("data3ins",      731, "\x1b[00;96;107m")
        CustomFormatter.add("data3upd",      732, "\x1b[00;96;107m")
        CustomFormatter.add("data3del",      733, "\x1b[00;96;107m")
        CustomFormatter.add("data3cmp",      734, "\x1b[00;96;107m")
        CustomFormatter.add("data3noop",     735, "\x1b[00;96;107m")
        CustomFormatter.add("data3where",    736, "\x1b[00;96;107m")
        CustomFormatter.add("data3info",     737, "\x1b[00;96;107m")
        CustomFormatter.add("data3flds",      738, "\x1b[00;96;107m")

        CustomFormatter.add("data4read",     740, "\x1b[00;96;107m")
        CustomFormatter.add("data4ins",      741, "\x1b[00;96;107m")
        CustomFormatter.add("data4upd",      742, "\x1b[00;96;107m")
        CustomFormatter.add("data4del",      743, "\x1b[00;96;107m")
        CustomFormatter.add("data4cmp",      744, "\x1b[00;96;107m")
        CustomFormatter.add("data4noop",     745, "\x1b[00;96;107m")
        CustomFormatter.add("data4where",    746, "\x1b[00;96;107m")
        CustomFormatter.add("data4info",     747, "\x1b[00;96;107m")
        CustomFormatter.add("data4flds",      748, "\x1b[00;96;107m")

        CustomFormatter.add("data5read",     750, "\x1b[00;96;107m")
        CustomFormatter.add("data5ins",      751, "\x1b[00;96;107m")
        CustomFormatter.add("data5upd",      752, "\x1b[00;96;107m")
        CustomFormatter.add("data5del",      753, "\x1b[00;96;107m")
        CustomFormatter.add("data5cmp",      754, "\x1b[00;96;107m")
        CustomFormatter.add("data5noop",     755, "\x1b[00;96;107m")
        CustomFormatter.add("data5where",    756, "\x1b[00;96;107m")
        CustomFormatter.add("data5info",     757, "\x1b[00;96;107m")
        CustomFormatter.add("data5flds",      758, "\x1b[00;96;107m")

        CustomFormatter.add("data6read",     760, "\x1b[00;96;107m")
        CustomFormatter.add("data6ins",      761, "\x1b[00;96;107m")
        CustomFormatter.add("data6upd",      762, "\x1b[00;96;107m")
        CustomFormatter.add("data6del",      763, "\x1b[00;96;107m")
        CustomFormatter.add("data6cmp",      764, "\x1b[00;96;107m")
        CustomFormatter.add("data6noop",     765, "\x1b[00;96;107m")
        CustomFormatter.add("data6where",    766, "\x1b[00;96;107m")
        CustomFormatter.add("data6info",     767, "\x1b[00;96;107m")
        CustomFormatter.add("data6flds",      768, "\x1b[00;96;107m")

        CustomFormatter.add("data7read",     770, "\x1b[00;96;107m")
        CustomFormatter.add("data7ins",      771, "\x1b[00;96;107m")
        CustomFormatter.add("data7upd",      772, "\x1b[00;96;107m")
        CustomFormatter.add("data7del",      773, "\x1b[00;96;107m")
        CustomFormatter.add("data7cmp",      774, "\x1b[00;96;107m")
        CustomFormatter.add("data7noop",     775, "\x1b[00;96;107m")
        CustomFormatter.add("data7where",    776, "\x1b[00;96;107m")
        CustomFormatter.add("data7info",     777, "\x1b[00;96;107m")
        CustomFormatter.add("data7flds",      778, "\x1b[00;96;107m")

        CustomFormatter.add("data8read",     780, "\x1b[00;96;107m")
        CustomFormatter.add("data8ins",      781, "\x1b[00;96;107m")
        CustomFormatter.add("data8upd",      782, "\x1b[00;96;107m")
        CustomFormatter.add("data8del",      783, "\x1b[00;96;107m")
        CustomFormatter.add("data8cmp",      784, "\x1b[00;96;107m")
        CustomFormatter.add("data8noop",     785, "\x1b[00;96;107m")
        CustomFormatter.add("data8where",    786, "\x1b[00;96;107m")
        CustomFormatter.add("data8info",     787, "\x1b[00;96;107m")
        CustomFormatter.add("data8flds",      788, "\x1b[00;96;107m")

        CustomFormatter.add("data9read",     790, "\x1b[00;96;107m")
        CustomFormatter.add("data9ins",      791, "\x1b[00;96;107m")
        CustomFormatter.add("data9upd",      792, "\x1b[00;96;107m")
        CustomFormatter.add("data9del",      793, "\x1b[00;96;107m")
        CustomFormatter.add("data9cmp",      794, "\x1b[00;96;107m")
        CustomFormatter.add("data9noop",     795, "\x1b[00;96;107m")
        CustomFormatter.add("data9where",    796, "\x1b[00;96;107m")
        CustomFormatter.add("data9info",     797, "\x1b[00;96;107m")
        CustomFormatter.add("data9flds",      798, "\x1b[00;96;107m")
