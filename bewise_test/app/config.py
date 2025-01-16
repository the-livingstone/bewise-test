from starlette.config import Config

config = Config("../.env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

API_HOST: str = config("API_HOST", default="0.0.0.0")
API_PORT: int = config("API_PORT", cast=int, default=8000)

POSTGRES_USER: str = config("POSTGRES_USER")
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD")
POSTGRES_HOST: str = config("POSTGRES_HOST", default="postgres")
POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int, default=5432)
POSTGRES_NAME: str = config("POSTGRES_NAME", default="db")
POSTGRES_MIN_POOL_SIZE: int = config("POSTGRES_MIN_POOL_SIZE", cast=int, default=1)
POSTGRES_MAX_POOL_SIZE: int = config("POSTGRES_MAX_POOL_SIZE", cast=int, default=5)