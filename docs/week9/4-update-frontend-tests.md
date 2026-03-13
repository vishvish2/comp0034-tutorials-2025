# 4. Update the fixtures for the frontend tests

You have not changed the front end app so the tests in principle are still valid.

However, the fixtures that create the live FastAPI server for the front end tests need to be
changed to use the new backend app.

If you have not already, then copy the tests created in week 5 into the `tests/frontend` directory.

## Fixtures in conftest.py

First, make sure you understand the differences between the files that contain the fixtures.

You now have 3 conftest.py files with different fixtures:

- `tests/conftest.py` at the top of the test directory tree that all test modules will use. This has
  the fixture that clears the settings cache and ensure that the test settings are used.
- `tests/backend/conftest.py` that the backend tests will use. This has the session and test client
  fixtures you just created.
- `tests/backend/conftest.py` that the frontend tests will use. This has the fixtures to run the
  FastAPI backend and the Streamlit frontend apps for the playwright tests.

Using multiple `conftest.py` files is appropriate. Fixtures are inherited through the hierarchy.

Tests in `tests/backend/` see:

- Fixtures from tests/backend/conftest.py
- Fixtures from tests/conftest.py

Tests in `tests/frontend/` see:

- Fixtures from tests/frontend/conftest.py
- Fixtures from tests/conftest.py

Neither backend nor frontend tests see the other folder's fixtures:

- Backend tests do not see frontend fixtures.
- Frontend tests do not see backend fixtures.

## Modify the front end fixtures

Your fixtures may be different. The following is my example.

The changes are:

- Add `from backend.core.config import get_settings`
- `def api_session_fixture(set_test_env):` uses the `set_test_env` fixture from
  `backend/conftest.py`
- Use the settings to get the database url in the `api_session_fixture`:

    ```python
    settings = get_settings()  # add this
    engine = create_engine(
        settings.database_url,  # modify this to use the url from settings
    ```

There is code duplication as the `api_session_fixture` has session scope, and the similar
`backend/contest.py::session` fixture does the same but has a function scope.

```python
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Generator
from urllib.request import urlopen

import pytest
import sqlalchemy as sa
import uvicorn
from sqlmodel import Session, select, SQLModel, StaticPool, create_engine
from streamlit.testing.v1 import AppTest

from backend.core.config import get_settings
from backend.core.db import add_data
from backend.core.deps import get_db
from backend.main import create_app
from backend.models.models import Games


def wait_for_http(url, timeout=10, process=None):
    start = time.time()
    while True:
        if process is not None and process.poll() is not None:
            raise RuntimeError(f"Server process exited early with code {process.returncode}")
        try:
            urlopen(url, timeout=1)
            return
        except Exception:
            if time.time() - start > timeout:
                raise RuntimeError(f"Server did not start in time: {url}")
            time.sleep(0.1)


@pytest.fixture(name="api_session", scope="session")
def api_session_fixture(set_test_env):
    """ Creates a test database dependency once for the test session.

    Rolls back all transactions at the end of all tests.

    From https://github.com/fastapi/sqlmodel/discussions/940
    """
    settings = get_settings()
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        # echo=True
        # echo=True Added so you can see what is happening when you run tests that use the database
        # you may prefer to set this to False
    )
    SQLModel.metadata.create_all(bind=engine)
    # Add data if empty
    with Session(engine) as session:
        games = session.exec(select(Games)).first()
        if not games:
            add_data(engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    nested = connection.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    engine.dispose()


@pytest.fixture(scope="session")
def api_server(api_session: Session):
    """Start the REST API server before Streamlit tests, using the test DB session."""

    def get_session_override():
        return api_session

    app = create_app()
    app.dependency_overrides[get_db] = get_session_override

    thread = threading.Thread(
        target=uvicorn.run,
        kwargs={
            "app": app,
            "host": "127.0.0.1",
            "port": 8000,
            "reload": False,
        },
        daemon=True,
    )
    thread.start()
    wait_for_http("http://127.0.0.1:8000")
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def app_server(api_server):
    """Start a Streamlit app server for Playwright tests using the subprocess library."""

    project_root = Path(__file__).resolve().parents[2]
    app_path = project_root / "src" / "paralympics" / "paralympics_dashboard.py"
    port = "8501"
    url = f"http://127.0.0.1:{port}"

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            port,
            "--server.headless",
            "true",
        ],
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=os.environ.copy(),
    )

    try:
        wait_for_http(url, process=process)
    except Exception as e:
        stdout, stderr = process.communicate(timeout=2)
        raise RuntimeError(
            "Failed to start Streamlit for Playwright tests. "
            f"Command app path: {app_path}\n"
            f"Exit code: {process.returncode}\n"
            f"STDOUT:\n{stdout}\n"
            f"STDERR:\n{stderr}"
        ) from e

    yield url

    # Clean shutdown
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture(name="at")
def streamlit_app_test_fixture() -> Generator[AppTest, Any, None]:
    project_root = Path(__file__).resolve().parents[2]
    app_file = project_root / "src" / "paralympics" / "paralympics_dashboard.py"
    at = AppTest.from_file(app_file)
    at.run()
    yield at
```

Run the front end tests to check that they still run e.g. `pytest tests/frontend`

Note that if you implemented the authentication last week then the following tests will now fail:

- all tests in `tests/frontend/test_teacher_admin.py`
- `tests/frontend/test_paralympics_playwright.py::test_new_question_submitted`

You can prevent pytest from running these in `pyproject.toml` in the `addopts` like this (you may
already have some options under addopts, if so just add these to the existing list):

```toml
[tool.pytest]
addopts = [
    "--ignore=tests/frontend/test_teacher_admin.py", # skip teacher admin frontend test file, needs to be modified to handle the login
    "--deselect=tests/frontend/test_paralympics_playwright.py::test_new_question_submitted"  # skips just the specified test, not the whole file
]
```

## Check all tests run

You should now be able to run all the tests, e.g. `pytest` should run frontend and backend tests

[Next activity](5-ci.md)