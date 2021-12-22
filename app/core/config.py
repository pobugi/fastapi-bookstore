from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    PROJECT_NAME: str = "Book Store"
    DATABASE_URL: str = Field(env="database_url")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
