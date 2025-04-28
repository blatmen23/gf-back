from pydantic import BaseModel, PostgresDsn, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class TgBot(BaseModel):
    token: str
    admin_id: int


class Scraper(BaseModel):
    connection_timeout: float
    max_pool_size: int
    time_delta: float
    time_delta_after_exception: float
    recursion_limit: int
    max_exception_counter: int


class Proxy(BaseModel):
    type: str
    username: str
    password: str
    address: str
    url: AnyUrl  # {TYPE}://{USERNAME}:{PASSWORD}@{ADDRESS}


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="GF__"
    )

    proxy: Proxy
    tg_bot: TgBot
    db: DatabaseConfig
    scraper: Scraper = Scraper(
        connection_timeout=5.5,
        max_pool_size=16,
        time_delta=1.,
        time_delta_after_exception=12,
        recursion_limit=3,
        max_exception_counter=100
    )


settings = Settings()
