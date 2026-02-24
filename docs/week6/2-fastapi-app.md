# 2. Create and configure a FastAPI app

## Create the app instance

Open and edit `main.py`.

The code to create the instance of the app is similar to creating a Flask or Dash instance:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Paralympics API",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

Add the code above, and then run the app.

In the terminal enter: `fastapi dev src/backend/main.py`

## Configure the app to accept requests from the front end app

CORS (Cross-Origin Resource Sharing) allows your front end app (Flask/Dash/Streamlit) to access
your FastAPI back end app.

To do this
you [configure CORSMiddleware](https://fastapi.tiangolo.com/tutorial/cors/?h=corsmidd#use-corsmiddleware).

Add the following (you can remove URLs from `origins = []` that you don't need).

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Paralympics API",
)

# Allow requests from front end apps running on localhost
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8050",  # dash default
    "http://localhost:5000",  # flask default
    "http://localhost:8501",  # streamlit default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

You won't see any change. Just check that your app is still running.

## Going further

Investigate how to add the database url to an environment file
using [Pydantic settings management](https://fastapi.tiangolo.com/advanced/settings/). Recommended
if you plan to use FastAPI beyond this course.

[Next activity](3-alembic.md)

