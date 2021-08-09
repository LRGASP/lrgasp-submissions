"""
Operations associated with logging
"""
import logging
import os
import sys
from logging.handlers import SysLogHandler

# setup from command line
_lrgasp_logger = None

def getLrgaspLogger():
    return _lrgasp_logger

def getFacilityNames():
    return tuple(SysLogHandler.facility_names.keys())


def getLevelNames():
    return tuple(sorted(logging._nameToLevel.keys()))


def parseFacility(facilityStr):
    """Convert case-insensitive facility string to a facility number."""
    facility = SysLogHandler.facility_names.get(facilityStr.lower())
    if facility is None:
        raise ValueError("invalid syslog facility: \"{}\"".format(facilityStr))
    return facility


def parseLevel(levelStr):
    "convert a log level string to numeric value"
    level = logging._nameToLevel.get(levelStr.upper())
    if level is None:
        raise ValueError("invalid logging level: \"{}\"".format(levelStr))
    return level


def _convertFacility(facility):
    """convert facility from string to number, if not already a number"""
    return facility if isinstance(facility, int) else parseFacility(facility)


def _convertLevel(level):
    """convert level from string to number, if not already a number"""
    return level if isinstance(level, int) else parseLevel(level)

def _loggerBySpec(logger):
    """Logger maybe a logger, logger name, or None for default logger, returns the
    logger."""
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)
    return logger

def setupLogger(logger, handler, formatter=None, level=None):
    """add handle to logger and set logger level to the minimum of it's current
    and the handler level.  Logger maybe a logger, logger name, or None for
    default logger, returns the logger.

    """
    logger = _loggerBySpec(logger)
    if level is not None:
        logger.setLevel(_convertLevel(level))
    if handler.level is not None:
        logger.setLevel(min(handler.level, logger.level))
    logger.addHandler(handler)
    if formatter is not None:
        handler.setFormatter(formatter)
    return logger

def setupStreamLogger(logger, fh, level, formatter=None):
    """Configure logging to a specified open file.  Logger maybe a logger or
    logger name, returns the logger."""
    level = _convertLevel(level)
    handler = logging.StreamHandler(stream=fh)
    handler.setLevel(level)
    return setupLogger(logger, handler, formatter, level=level)


def setupStderrLogger(logger, level, formatter=None):
    """configure logging to stderr.  Logger maybe a logger, logger name, or
    None for default logger, returns the logger."""
    return setupStreamLogger(logger, sys.stderr, _convertLevel(level), formatter)


def getSyslogAddress():
    """find the address to use for syslog"""
    for dev in ("/dev/log", "/var/run/syslog"):
        if os.path.exists(dev):
            return dev
    return ("localhost", 514)


def setupSyslogLogger(logger, facility, level, prog=None, address=None, formatter=None):
    """configure logging to syslog based on the specified facility.  If prog
    specified, each line is prefixed with the name.  Logger maybe a logger or
    logger name, returns the logger."""
    if address is None:
        address = getSyslogAddress()
    handler = SysLogHandler(address=address, facility=facility)
    # add a formatter that includes the program name as the syslog ident
    if prog is not None:
        handler.setFormatter(logging.Formatter(fmt="{} %(message)s".format(prog)))
    handler.setLevel(level)
    return setupLogger(logger, handler, formatter)


def setupNullLogger(logger, level=None):
    "configure discard logging.  Returns logger."
    handler = logging.NullHandler()
    if level is not None:
        handler.setLevel(_convertLevel(level))
    return setupLogger(logger, handler)


def addCmdOptions(parser, *, defaultLevel=logging.WARN):
    """
    Add command line options related to logging.  None of these are defaulted,
    as one might need to determine if they were explicitly set. The use case
    being getting a value from a configuration file if it is not specified on
    the command line.
    """
    # want to validate name, but want to store the string in the arguments vector
    # rather than the numeric value.
    def validateFacility(facilityStr):
        parseFacility(facilityStr)
        return facilityStr

    def validateLevel(levelStr):
        parseLevel(levelStr)
        return levelStr

    parser.add_argument("--syslogFacility", type=validateFacility,
                        help="Set syslog facility to case-insensitive symbolic value, if not specified, logging is not done to stderr, "
                        " one of {}".format(", ".join(getFacilityNames())))
    parser.add_argument("--logStderr", action="store_true",
                        help="also log to stderr, even when logging to syslog")
    parser.add_argument("--logLevel", type=validateLevel, default=defaultLevel,
                        help="Set level to case-insensitive symbolic value, one of {}".format(", ".join(getLevelNames())))
    parser.add_argument("--logConfFile",
                        help="Python logging configuration file, see logging.config.fileConfig()")
    parser.add_argument("--logDebug", action="store_true",
                        help="short-cut that that sets --logStderr and --logLevel=DEBUG")


def setupFromCmd(opts, *, logger=None, prog=None):
    """configure logging based on command options. Prog is used it to set the
    syslog program name. If prog is not specified, it is obtained from sys.arg.
    Logger maybe a logger, logger name, or None for default logger, returns the logger.

    N.B: logging must be initialized after daemonization
    """
    if opts.logDebug:
        opts.logStderr = True
        opts.logLevel = logging.DEBUG
    if prog is None:
        prog = os.path.basename(sys.argv[0])
    logger = _loggerBySpec(logger)
    level = _convertLevel(opts.logLevel) if opts.logLevel is not None else logging.WARN
    if opts.syslogFacility is not None:
        setupSyslogLogger(logger, opts.syslogFacility, level, prog=prog)
    if (opts.syslogFacility is None) or opts.logStderr:
        setupStderrLogger(logger, level)
    if opts.logConfFile is not None:
        logging.config.fileConfig(opts.logConfFile)
    global _lrgasp_logger
    _lrgasp_logger = logger
    return logger


class StreamToLogger(object):
    """
    File-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass
