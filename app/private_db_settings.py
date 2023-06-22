import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST_DB: str
    PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = '/code/app/.env'
        env_file_encoding = 'utf-8'

    def init_variables(self):
        for k, v in self.__dict__.items():
            os.environ[k] = v
