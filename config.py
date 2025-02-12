from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN_WB: str
    model_config = SettingsConfigDict(env_file=f".env")


# Получаем параметры для загрузки переменных среды
settings = Settings()

