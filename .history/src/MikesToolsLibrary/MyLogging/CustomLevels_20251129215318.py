#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomLevels.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 21:53:18"
###############################################################################


import logging
from logging import Logger
from MikesToolsLibrary.MyLogging.log_decorator import log_decorator


from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter

###############################################################################
###############################################################################
class CustomLevels:
    """Defines custom logging levels."""
    DEFAULT_TEXT_MSG = "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~"


    # -----------------------------------------------------------------
    def __init__(self):
        pass
        ##self.logger = logger

    # -----------------------------------------------------------------
    @classmethod
    def add_log_level(cls, level_name, level_num, method_name=None, color=None, specialChars:str =None):
        if not method_name:
            method_name = level_name.lower()

        if hasattr(logging, level_name):
            raise AttributeError(f"{level_name} already defined in logging module")
        if hasattr(logging, method_name):
            raise AttributeError(f"{method_name} already defined in logging module")
        if hasattr(logging.getLoggerClass(), method_name):
            raise AttributeError(f"{method_name} already defined in logger class")

        def log_for_level(self, message=None, *args, **kwargs):
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

        if specialChars:
            CustomFormatter.SPECIAL_CHARACTERS[level_num] = specialChars

        # Register color if provided
        if color:
            CustomFormatter.COLORS[level_num] = color
            # print(f"Adding color for level {level_name} ({level_num}): {repr(CustomFormatter.COLORS[level_num])}")



    # -----------------------------------------------------------------
    @staticmethod
    def add_custom_level(level_name, level_num, method_name=None):
        return CustomLevels.add_log_level(level_name, level_num, method_name)


    # -----------------------------------------------------------------
    @classmethod
    def add(self, name :str, id: int, fmt: str, specialChars:str=None) -> None:
        """
        Adds a new logging level with a custom format.
        :param name: Name of the logging level.
        :param id: Numeric ID of the logging level.
        :param fmt: Format string for the logging level.
        """
        self.add_log_level(name, id, color=fmt, specialChars = specialChars)
        # CustomFormatter.FORMATS[id]  = fmt + CustomFormatter.formatStr + CustomFormatter.reset
        # CustomFormatter.COLORS[id]  = fmt
        # print(f"Added custom level: {name} ({id}) with format: {repr(CustomFormatter.COLORS[id])}")

    # -----------------------------------------------------------------
    # def setupLogger( logger:logging, fileName:str, isTesting=False ) -> None:
    @classmethod
    def addMyCustomLevels(self, logger) -> None:
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
        self.theLogger = logger
        # self.theFilename = fileName

        self.add("QUERY",    55, "\x1b[1;35;40m")

        self.add("SUCCESS", 91,  "", "✔")
        self.add("FAILURE", 92, "", "❗❌")
        
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

        self.add("rocket",         600, "\x1b[00;91;103m","🚀")
        self.add("party",          601, "\x1b[00;91;103m","🎉")
        self.add("cross",          602, "\x1b[00;91;103m","❌")
        self.add("check",          603, "\x1b[00;91;103m","✅")
        self.add("closedfolder",   604, "\x1b[00;91;103m","📁")
        self.add("openfolder",     604, "\x1b[00;91;103m","📂")
        self.add("tools",          605, "\x1b[00;91;103m","🛠 ")
        self.add("explanationmark",606, "\x1b[00;91;103m","❗️")
        self.add("warningsign",    607, "\x1b[00;91;103m","⚠️")
        self.add("infosign",       608, "\x1b[00;91;103m","ℹ️")
        self.add("music",          609, "\x1b[00;91;103m","🎵")
        self.add("magnifierleft",  610, "\x1b[00;91;103m","🔍")
        self.add("magnifierright", 611, "\x1b[00;91;103m","🔎")
        self.add("pipe",           612, "\x1b[00;91;103m","🐛")
        self.add("microscope",     613, "\x1b[00;91;103m","🔬")
        self.add("telescope",      614, "\x1b[00;91;103m","🔭")
        self.add("fastforward",    615, "\x1b[00;91;103m","⏩")
        self.add("fastforward2",    616, "\x1b[00;91;103m","⏩    ✓")

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

        
        """
        ⚠️ Status & Severity
        • 	ℹ (U+2139) — Information symbol
        • 	⚠ (U+26A0) — Warning sign
        • 	✖ (U+2716) — Heavy multiplication X (error)
        • 	‼ (U+203C) — Double exclamation mark (critical)
        • 	❗ (U+2757) — Heavy exclamation mark
        • 	❌ (U+274C) — Cross mark (failure)
        • 	✔ (U+2714) — Heavy check mark (success)
        • 	✅ (U+2705) — Green check mark (success, emoji style)

        🛠 Debugging & Process
        • 	… (U+2026) — Ellipsis (ongoing process)
        • 	▶ (U+25B6) — Black right-pointing triangle (start/run)
        • 	⏸ (U+23F8) — Pause symbol
        • 	⏹ (U+23F9) — Stop symbol
        • 	🔍 (U+1F50D) — Magnifying glass (search/debug)
        • 	🛠 (U+1F6E0) — Hammer and wrench (setup/config)

        📊 Data & Flow
        • 	→ (U+2192) — Right arrow (flow, next step)
        • 	⇒ (U+21D2) — Double arrow (result, implication)
        • 	↔ (U+2194) — Left-right arrow (exchange)
        • 	⤴ (U+2934) — Arrow pointing up then right (return)
        • 	⤵ (U+2935) — Arrow pointing down then left (exit)

        🔒 Security & Access
        • 	🔒 (U+1F512) — Lock (secure)
        • 	🔓 (U+1F513) — Unlock (open access)
        • 	🔑 (U+1F511) — Key (credentials)
        • 	🛡 (U+1F6E1) — Shield (protection)

        🧭 Miscellaneous Useful Symbols
        • 	★ (U+2605) — Black star (highlight)
        • 	☆ (U+2606) — White star (optional/secondary)
        • 	☑ (U+2611) — Ballot box with check
        • 	☠ (U+2620) — Skull and crossbones (fatal error)
        • 	⏱ (U+23F1) — Stopwatch (timing)
        • 	📦 (U+1F4E6) — Package (deployment, build)
        • 	📝 (U+1F4DD) — Memo (notes, config
        """


    # -----------------------------------------------------------------
    def show_all_levels(logger):

        # logger = logging.getLogger("MikesToolsLibrary")
        # logger = logging.getLogger()


        logger.debug('This message should go to the log file level 10uuuuuuuu')
        logger.info('So should this level 20uuuuuuuuu')
        logger.warning('And this, too level 30uuuuuuuuuuu')
        ### logger.warn('And this, too just warn not warning')
        logger.error('test error level level 40uuuuuuuuuuuuuuuuuu')
        logger.critical('test critical error level 50uuuuu')

        logger.query('test of query 55')

        logger.notice("This is a NOTICE messageuuuuuuuuuuuuuuuuu❌❌❌❌")

        logger.success("test of success 91")
        logger.success()
        self.add("SUCCESS", 91,  "", "✔")
        self.add("FAILURE", 92, "", "❗❌")


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
        logger.mark("")
        logger.mark1("")

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
        logger.fastforward      ("test of telescope     615")

        logger.fastforward2      ("test of telescope     616")

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


    # -----------------------------------------------------------------
    def show_possible_colors():
        for level_num, color in CustomFormatter.COLORS.items():
            print(f"Level {level_num}: Color: {repr(color)}")
        attribs ={ '00': 'Normal', '01':'Bold', '04':'Underlined', '05':'Blinking', '07':'Reversed', '08':'Concealed'}
        foreground = {'30':'black' , '31':'red','32':'green', '33':'orange', '34':'blue', '35':'purple', '36':'cyan', '37':'grey',
            '90':'dark grey','91':'light red','92':'light green', '93':'yellow', '94':'light blue', '95':'light purple',
            '96':'turquoise', '97':'bright white'}
        background = {'40':'black' , '41':'red','42':'green', '43':'orange', '44':'blue', '45':'purple', '46':'cyan', '47':'grey',
            '100':'dark grey','101':'light red','102':'light green', '103':'yellow', '104':'light blue', '105':'light purple',
            '106':'turquoise', '107':'bright white'}

        """ shows all the different combinations of attributes, foreground colors, and background colors """
    
        for b,bv in background.items():
            for f, fv in foreground.items():
                for a,av in attribs.items():
                    print (f"\x1b[0m  \033[{a};{f};{b}m ...A...{fv} on {bv} background with atrrib {av}      AaBbQrStUvWxYz--xxx {a};{f};{b} \033[0m ")

# -----------------------------------------------------------------

# =================================================================
## from https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
## -----------------------------------------------------------------
##
## also from https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
## from https://azrael.digipen.edu/~mmead/www/mg/ansicolors/index.html
##             ESC[1;37;44mBright white on blueESC[0m
##
##   Attributes	      Foreground color	Background color
##                      30 = black           40 = black
##   00 = normal        31 = red             41 = red
##   01 = bold          32 = green           42 = green
##   04 = underlined    33 = orange          43 = orange
##   05 = blinking      34 = blue            44 = blue
##   07 = reversed      35 = purple          45 = purple
##   08 = concealed     36 = cyan            46 = cyan
##                      37 = grey            47 = white (grey)
##
##                      90 = dark grey       100 = dark grey
##                      91 = light red       101 = light red
##                      92 = light green     102 = light green
##                      93 = yellow          103 = yellow
##                      94 = light blue      104 = light blue
##                      95 = light purple    105 = light purple
##                      96 = turquoise       106 = turquoise
##                      97 = bright White    107 = bright white
##
##
# -----------------------------------------------------------------

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------

    # -----------------------------------------------------------------
