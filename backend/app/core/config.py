from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sellince Backend"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: str = "http://localhost:3000"
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: str = "lax"
    SQL_ECHO: bool = False

    model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
)
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
