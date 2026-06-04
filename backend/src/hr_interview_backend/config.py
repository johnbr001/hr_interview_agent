from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://hr:hr_secret@localhost:5432/hr_interview"
    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "default"
    temporal_task_queue: str = "hr-interview"
    rag_upload_dir: str = "./data/uploads"
    cors_origins: str = "http://localhost:5173"


settings = Settings()
