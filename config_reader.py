from pydantic_settings import BaseSettings


class Postgres(BaseSettings):
    host: str
    port: int
    db: str
    user: str
    password: str

    def make_connection_string(self) -> str:
        """Function to make a connection string to postgres database."""
        result = (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )
        return result


class Redis(BaseSettings):
    host: str
    port: int
    db: int

    def make_connection_string(self) -> str:
        """Function to make a connection string to redis."""
        result = f"redis://{self.host}:{self.port}/{self.db}"
        return result


class Config(BaseSettings):
    postgres: Postgres
    redis: Redis

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "_"


def load_config(env_file=".env") -> Config:
    """Load config from env file."""
    config = Config(_env_file=env_file)  # type: ignore
    return config
