from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    telegram_bot_token: str
    public_base_url: str = "http://localhost:8000"
    app_name: str = "Nails & Inspiration"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
