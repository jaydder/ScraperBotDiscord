from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DISCORD_TOKEN: str
    OWNER_ID: int
    GUILD_ID: int
