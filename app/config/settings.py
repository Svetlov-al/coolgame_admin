from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    pass

    class Config:
        env_file = ".env"
