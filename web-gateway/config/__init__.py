from pydantic_settings import BaseSettings
from pydantic import Field

class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Intro"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8100


class KafkaSettings(BaseSettings):
    KAFKA_URL: str = Field(default = "127.0.0.1:9093", env = "KAFKA_URL")

class ApiSettings(BaseSettings):
    API_URL: str = Field(default = "http://localhost:8000", env = "API_URL")

class Settings(CommonSettings, ServerSettings, KafkaSettings, ApiSettings):
    pass


settings = Settings()
