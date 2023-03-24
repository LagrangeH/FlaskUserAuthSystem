import sys

from loguru import logger as log


def configure_logging(debug: bool = False) -> None:
    log.remove()

    log.add(
        sys.stdout,
        level='DEBUG' if debug else 'INFO',
        colorize=True,
        backtrace=debug,
        diagnose=debug,
        enqueue=True,
        catch=True,
    )

    log.add(
        'logs/err_{time:DD-MMM_HH:mm:ss.S}.log',
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
            'logs/deb_{time:DD-MMM_HH:mm:ss.S}.log',
            level='DEBUG',
            colorize=False,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            catch=True,
            delay=True,
            retention='3 days',
        )
