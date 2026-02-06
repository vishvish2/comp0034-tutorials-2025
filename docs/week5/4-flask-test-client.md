# 4. FLASK: Flask test client

To test the routes of a Flask app you can use a combination of:

- [Flask test client](https://flask.palletsprojects.com/en/3.0.x/testing/#fixtures) which runs a
  test app and allows you to make http requests to routes
- [Pytest](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#choosing-a-test-layout-import-rules)
  for test
  assertions

## Create a Flask test client as a pytest fixture

This is explained with code in
the [Flask documentation](https://flask.palletsprojects.com/en/stable/testing/#fixtures).

The code is shown below.

Add this to `conftest.py`. Note that you need to turn off CSRF protection for the tests.

```python
import pytest
from paralympics import create_app


@pytest.fixture(scope='session')
def app():
    """Create a Flask app configured for testing"""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False
        }
    )
    yield app


@pytest.fixture(scope="session")
def client(app):
    """ Create a Flask test client """
    yield app.test_client()
```

## Structure of tests using the Flask test client

The general structure of this type of test is:

1. ARRANGE: Pass the Flask test client fixture to the test function.
2. ACT: Use the test client to make an HTTP request to one of your routes. Assign the response
   object to a variable.
3. ASSERT: Access parameter of the response object and use assertions to check the validity.

Use the client fixture by passing it as parameter to the test function e.g.,
`def some_test(client):`

To make an HTTP request using the 'client'
see [Sending Requests with the Test Client](https://flask.palletsprojects.com/en/stable/testing/#sending-requests-with-the-test-client).

For example:

```python
response = client.get("/")
```

The [Flask response object](https://flask.palletsprojects.com/en/stable/api/#flask.Response) has
attributes such as:

- the HTTP status code (`request.status_code`)
- page content (`response.data`).
- page header details such as the content type (`response.header["Content-Type"]`)
- the JSON payload (`response.json`)

The more common [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) you
might expect are:

- 404 NOT FOUND
- 200 OK for successful GET request
- 201 CREATED for POST requests creating a new resource
- 500 INTERNAL SERVER ERROR This might indicate a problem with the request, or might indicate a
  problem in the server
  side code.

To see what the attributes of the Flask response object look like; add the following code to
`test_routes.py` and run
it.:

```python
def test_print_response_params(client):
    """
    This is just so you can see what type of detail you get in a response object.
    Don't use this in your tests!
    """
    response = client.get("/")
    print("Printing response.headers:")
    print(response.headers)
    print('\n Printing response.headers["Content-Type"]:')
    print(response.headers['Content-Type'])
    print("Printing response.status_code:")
    print(response.status_code)
    print("Printing response.data:")
    print(response.data)
    print("Printing response.json:")
    print(response.json)
```

Now delete the code you just added as you don't need it in the test code.

### Test the home page is successful when accessed using a GET HTTP request

Aspects to check that show the home page was returned include:

- status code should be 200 OK
- should have the word 'Paralympics' in the body of the text

A test should test one thing, that does not necessarily mean one assertion. You could decide to have
2 tests for the
above, or one test with two assertions.

For example:

```python
def test_home_page_loads(client):
    """
    GIVEN a test client
    WHEN the 'home' page is requested
    THEN check that the response is 200
    AND check the page title contains the word "Paralympics"
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Paralympics" in response.data
    # alternative: assert "<title>Paralympics" in response.get_data()
```

### Test for an HTTP method that is not allowed

Write a test that an HTTP POST request for the locations page route should return an HTTP error.

This route only accepts GET requests so it should return an 'HTTP Method not allowed' status
code, [405](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405).

```python
def test_locations_fails_post_request(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /locations
    THEN the status code should be 405
    """
    response = client.post("/locations")
    assert response.status_code == 405
```

Add your own test for the `/trends` route.

### Test a POST route with form data

Refer to
the [Flask test documentation for passing form data](https://flask.palletsprojects.com/en/stable/testing/#form-data).

The following tests that the /participants page on submit of a form. Pass the form data as a
dict to the `data=` attribute of the request.

```python
def test_participants_form_post_success(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /participants with valid form data
    THEN the status code should be 200
    """
    # Simulate posting the form with multiple selected types
    data = {"paralympics_types": ["winter", "summer"]}
    resp = client.post("/participants", data=data)
    assert resp.status_code == 200
```

### Write your own route tests

This depends on which routes you have written. Look at your routes and try to write tests that:

- test what happens when the route succeeds
- test what happens when an unexpected value is passed
- test what happens when the wrong method is used
- test that uses data in a form
- test that passes data to a form

## Unit tests

You can also write unit tests for the 'helper' functions that are used by your routes. These do not
require the test client as they are not accessed as HTTP requests and don't require the Flask app to 
be running.

Unit testing with pytest was covered in COMP0035.

An example of unit tests for a `make_prediction` function:

```python
def test_prediction_returns_int():
    """
    GIVEN a function to make_prediction
    WHEN a request is made to get_prediction with valid data
    THEN the result should be an integer
    """
    from student.flask_paralympics.paralympics import make_prediction
    prediction = make_prediction(2030, "Germany")
    assert isinstance(prediction, int)


def test_prediction_no_data_returns_error():
    """
    GIVEN a function to make_prediction
    WHEN a request is made to get_prediction with invalid data
    THEN the result should be an error message with 'Error making prediction'
    """
    from student.flask_paralympics.paralympics import make_prediction
    prediction = make_prediction(2030, "Invalid")
    assert "Error making prediction" in prediction
```

[Next activity](5-github-actions.md)