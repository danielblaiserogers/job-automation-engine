from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Automation Engine"
    DATABASE_URL: str = "sqlite:///./jobs.db"
    ADZUNA_APP_ID: str
    ADZUNA_APP_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()