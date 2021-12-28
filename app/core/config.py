from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    PROJECT_NAME: str = "Book Store App"
    DATABASE_URL: str = Field(env="database_url")
    TEST_DATABASE_URL: str = Field(env="test_database_url")
    BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
