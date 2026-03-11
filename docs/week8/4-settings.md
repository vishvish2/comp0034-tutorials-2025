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


settings = Settings()
```

Read values from the settings in your app. For example, modify the database code in
`/core/db.py` to use the `database_url` property:

```python
from sqlmodel import create_engine
from backend.core.config import settings

# Original code
# sqlite_file = resources.files(data).joinpath("paralympics.db")
# sqlite_url = f"sqlite:///{sqlite_file}"

# Updated to use settings class and .env file
connect_args = {"check_same_thread": False}
engine = create_engine(settings.database_url, connect_args=connect_args, echo=True)
```

Note: if you choose to complete the optional authentication activity in the next activity you will
need to edit the `.env` and `config.py` files.

[Next activity](5-auth.md)
