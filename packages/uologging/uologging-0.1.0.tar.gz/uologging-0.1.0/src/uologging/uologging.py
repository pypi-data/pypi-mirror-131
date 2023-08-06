import logging
import argparse


_logging_format = logging.Formatter(
    '%(asctime)s -- %(name)s [%(levelname)s] %(message)s')


def add_verbosity_flag(parser: argparse.ArgumentParser):
    """Add a --verbose/-v flag to an argparse.ArgumentParser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to be updated.

    Example:
        This should be invoked like the following:
        >>> import uologging
        >>> import argparse
        >>> parser = argparse.ArgumentParser()
        >>> uologging.add_verbosity_flag(parser)

        When parsing args, the verbosity_flag will be set if --verbose/-v is passed!
        >>> args = parser.parse_args(['-vv'])
        >>> args.verbosity_flag
        2

        The verbosity_flag is intended to be used as input for init_console_logging().
    """
    parser.add_argument(
        '-v', '--verbose',
        dest='verbosity_flag',
        action='count',
        default=0,
        help='Logging verbosity. "-vv" results in maximum logging.'
    )


def get_default_parser():
    """Provides an argparse ArgumentParser configured to take --verbose flag.

    Returns:
        argparse.ArgumentParser: Provides a --verbose/-v flag. Should be used as a 'parent parser.'

    Example:
        This should be invoked like the following:
        >>> import uologging
        >>> import argparse
        >>> parser = argparse.ArgumentParser(parents=[uologging.get_default_parser()])

        The parser has been configured with the uologging default_parser as a parent parser.
        When parsing args, the verbosity_flag will be set if --verbose/-v is passed!
        >>> args = parser.parse_args(['-vv'])
        >>> args.verbosity_flag
        2

        The verbosity_flag is intended to be used as input for init_console_logging().
    """
    parser = argparse.ArgumentParser(add_help=False)
    add_verbosity_flag(parser)
    return parser


def init_console_logging(package, verbosity_flag: int = 0):
    """Setup logging to be output to the console.

    Args:
        package (module): The package you are interested in tracing.
        verbosity_flag (int, optional): Higher number means more logging [0,2]. 
            Max is 2 (show DEBUGs, INFOs, WARNINGs, ERRORs, CRITICALs). 
            Default is 0 (show WARNINGs, ERRORs, CRITICALs).

    Example:
        The verbosity_flag can be gathered via argparse using get_default_parser:
        >>> import uologging
        >>> import argparse
        >>> parser = argparse.ArgumentParser(parents=[uologging.get_default_parser()])
        >>> args = parser.parse_args(['-vv'])
        >>> args.verbosity_flag
        2

        Now, init_console_logging with that verbosity_flag for YOUR package (replace "uologging" with the package that you want to trace):
        >>> uologging.init_console_logging(uologging, args.verbosity_flag)
    """
    _setup_console_logging(package)
    set_logging_verbosity(package, verbosity_flag)


def set_logging_verbosity(package, verbosity_flag: int = 0):
    """Set the logging verbosity for this entire package, via the root logger.

    Args:
        package (module): The package you are interested in tracing.
        verbosity_flag (int): Higher number means more logging. Default to WARNING.
    """
    root_logger = _get_root_logger(package)
    if verbosity_flag == 1:
        root_logger.setLevel(logging.INFO)
    elif verbosity_flag >= 2:
        root_logger.setLevel(logging.DEBUG)
    else:  # Default to WARNING, following Python logging standards
        root_logger.setLevel(logging.WARNING)


def _setup_console_logging(package):
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(_logging_format)
    root_logger = _get_root_logger(package)
    root_logger.addHandler(consoleHandler)


def _get_root_logger(package):
    try:
        package_name = package.__name__
    except AttributeError as e:
        if isinstance(package, str):
            package_name = package
        else:
            raise e
    return logging.getLogger(package_name)
