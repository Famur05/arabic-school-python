from datetime import timedelta
from authx import AuthX, AuthXConfig
from app.config.settings import settings

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
config.JWT_ALGORITHM = settings.JWT_ALGORITHM
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False

auth = AuthX(config=config)
