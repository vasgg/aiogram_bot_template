from functools import cache
from pathlib import Path
import tomllib

from pydantic import BaseModel, ConfigDict, SecretStr, ValidationError

from bot.enums import Stage

DEFAULT_CONFIG_PATH = Path("config.toml")


class BotConfig(BaseModel):
    admin: int
    token: SecretStr
    stage: Stage

    model_config = ConfigDict(extra="forbid")


class RedisConfig(BaseModel):
    url: SecretStr

    model_config = ConfigDict(extra="forbid")


class DBConfig(BaseModel):
    user: str
    password: SecretStr
    host: str
    port: int
    name: str
    echo: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def pg_dsn(self) -> SecretStr:
        return SecretStr(
            f"postgresql+asyncpg://" f"{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
        )

    model_config = ConfigDict(extra="forbid")


class Settings(BaseModel):
    bot: BotConfig
    redis: RedisConfig
    db: DBConfig

    model_config = ConfigDict(extra="forbid")


def resolve_config_path(config_path: str | Path | None = None) -> Path:
    path = Path(config_path or DEFAULT_CONFIG_PATH).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def load_settings(config_path: str | Path | None = None) -> Settings:
    path = resolve_config_path(config_path)
    try:
        with path.open("rb") as config_file:
            raw_settings = tomllib.load(config_file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Config file '{path}' was not found. Copy 'config.toml.example' to 'config.toml' and update the values."
        ) from exc
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"Failed to parse config file '{path}': {exc}") from exc

    try:
        return Settings.model_validate(raw_settings)
    except ValidationError as exc:
        raise ValueError(f"Invalid config file '{path}':\n{exc}") from exc


@cache
def _get_settings_cached(config_path: Path) -> Settings:
    return load_settings(config_path)


def get_settings(config_path: str | Path | None = None) -> Settings:
    return _get_settings_cached(resolve_config_path(config_path))
