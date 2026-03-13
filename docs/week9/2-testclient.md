# 2. Using the FastAPI TestClient

In these tests you are testing the FastAPI endpoints (routes) return correct responses and behave
as expected.

FastAPI APIs can be tested using FastAPI's TestClient. TestClient is an HTTPX-based testing utility
that allows you to test API endpoints (routes) without running the server. Remember that when you
tested the Streamlit routes, you created a fixture to run the FastAPI backend server first. The
TestClient removes the need for this when testing the FastAPI endpoints.

You will:

- Create a TestClient
- Create a test function with a name that starts `test_`. Starting the test with `test_` allows
  pytest to automatically recognise that this is a test.
- Use the TestClient to make an http request to a route
- Use the response from the request, and add pyest assertions, for example you can check
    - `response.status_code` to check the HTTP response status
    - `response.json()` to check content in the response body

These tests are integration tests, because they exercise the full request–response cycle of the
app, including routing, dependency injection, validation, and response generation.

If you want to write unit tests, you will need to isolate the routes from dependencies, e.g. using
mocking. Mocking has not been covered in the course though if you search you will find external
tutorials cover this if you want to implement them,
e.g. [example test code using monkeypatch](https://testdriven.io/blog/fastapi-crud/#test)

## Create the first test

This test will verify that when the GET /games endpoint is called, that is return a status of
200 OK. This endpoint is in the module `src/backend/games_router.py`.

The test function will:

- create an instance of the FastAPI test client
- use the test client to make a GET request to `/games` and receive a response
- use pytest assertio to verify that the `.status_code` from the response is equal to 200

Create an appropriate test module, e.g. `tests/backend/test_games_router.py`

Add a test:

```python
from fastapi.testclient import TestClient

from backend.main import app

# Create an instance of the FastAPI test client
client = TestClient(app)


def test_get_games_ok():
    # Use the test client to make a requst to the GET /games endpoint (route)
    response = client.get("/games")
    # Use pytest assertion to verify that the response to the request has a status code of 200
    assert response.status_code == 200, "Should return status code 200"
```

Run the test, e.g. in the terminal enter:

- `pytest` to run all tests
- or `tests/backend/test_quiz_router.py::test_get_games` to run just this test

Check that the test passes.

Note: there was initially an error in `games_service.py` in the method `GamesService.get_games()`.
If your test fails with
`TypeError: GamesService.get_games() takes 1 positional argument but 2 were given` then please edit
that method to add either:

- `def get_games(self, session: SessionDep) -> list[Games]: ...`, or
- `@staticmethod above get_games(...)`

## Add a test for the variable GET route

Using the approach above, create a second test for the route that get a games by `id` where `id=1`.

The endpoint is GET /questions/1

The status code should be 200.

The response `.json().get('id')` should be 1.

Add the test method to the test module you created earlier and run the test.

So you can see what is raised when a test fails, change the request to /questions/2 and run the test
again. It should now fail. Remember to change it back to 1 again as you want the test to pass if the
code is correct.

## Next activity

These tests only read or GET values from the database, they don't alter the state of the database.
The next activity considers how to handle tests that could potentially alter the database state.

[Next activity](3-tests-database.md)