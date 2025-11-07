# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # or "allow" if you want to keep unknowns
    )

    # Accept DATABASE_URL or database_url
    database_url: str = Field(..., validation_alias=AliasChoices("DATABASE_URL", "database_url"))
    # require | disable | verify-full
    db_ssl_mode: str = Field("require", validation_alias=AliasChoices("DB_SSL_MODE", "db_ssl_mode"))

    # NEW: include your JWT settings so they’re not “extra”
    jwt_secret: str = Field("change_me", validation_alias=AliasChoices("JWT_SECRET", "jwt_secret"))
    jwt_alg:    str = Field("HS256",    validation_alias=AliasChoices("JWT_ALG", "jwt_alg"))

settings = Settings()
