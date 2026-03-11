# 3. Logging and custom errors

Much of this topic has already been covered and is not repeated here:

- Log errors (COMP0035)
- Try/catch (COMP0035)
- Raise HTTP Exceptions (COMP0034 Week 6)

This activity focuses only on the new elements specific to FastAPI:

- Customise error handlers, e.g. 500 Internal Server error
- Custom error types, e.g. for specific business logic

FastAPI automatically handles validation errors, but may want need to return custom errors:

- Customise error handlers, e.g. 500 Internal Server error
- Custom error types, e.g. for specific business logic

The [FastAPI handling errors documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/?h=errors)
these.

## Logging errors

This was covered in COMP0035. Remember to configure the logging before starting the app.

One way to do this is to add the code to `main.py` on startup. You can then log events and errors in
your code.

```python
import logging

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "paralympicsapp.log"

# Configure logging to file and terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Async lifespan even though the routes are sync—this is fine.
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events.

    Handles startup and shutdown events for the FastAPI application.
    On startup, initializes the database by creating tables if they don't exist.

    Args:
        app: The FastAPI application instance.

    Yields:
        None:
    """
    # Startup: creates the database
    with Session(engine) as session:
        # Use the logger, e.g. to record a system event or error
        logger.info("Initializing database...")
        init_db(session)
    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Application shutting down...")
```

## Handling HTTP errors in routes

You have already seen how to raise exceptions in routes, e.g.

```python
def get_games_by_id(session: SessionDep, games_id: int) -> Games:
    """ Method to retrieve a game by its ID.
    Args:
        session: SQLModel session
        games_id: Games.id

    Returns:
        Games: Paralympic Games object

    Raises:
        HTTPException 404 Not Found
        """
    result: Optional[Games] = session.get(Games, games_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Games with id {games_id} not found")
    return result
```

See the [documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/?h=errors) also.

## Customising errors

You can both create a custom error specific to your app, and also customise how errors are handled.

By default, FastAPI catches exceptions that bubble up and returns a JSON response:

`{"detail": "Internal Server Error"}`

You may want to customise this with more specific detail for your app.

For example, this creates a handler for 500 Internal Server messages that has a customised message
and uses the logger to record the error. You could add this to `main.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Paralympics API")


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    # Log the error details for debugging purposes
    logger.error(f"Server error occurred: {exc}")
    # Return a user-friendly error response
    return JSONResponse(status_code=500,
                        content={"message": "Internal server error. Please try again later."}
                        )
```

The paralympics app doesn't include any custom errors so the following is from the FastAPI
documentation.

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

If you look at the following example repos in GitHub you can see how others handle custom errors for
their apps:

- [Orchestra tutorial](https://www.getorchestra.io/guides/fastapi-mastering-error-handling-with-examples)
- [Ssali Jonathan - GitHub](https://github.com/jod35/fastapi-beyond-CRUD/blob/main/src/errors.py)
- [Arjan Code - GitHub](https://github.com/ArjanCodes/examples/tree/main/2024/tuesday_tips/fastapi_custom_exceptions/skypulse/app)

[Next activity](4-settings.md)