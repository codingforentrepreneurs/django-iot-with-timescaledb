from pathlib import Path
from functools import lru_cache
from decouple import Config, RepositoryEnv

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR_ENV = BASE_DIR / '.env'
REPO_DIR = BASE_DIR.parent
REPO_DIR_ENV = BASE_DIR / '.env'
REPO_DIR_WEB_ENV = BASE_DIR / '.env.web'


@lru_cache
def get_config():
    if BASE_DIR_ENV.exists():
        return Config(RepositoryEnv(str(BASE_DIR_ENV)))
    elif REPO_DIR_WEB_ENV.exists():
        return Config(RepositoryEnv(str(REPO_DIR_WEB_ENV)))
    elif REPO_DIR_ENV.exists():
        return Config(RepositoryEnv(str(REPO_DIR_ENV)))
    from decouple import config
    return config


config = get_config()