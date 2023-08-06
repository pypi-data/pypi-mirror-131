uologging is a solution for configuring Python's built-in logging module.

> A full example is provided in the docstring for `uologging.init_console_logging()`.


## Configuring `logging` via `uologging`

The verbosity_flag can be gathered via argparse using uologging.get_default_parser():

    import uologging
    import argparse
    parser = argparse.ArgumentParser(parents=[uologging.get_default_parser()])
    args = parser.parse_args(['-vv'])

Now, call uologging.init_console_logging() with that verbosity_flag for YOUR package:

    uologging.init_console_logging(mypackage, args.verbosity_flag)

### Default Log Level

Per Python logging suggestion: WARNING, ERROR, and CRITICAL messages are all logged by default.
Meanwhile, INFO and DEBUG messages can be enabled by providing `verbosity_flag` of 1 or 2 to `uologging.init_console_logging()`.

## `logging` Best Practices

Use the Python logging package per the following best practices:

* `logger = logging.getLogger(__name__)` to get the logger for each module/script.
* Use `logger.debug()`, `logger.info()`, `logger.warning()`, etc to add tracing to your modules/packages/scripts.


A trivial example demonstrating best practices:

    # hello.py
    import logging

    logger = logging.getLogger(__name__)

    def hello():
        logger.debug('About to say "hello!"')
        print('hello!')
        logger.debug('Said "hello!"')
