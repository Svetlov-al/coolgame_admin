from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    admin_password: str

    class Config:
        env_file = ".env"

settings = Settings()
