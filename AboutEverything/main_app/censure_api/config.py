from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CENSURED_API: str
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
