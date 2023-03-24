import sys
from pathlib import Path

from environs import Env
from loguru import logger as log


env = Env()

for i in Path.cwd().glob('envs/*.env'):
    if i.name == '.env':
        path = i
        break
else:
    log.error("No .env file found in envs/")
    sys.exit(1)

env.read_env(path=str(path))
