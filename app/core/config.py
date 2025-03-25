from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    assistant_id: str
    mongo_db_uri: str
    db_name: str

    # Configuration for loading environment variables
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Create an instance of the Settings class
settings = Settings()
