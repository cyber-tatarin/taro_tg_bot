import logging
import os

from openai.types import ChatModel
from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

env_path = os.path.join("src", "data", ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="forbid", env_file=env_path, env_file_encoding="utf-8"
    )

    # API TOKENS
    TELEGRAM_API_TOKEN: str
    # OPENAI_API_KEY: str
    GSHEETS_JSON_PATH: str = os.path.join("src", "data", "gsheets_key.json")
    OPENAI_API_KEY: str
    OPENAI_MODEL: ChatModel = 'gpt-4o'
    # OPENAI_MODEL: ChatModel = 'gpt-3.5-turbo'
    # DEV SETTINGS
    # DEV_USER_ID: int

    # # POSTGRESQL DATABASE FIELDS
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def SYNC_DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # REDIS DATABASE FIELDS
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASS: str
    REDIS_FSM_DB_NUMBER: int = 0
    # REDIS_FSM_UTIL_NUMBER: int = 1

    @property
    def REDIS_BASE_URL(self) -> str:
        return F'redis://:{self.REDIS_PASS}@{self.REDIS_HOST}:'\
            f'{self.REDIS_PORT}/'

    @property
    def REDIS_FSM_URL(self) -> RedisDsn:
        return f'{self.REDIS_BASE_URL}/{self.REDIS_FSM_DB_NUMBER}'
    
    # REMINER1_SECONDS: int = 60*60*0.5
    # REMINER2_SECONDS: int = 60*60*1.5
    # REMINER3_SECONDS: int = 90*60*3
    
    REMINER1_SECONDS: int = 30
    REMINER2_SECONDS: int = 60
    REMINER3_SECONDS: int = 90
    # recommendation_hour: 1
    # recommendation_minute: 0
    # moon_data_hour: 1
    # moon_data_minute: 0
    
    recommendation_hour: int = 14
    recommendation_minute: int = 55
    moon_data_hour: int = 14
    moon_data_minute: int = 55
    
    first_advise_seconds: int = 15
    
    # days_to_send: 30
    days_to_send: int = 3
    admin_tg: str
    admin_tg_link: str
    
    # @property
    # def admin_tg_link(self) -> str:
    #     return self.admin_tg_link_raw.replace(".", "\\.")
    # @property
    # def REDIS_UTIL_URL(self) -> RedisDsn:
    #     return f'{self.REDIS_BASE_URL}/{self.REDIS_FSM_UTIL_NUMBER}'

settings = Settings(_env_file=env_path, _env_file_encoding="utf-8")
