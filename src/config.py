from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_NAME: str

    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_USER: str
    RABBIT_PASSWORD: SecretStr
    RABBIT_VHOST: str = "/"

    @property
    def database_url_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def database_url_psycopg(self):
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def rabbit_url(self):
        return (
            f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASSWORD.get_secret_value()}@"
            f"{self.RABBIT_HOST}:{self.RABBIT_PORT}/{self.RABBIT_VHOST}"
        )

    model_config = SettingsConfigDict(
        env_file=[
            ".env",
            ".env.local",
        ],
    )


settings = Settings()
