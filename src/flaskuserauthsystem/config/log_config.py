import logging

from loguru import logger as log


def configure_logging(debug: bool = False, testing: bool = False) -> None:
    # Remove existing Loguru handlers
    log.remove()

    try:
        log.level('STATIC', no=9, color='<blue><bold>')
    except TypeError:
        log.debug('STATIC level already exists')

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            logger_opt = log.opt(depth=6, exception=record.exc_info, colors=True)
            message = record.getMessage() if not record.args else ' '.join(record.args)
            if '/static/' in message:
                logger_opt.log("STATIC", message)
            else:
                logger_opt.log(record.levelname, message)

    # Create a logger object for the logging standard library
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.NOTSET)

    log.add(
        logging.StreamHandler(),
        level='DEBUG' if debug else 'INFO',
        colorize=True,
        backtrace=debug,
        diagnose=debug,
        enqueue=True,
        catch=True,
    )

    log.add(
        'logs%s/{time:DD-MMM_HH:mm:ss.SSS}_err.log' % ('_test' if testing else ''),
        level='ERROR',
        colorize=False,
        backtrace=debug,
        diagnose=debug,
        enqueue=True,
        catch=True,
        delay=True,
        rotation='100 MB',
        retention='1 months',
        compression='zip',
    )

    if debug:
        log.add(
            'logs%s/{time:DD-MMM_HH:mm:ss.SSS}_deb.log' % ('_test' if testing else ''),
            level='DEBUG',
            colorize=False,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            catch=True,
            delay=True,
            retention='3 days',
        )

        log.add(
            'logs%s/{time:DD-MMM_HH:mm:ss.SSS}_trace.log' % ('_test' if testing else ''),
            level='TRACE',
            colorize=False,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            catch=True,
            delay=True,
            retention='3 days',
        )
