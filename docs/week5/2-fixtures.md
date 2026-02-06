# 2. Pytest fixtures to run the apps

Pytest fixtures were introduced in COMP0035.

Common fixtures for use by test modules are placed in `conftest.py`, fixtures can also be placed
within the test modules.

In this activity you will create two fixtures:

1. Fixture to run the REST API app once for the test session
2. Fixture to run the Dash/Flask/Streamlit app once for the test session

Both apps need to be running for the browser tests. You can run them once for all the tests in
that session, or per test function or class.

## Fixture to run the REST API in a thread

The REST API runs with uvicorn:
`uvicorn.run("src.data.api:app", host="127.0.0.1", port=8000, reload=True)`

Note that I renamed `mock_api.py` to `api.y` to avoid confusion (it is not a mock).

When you run the tests, you want the app to be run automatically. The code below runs the 
REST API once for each test session and automatically runs it.

As you need to run two apps, then each will run on their own thread or process. You could use 
`threading`, `multiprocessing` or `processing` for this.

The REST API interacts with a database. You don't want the tests to alter your 'live' database.
You will look at the REST API and how to test using a test database after reading week. The 
following is a more crude solution that simply copies the database at the start of the tests and
replaces it at the end so it is back to the original state. 

```python
@pytest.fixture(scope="session", autouse=True)
def api_server():
    """Start the REST API server before Dash app tests."""

    # Create a copy of the database
    root = Path(__file__).parent.parent
    _orig_db = root.joinpath("src", "data", "paralympics.db")
    _backup_db = _orig_db.with_suffix(_orig_db.suffix + ".orig")

    if not _orig_db.exists():
        raise RuntimeError(f"Original DB not found: {_orig_db}")

    # backup original database
    shutil.copy2(_orig_db, _backup_db)

    # Import the REST API app and run in a thread
    from data.api import app

    thread = threading.Thread(
        target=uvicorn.run,
        kwargs={
            "app": app,
            "host": "127.0.0.1",
            "port": 8000,
            "reload": False
        },
        daemon=True,
    )
    thread.start()

    # Use a helper function to wait for the server to load
    # Alternative use `time.sleep(10)`
    wait_for_http("http://127.0.0.1:8000")

    yield

    # Teardown: restore the original database
    if _backup_db.exists():
        shutil.copy2(_backup_db, _orig_db)
        try:
            _backup_db.unlink()
        except Exception:
            pass
```

## Fixture to run the Dash/Flask/Streamlit app in a thread
This varies by app as the syntax to run the apps is different. You may need to adapt slightly 
if you start your app differently.

### Dash version 
Dash testing provides a fixture that uses threading, called `dash_thread_server`. I've used this in the
code below to simplify the code. You don't have to use the dash_thread_server fixture.

You need to install Dash testing to get the fixture.

`pip install dash[testing]`; or `pip install dash\[testing]` on some Mac shells.


```python
from dash.testing.application_runners import import_app


@pytest.fixture(scope="function")
def app_server(dash_thread_server):
    """ Start the Dash app server using the Dash testing dash_thread_server fixture

    Uses `scope="function"` as the dash_thread_server fixture is function scope
    """
    app = import_app("paralympics.app")
    server = dash_thread_server.start(app, host="127.0.0.1")
    try:
        yield dash_thread_server.url  # you can yield the dash_thread_server and not just the url
    finally:
        dash_thread_server.stop()
```

### Flask version
Note that this uses a config class for the test config. You will need to adapt the code if you
are not using this.

```python
import threading

from paralympics import create_app


@pytest.fixture(scope="session")
def app_server():
    """Start a Flask app server for Playwright tests

     Uses the threading library.
     """
    from paralympics.config import TestingConfig
    from paralympics import create_app

    app = create_app(TestingConfig)

    thread = threading.Thread(
        target=app.run,
        kwargs={'host': '127.0.0.1', 'debug': False, 'use_reloader': False, 'port': 5000},
        daemon=True
    )
    thread.start()

    wait_for_http("http://127.0.0.1:5000")

    yield f"http://127.0.0.1:5000"
```
### Selenium version
```python
import subprocess
import time

import pytest


@pytest.fixture(scope="session")
def app_server():
    """Start a Streamlit app server for Playwright tests using the subprocess library."""

    app_path = "src/paralympics/paralympics_dashboard.py"
    port = "8501"
    url = f"http://127.0.0.1:{port}"

    process = subprocess.Popen([
        *('streamlit', 'run', app_path),
        *('--server.port', port),
        *('--server.headless', 'false'),
    ])

    time.sleep(10)  # give Streamlit some time to start

    yield url

    # Clean up/shutdown        
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
```

[Next activity](3-playwright-tests.md)
