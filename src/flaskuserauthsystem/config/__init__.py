import sys
from pathlib import Path

from environs import Env
from loguru import logger as log


env = Env()

log.debug(Path.cwd())
for i in Path.cwd().glob('envs/*.env'):
    if i.name == '.env':
        path = i
        break
else:
    log.error("No .env file found")
    sys.exit(1)

log.debug(f"Loading environment from {path}")
env.read_env(path=str(path))
