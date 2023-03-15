from loguru import logger as log


def configure_logging(debug: bool = False) -> None:
    if debug:
        log.add(
            'logs/debug.log',
            level='DEBUG',
            colorize=True,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            catch=True,
            delay=False,
        )
