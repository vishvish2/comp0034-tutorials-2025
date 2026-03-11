# 4. Add the POST routes

## POST routes

POST routes create a new resource or submit data to the server, i.e. non-idempotent operations.
Include error handling e.g., return 400 Bad Request for invalid input.

## Add functions to support the creation of a new Games object

To do this you need:

1. An HTTP POST route `@router.post()` function in `games_router.py`
2. A `.create_games()` method in the `GamesService` class in `games_service.py`

You will also need the following schemas:

```python
class GamesBase(SQLModel):
    """Base schema for Games with core fields"""
    event_type: str
    year: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    countries: Optional[int] = None
    events: Optional[int] = None
    sports: Optional[int] = None
    participants_m: Optional[int] = None
    participants_f: Optional[int] = None
    participants: Optional[int] = None
    highlights: Optional[str] = None
    url: Optional[str] = None

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        allowed = ["winter", "summer"]
        value = value.lower()
        if value not in allowed:
            raise ValueError(f"{value} is not in {allowed}")
        return value

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        value = int(value)
        if value < 1960 or value > 9999:
            raise ValueError(f"{value} must be between 1960 and 9999")
        return value


class GamesCreate(GamesBase):
    """Schema for creating a new Games record"""
    pass


class GamesRead(GamesBase):
    """Schema for reading a Games record"""
    id: int
    model_config = ConfigDict(from_attributes=True)
```

### Add a POST route to `games_router.py`

Use the `GamesCreate` schema which defines what is valid for a new Games to be created. This will
ensure that the data provided by the user matches what the schema defines to be valid.

Use the games service `create_games` function to pass the data to the service that will then
create the new games object and save to the database.

If the process is successful, then return to the user the newly created object, including its
row id, which is defined in the `GamesRead` schema. The HTTP status code for success of a POST route
is 201, and not 200; specify this in the `@router.post()` decorator.

Add this route code:

```python
@router.post("/games", response_model=GamesRead, status_code=status.HTTP_201_CREATED)
def create_games(session: SessionDep, games_data: GamesCreate) -> Any:
    """ Creates a new paralympic Games """
    new_games = crud.create_games(session, games_data)
    return new_games
```

### Add a "create" method to the database service class in `games_service.py`

This method receives the dict with data for a new Games from the route and a database Session
dependency.

It creates a new Games object using the data from the dict.

It adds and commits it to the database using the Session.

The `refresh()` method ensures that the new Games object is updated with the inserted row id
once it has been saved to the database.

Return the new Games object to the route, which then in turn will use the `GamesRead` schema to
check the values to return to the user.

Add this code to the GamesService:

```python
def create_games(session: SessionDep, games_create: GamesCreate) -> Games:
    """ Method to create a new games.


    Args:
        session: FastAPI dependency with SQLModel session
        games_create: data for a new Paralympic Games object

    Returns:
        Games: Paralympic Games object
        """
    new_games = Games.model_validate(games_create)
    session.add(new_games)
    session.commit()
    session.refresh(new_games)
    return new_games
```

Run the app (if not already running); go to http://127.0.0.1:8000/docs and check that the POST
routes for Games works, and you get a 201 response with data that includes the `id`.

Try to add a new Games with `"event_type": "hello"`; you should get a validation error.

## Repeat for Question and Response

Using the approach above, add the same POST/create functions for the Question and Response
models in the `quiz_router.py` and `quiz_service.py`.

Complete the code:

```python
@router.post("/questions", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
# complete the code

@router.post("/responses", response_model=ResponseRead, status_code=status.HTTP_201_CREATED)
# complete the code
```

Complete the code:

```python
def create_question():
    """ Method to create a new Question.

    Args:
        db: SQLModel session dependency
        question_create: data for a new Question object

    Returns:
        Question: Question object
        """


def create_response():
    """ Method to create a new Response.

    Args:
        db: SQLModel session dependency
        response_create: data for a new Response object

    Returns:
        Response: Response object
    """
```

You will need these schemas:

```python
class QuestionBase(SQLModel):
    """Base schema for Question with core fields"""
    question_text: str


class QuestionCreate(QuestionBase):
    """Schema for creating a new Question record"""
    pass


class QuestionRead(QuestionBase):
    """Schema for reading a Question record"""
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseBase(SQLModel):
    """Base schema for Response with core fields"""
    question_id: Optional[int] = None
    response_text: str
    is_correct: bool


class ResponseCreate(ResponseBase):
    """Schema for creating a new Response record"""
    pass


class ResponseRead(ResponseBase):
    """Schema for reading a Response record"""
    id: int
    model_config = ConfigDict(from_attributes=True)
```

[Next activity](5-delete-routes.md)