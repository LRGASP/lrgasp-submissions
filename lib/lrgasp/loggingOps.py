"""
Operations associated with logging
"""
import logging
import os
import sys
from logging.handlers import SysLogHandler


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


def setupLogger(handler, formatter=None):
    """add handle to logger and set logger level to the minimum of it's
    current and the handler level.  Returns logger."""
    logger = logging.getLogger()
    if handler.level is not None:
        logger.setLevel(min(handler.level, logger.level))
    logger.addHandler(handler)
    if formatter is not None:
        handler.setFormatter(formatter)
    return logger

def setupStreamLogger(fh, level, formatter=None):
    "Configure logging to a specified open file.  Returns logger."
    handler = logging.StreamHandler(stream=fh)
    handler.setLevel(_convertLevel(level))
    return setupLogger(handler, formatter)


def setupStderrLogger(level, formatter=None):
    "configure logging to stderr  Returns logger."
    return setupStreamLogger(sys.stderr, _convertLevel(level), formatter)


def getSyslogAddress():
    """find the address to use for syslog"""
    for dev in ("/dev/log", "/var/run/syslog"):
        if os.path.exists(dev):
            return dev
    return ("localhost", 514)


def setupSyslogLogger(facility, level, prog=None, address=None, formatter=None):
    """configure logging to syslog based on the specified facility.  If
    prog specified, each line is prefixed with the name.  Returns logger."""
    if address is None:
        address = getSyslogAddress()
    handler = SysLogHandler(address=address, facility=facility)
    # add a formatter that includes the program name as the syslog ident
    if prog is not None:
        handler.setFormatter(logging.Formatter(fmt="{} %(message)s".format(prog)))
    handler.setLevel(level)
    return setupLogger(handler, formatter)


def setupNullLogger(level=None):
    "configure discard logging.  Returns logger."
    handler = logging.NullHandler()
    if level is not None:
        handler.setLevel(_convertLevel(level))
    return setupLogger(handler)


def addCmdOptions(parser):
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
    parser.add_argument("--logLevel", type=validateLevel,
                        help="Set level to case-insensitive symbolic value, one of {}".format(", ".join(getLevelNames())))
    parser.add_argument("--logConfFile",
                        help="Python logging configuration file, see logging.config.fileConfig()")


def setupFromCmd(opts, prog=None):
    """configure logging based on command options. Prog is used it to set the
    syslog program name. If prog is not specified, it is obtained from sys.arg.

    N.B: logging must be initialized after daemonization
    """
    if prog is None:
        prog = os.path.basename(sys.argv[0])
    level = _convertLevel(opts.logLevel) if opts.logLevel is not None else logging.INFO
    if opts.syslogFacility is not None:
        setupSyslogLogger(opts.syslogFacility, level, prog=prog)
    if (opts.syslogFacility is None) or opts.logStderr:
        setupStderrLogger(level)
    if opts.logConfFile is not None:
        logging.config.fileConfig(opts.logConfFile)
