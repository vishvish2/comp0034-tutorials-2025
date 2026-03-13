# 6. Testing routes with authentication

Skip this if you didn't add authentication to the app code in week 8.

This activity covers:

1. Fixtures for authentication
2. Testing the signup and login routes/endpoints in the authentication routes
3. Testing the service to create a new user
4. Testing login and routes that are protected by authentication

## 1. Additional fixtures for authentication

To test login in the `auth_router.py` and the authenticated routes in the `quiz_router.py` you will
first need to add additional fixtures to `backend/conftest.py`.

1. A fixture to add a test user to the database.

    ```python
    @pytest.fixture(name="test_user")
    def test_user_fixture(session: Session) -> User:
        """Creates a test user in the database"""
        from backend.core.security import get_password_hash
    
        test_user = User(
            email="testuser@example.com",
            hashed_password=get_password_hash("testpassword")
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        return test_user
    ```

2. A test client fixture that overrides the CurrentUser dependency.

    You already did this for the database dependency in the test client fixture. This fixture therefore
    resembles the test client but with the additional dependency.
    
    It uses both the `session` and `test_user` fixtures.
    
    ```python
    @pytest.fixture(name="client_with_auth")
    def client_with_auth_fixture(session: Session, test_user: User):
        """Creates a test client with CurrentUser dependency overridden with a test user"""
    
        def get_session_override():
            return session
    
        def get_current_user_override():
            return test_user
    
        app = create_app()
        app.dependency_overrides[get_db] = get_session_override
        app.dependency_overrides[get_current_user] = get_current_user_override
    
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()
    ```

## 2. Test the signup and login routes

Create a new test module `tests/backend/test_auth_router.py`.

You can create your own details for a fake user for testing, or install the `faker` library (
`pip install faker`) as shown in the example below.

The test function is otherwise similar to the POST /games test you wrote earlier.

### Test the POST /signup endpoint

```python
def test_signup_success(client):
    signup_data = {
        "email": fake.email(),
        "password": fake.password(),
    }
    response = client.post(
        "/signup", json=signup_data
    )
    data = response.json()

    # Signup route returns 201 Created on success and returns the user object
    assert response.status_code == 201, "Signup route should return 201 status code"
    assert data["id"] is not None, "A created user should have an id."
```

1. Add the above test and run it: `pytest tests/backend/test_auth_router.py::test_signup_success`

2. Create a further test that signup fails when only the email is passed in the signup data. This
   should return a 422 status as it raises a validation error when the data does not match the
   UserCreate schema.

### Tests for login

Add this test which uses the `client` fixture and the new `test_user` fixture.

The route requires data that matches the OAuth2PasswordRequestForm which has username and password.
`username` in this implementation is the email address.

A request is made to the POST /login/access-token route.

```python
def test_login_access_token_succeeds(client, test_user):
    password = "testpassword"
    response = client.post(
        "/login/access-token",
        data={"username": test_user.email, "password": password},
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["access_token"] != ""
    assert data["token_type"] == "bearer"
```

Now add:
1. A test that uses the wrong password. This should return a status code of 400.
2. A tests that has a user that is not in the database. This should also return a status code of 400.

## 2. Test the creation of a new user in the database

This test verifies that a new user can be created.

It is an example of a test that does not use the test client, only the session fixture.

Create a new test module `tests/backend/test_auth_service.py`.

Add a test to verify a user was created.

```python
from faker import Faker
from sqlmodel import Session

from backend.models.schemas import UserCreate
from backend.services.auth_service import AuthService

fake = Faker()


# This test does not use the test client but does use the session fixture
def test_create_user(session: Session) -> None:
    email = fake.email()
    password = fake.password()
    user_in = UserCreate(email=email, password=password)
    crud = AuthService()
    user = crud.create_user(session=session, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password"), "User model must include hashed_password attribute"
    assert user.hashed_password is not password, "The hashed_password attribute must not be equal to password"
```

Run the test: `pytest tests/backend/test_auth_service.py::test_create_user`

## 4. Test the quiz routes protected by authentication

This test requires the `client_with_auth` fixture as the quiz service requires the CurrentUser dependency to add a new question and responses.

```python
def test_create_question_authorised(client_with_auth):
    response = client_with_auth.post("/questions", json={"question_text": "Some text"})
    assert response.status_code == 201, "Create question should return status code 201 as the user is authenticated."
```

Add a test to create responses for the question.

If you want to test with an unauthorised user, use the `client` fixture instead.

[Next activity](7-end.md)
