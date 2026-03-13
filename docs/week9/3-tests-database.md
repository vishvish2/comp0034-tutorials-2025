# 3. Rollback of database changes between tests

## Considerations for the database when testing

When you test your application, you don't want to use the live, or production, version of your
database. You want a version for testing. This version may have the same data as the production
version, or it may have just a sample of data entries that are sufficient for testing.

Each time you run the tests you want the results to be the same if the code under test has not
changed. For example, if you run a test that deletes a given item then the next time you run the
tests, that test will fail as it is no longer there.

For these reasons, when you test FastAPI routes that could alter the database state you will
want to create a test client that:

- uses a test version of the database
- rolls back database transactions after each test

## Modify the app to support configurations for different environments

If you have not already done so, then follow the guidance
in [week 8 activity 4](https://github.com/nicholsons/comp0034-tutorials-2025/blob/master/docs/week8/4-settings.md)
to create a`backend/config.py` with the multiple settings classes.
See [example here](https://github.com/nicholsons/comp0034-tutorialapp-fastapi/blob/master/src/backend/core/config.py)
with changes also made to `db.py` to use `get_settings`; and `deps.py` to use `get_engine` rather
than importing an instance of `engine`.

Add another line to the `.env` file for the test database file name:

```text
TEST_DB = test_paralympics.db
```

To ensure that all the tests use the SettingsTest config, you can either set an environment
variable, for example:

Option 1: Set using pytest.ini

1. Install: `pip install pytest-env`
2. Create or edit `pytest.ini` in the project root with the following

```text
[pytest]
env =
    ENV=testing
```

an alternative to the pytest.ini is to update pyproject.toml with:

```toml
[tool.pytest_env]
ENV = "testing"
```

Option 2: Set the environment variable on the comment line when running pytest: `ENV=test pytest`

With either option, you also want to make sure that the setting cache has test settings.

Add a new file `tests/conftest.py`. This file sits above the subdirectories for the frontend and
backend tests. In it add the following fixture:

```python
import os

import pytest

from backend.core.config import get_settings


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    os.environ["ENV"] = "testing"
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
```

## Add a pytest fixture to roll back transactions between tests

A transaction is like a temporary "workspace" inside the database where a group of operations is
treated as a single unit. You can make a number of changes to the database and keep them in this
group, however these are not permanently changed until you **commit** them.

You make the changes, these are stored as a transaction, and then that transaction can either be
committed to permanently save the changes, or as we want, can be rolled back so that the changes
are not saved.

Databases do this as transactions guarantee:

- Either all operations succeed, or none do.
- Your changes aren't visible to other sessions until you commit.
- The database never gets into a half‑updated or corrupted state.
- Once committed, changes survive crashes.

The transaction capability is managed in your code through SQLAlchemy. SQLModel is built on top of
SQLAlchemy, however not all SQLAlchemy functionality is exposed through the SQLModel interface, in
some instances you will need to import the SQLAlchemy functionality directly.

The following pytest fixture code
is [from a discussion in the FastAPI repository](https://github.com/fastapi/sqlmodel/discussions/940),
though you will find other solutions if you search.

Create a new file called `conftest.py` in `tests/backend`.

Add the following code to it. This fixture handles the rollback of the transactions.

```python
import os

import pytest
import sqlalchemy as sa
from backend.core.config import get_settings, get_settings
from backend.core.deps import get_current_user, get_db
from backend.main import create_app
from backend.models.models import User
from sqlmodel import SQLModel, Session, StaticPool, create_engine


# Depends on the set_test_env to start before starting the session_fixture
@pytest.fixture(name="session")
def session_fixture(set_test_env):
    """ Creates a test database dependency.

    Rolls back all transactions after each test.

    From https://github.com/fastapi/sqlmodel/discussions/940

    Note: the test_paralympics.db contains data, if you create an in memory database you will also
    need to seed some sample data for testing.
    """
    settings = get_settings()
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
        # echo=True Added so you can see what is happening when you run tests that use the database
        # you may prefer to set this to False
    )
    SQLModel.metadata.create_all(bind=engine)
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
```

## Create a fixture that configures the test client to use the test database

In your app code you have a database (or session) dependency called `get_db` or `get_session`.

Without changing your app code, you want the tests to get the test database session instead. To do
this you **override the dependency**.

To do this create a test client fixture that uses the session fixture you created above.

```python
@pytest.fixture(name="client")
def client_fixture(session: Session):
    """ Creates a test client that overrides the database dependency.
    
     Code from: https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#client-fixture
     """

    def get_session_override():
        return session

    app = create_app()
    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

## Create a test for a POST route

Now that you have the necessary dependencies, create a test that uses them.

Create a test function for POST /games:

- The test function takes the client fixture as an argument. e.g. `test_post_games_succeeds(client)`
- Create JSON data to create a new games, e.g.

    ```python
    games_data = {
        "event_type": "summer",
        "year": 2060,
    }
    ```
- You pass the `games_data` using the `json` argument e.g. `client.post("/games", json=games_data)`
- Assert that the response code is 201 Created.
- Assert that in the `json` of the response you can get the year which should be 2060.

Run the test. It should pass.

Try adding another test, this time assert that it fails validation when a required parameter is
missing, for example using just this:

    games_data = {
        "event_type": "winter"
    }

Validation errors return status code 422.

## Create delete tests

1. Write a test that deletes the games with id of 1.
2. Write a test that deletes a games with the id of 4057.

The DELETE /games route should respond with 204 No Content for both of the above, i.e. even if there
is no games with that id to delete. If it does not then the delete code has not been correctly 
implemented and needs to be changed.

## Check all your tests run

If you have been running each test individually, Check that all your tests run.


[Next activity](4-update-frontend-tests.md)