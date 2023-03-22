from datetime import datetime

from loguru import logger as log


def configure_logging(debug: bool = False) -> None:
    if debug:
        log.add(
            f'logs/debug_{datetime.utcnow()}.log',
            level='DEBUG',
            colorize=False,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            catch=True,
            delay=True,
        )
