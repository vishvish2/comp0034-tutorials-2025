import subprocess
import time
from pathlib import Path

import pytest
import uvicorn
import shutil
import threading


@pytest.fixture(scope="session", autouse=True)
def api_server():
    """Start the REST API server before app testing."""

    # Create a copy of the database
    root = Path(__file__).parent.parent
    _orig_db = root.joinpath("src", "data", "paralympics.db")
    _backup_db = _orig_db.with_suffix(_orig_db.suffix + ".orig")

    if not _orig_db.exists():
        raise RuntimeError(f"Original DB not found: {_orig_db}")

    # backup original database
    shutil.copy2(_orig_db, _backup_db)

    # Import the REST API app and run in a thread
    from src.data.mock_api import app

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
    # wait_for_http("http://127.0.0.1:8000")
    time.sleep(10)

    yield

    # Teardown: restore the original database
    if _backup_db.exists():
        shutil.copy2(_backup_db, _orig_db)
        try:
            _backup_db.unlink()
        except Exception:
            pass


@pytest.fixture(scope="session")
def app_server():
    """Start a Streamlit app server for Playwright tests using the subprocess
        library."""

    app_path = "src/paralympics/app.py"
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
