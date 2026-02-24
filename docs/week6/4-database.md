# 4. Configure the database to use within the app

Alembic is a tool to manage changes to the structure of the database tables. It does not make the
database accessible to your FastAPI app.

You now need to configure your app to interact with the database.

## Create the database when the app starts

[FastAPI's lifecycle events](https://fastapi.tiangolo.com/advanced/events/) manage actions on
startup and shutdown of the app.

Their [tutorial section on using SQLModel](https://fastapi.tiangolo.com/tutorial/sql-databases/)
tells you to use `@app.on_event("startup")` however, if you use this you will see a warning that
it has been deprecated, and it will advise you to use lifecycle events instead.

Create a lifecycle event that initialises the database on startup, and adds data to it if it does 
not already exist.

The lifecycle event is shown as an asynchronous function, though you can call synchronous
functions within it.

Add the following code to `main.py` before the line where you create the app instance.

```python
from contextlib import asynccontextmanager
from sqlmodel import Session

from backend.core.db import engine, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events.

    Handles startup and shutdown events for the FastAPI application.
    On startup, initializes the database by creating tables if they don't exist.
    """
    with Session(engine) as session:
        init_db(session)
        yield
```

You also need to modify the app instance to use the lifecycle event.

```python
app = FastAPI(
    title="Paralympics API",
    lifespan=lifespan
)
```

## Module to handle database functions

To avoid `main.py` becoming too large, keep this for creating and configuring the app instance.

In the code you copied at the start, there is a package named `core` with a module named `db.py`.

Open `db.py`. It has:

1. A section that defines the location of the database file and creates a sqlite engine.
2. A function, `init_db` that adds data to the database if it does not already exist.
3. A series of functions adapted from COMP0035 to add the data from the Excel file to the database.

Make sure you read 1 and 2 and understand what the code does.

## Add a Dependency for the session

In COMP0035 you used session to execute SQL statements and commands such as commit and add. You will
use a session to access the database throughout the app code.

[FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) are 'a way for your code
to declare things that it requires to work and use: "dependencies".' Shared database connections are
a common such 'dependency'.

For clear separation of code, create a new module called `dependencies.py` or `deps.py` in the
`core` package.

Add to this file a dependency for the database session. The following creates a dependency called
`get_db`. You can name it anything, `get_db` is used below only for consistency with other tutorials
and examples.

```python
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from backend.core.db import engine


def get_db():
    """ Dependency for database session
    
    Yields:
        session: SQLModel session
        
    Note: you don't need to session.close() as the context manager handles this
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
```

## Check the app runs

You will not see any visible difference to your app from the last three activities. Just check that
it is still running and there are no errors. You may need to check import paths for code you have
copied in case your file and folder structure differs from the copied code.

[Next activity](5-routes.md)