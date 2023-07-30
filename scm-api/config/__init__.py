from pydantic_settings import BaseSettings
from pydantic import Field


class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Intro"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = Field(default = "127.0.0.1:27017", env="DB_URL")
    DB_NAME: str = "userbuys"

class KafkaSettings(BaseSettings):
    KAFKA_HOST: str = Field(default = "127.0.0.1:9093", env="KAFKA_HOST")
    KAFKA_TOPIC: str = "mytopic"


class Settings(CommonSettings, ServerSettings, DatabaseSettings, KafkaSettings):
    pass


settings = Settings()
