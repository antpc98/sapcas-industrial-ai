from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SAPCAS Industrial AI"
    app_env: str = "local"
    database_url: str = "postgresql+psycopg://sapcas:sapcas@localhost:5432/sapcas"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
