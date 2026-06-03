from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "default"
    temporal_task_queue: str = "hr-interview"
    chroma_persist_dir: str = "./data/chroma"
    rag_upload_dir: str = "./data/uploads"
    brave_api_key: str = ""
    tavily_api_key: str = ""


settings = Settings()
