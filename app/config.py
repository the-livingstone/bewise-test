from starlette.config import Config

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
TESTING: bool = config("TESTING", cast=bool, default=False)

API_HOST: str = config("API_HOST", default="0.0.0.0")
API_PORT: int = config("API_PORT", cast=int, default=8000)

DB_URL: str = config("DB_URL", default="sqlite:///db")
