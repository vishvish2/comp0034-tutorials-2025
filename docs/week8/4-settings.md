# 4. Managing secret/private settings

Your app may need to settings that should be kept private, e.g., database credentials, secret keys
for authentication.

Do not put these in GitHub where others can see them; instead save them to an environment variables,
`.env` file. and load the values in the app

Environment variables are widely used, not just by Python apps
For FastAPI use Pydantic Settings to manage configuration from values in a .env file

## Pydantic settings with .venv

Install Pydantic Settings and dotenv, e.g. `pip install pydantic-settings python-dotenv`

Create a filed named just `.env` in the root of the project with the database details. Uou could
also add environment configuration and use that to configure logging:

```text
# Database
DB_DRIVER=sqlite:///
DB_NAME=paralympics.db

# Environment configuration
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

Create a `/core/config.py` module with a Settings class in your FastAPI app. This will read values
from the `.env` file.

```python
import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    db_name: str
    db_driver: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return f"{self.db_driver}{BASE_DIR}/src/data/{self.db_name}"


def get_settings():
    settings = Settings()
    return settings
```

Read values from the settings in your app. For example, modify the database code in
`/core/db.py` to use the `database_url` property:

```python
from sqlmodel import create_engine
from backend.core.config import get_settings

# Original code
# sqlite_file = resources.files(data).joinpath("paralympics.db")
# sqlite_url = f"sqlite:///{sqlite_file}"

# Updated to use settings class and .env file, converted to function to allow lazy loading
def get_engine():
    settings = get_settings()
    connect_args = {"check_same_thread": False}
    engine = create_engine(settings.database_url, connect_args=connect_args, echo=True)
    return engine
```

Note: if you choose to complete the optional authentication activity in the next activity you will
need to edit the `.env` and `config.py` files.

## Settings for multiple environments
Often you will want different settings for different environments, e.g. development, testing, and
production. A common pattern is to have different configurations for each.

There are different solutions for this, however a common pattern is to define a base settings class
with attributes that are common to all environments and inherit this class to create variants for
the different environments, much as you did with the Pydantic schemas and SQLmodel model classes.

For example, the following version allows for different secret keys and database names in each
environment. Only development and testing are needed for this project.

```python
from __future__ import annotations

import os
import secrets
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class SettingsBase(BaseSettings):
    """ Settings class with values for all environments"""
    db_name: str
    db_driver: str
    algorithm: str
    access_token_expires: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        db_path = BASE_DIR / "src" / "data" / self.db_name
        return f"{self.db_driver}{db_path}"


class SettingsDevelopment(SettingsBase):
    """ Settings class with values for development environment"""
    db_name: str
    secret_key: str = secrets.token_urlsafe(32)


class SettingsTest(SettingsBase):
    """ Settings class with values for the testing environment"""
    db_name: str = Field(validation_alias="test_db")
    secret_key: str = "some-other-super-secret-key-for-testing"



@lru_cache()
def get_settings() -> SettingsBase:
    """Return settings class from environment with a development fallback.

    @lru_cache() caches the settings so it is only created once per process.
    """
    env = (os.getenv("ENV") or os.getenv("ENVIRONMENT") or "development").lower()
    mapping = {
        "development": SettingsDevelopment,
        "testing": SettingsTest,
    }
    # mapping.get(env, SettingsDevelopment) returns a class, the final () instantiates that class.
    return mapping.get(env, SettingsDevelopment)()
```

You can then use the settings in the code, for 



[Next activity](5-auth.md)
