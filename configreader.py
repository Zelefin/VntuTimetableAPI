from pydantic_settings import BaseSettings


class Postgres(BaseSettings):
    host: str
    port: int
    db: str
    user: str
    password: str


class Config(BaseSettings):
    postgres: Postgres

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "_"


def load_config(env_file=".env") -> Config:
    config = Config(_env_file=env_file)
    return config
