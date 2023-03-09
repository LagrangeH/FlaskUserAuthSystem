from loguru import logger as log


log.add(
    'logs/debug.lob',
    level='DEBUG',
    colorize=True,
    backtrace=True,
    diagnose=True,
    enqueue=True,
    catch=True,
)