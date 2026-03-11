# 6. Add the PUT and/or PATCH routes

The purpose of these methods is to update or replace an existing resource.

PUT replaces the entire resource i.e. it replaces all the fields, PATCH can be used for partial
updates.

PUT requests are idempotent, that is repeating the same request should have the same effect, whereas
a PATCH request may not always be idempotent. For instance, if a resource includes an
auto-incrementing counter, a PUT request will overwrite the counter (since it replaces the entire
resource), but a PATCH request may not.

Return 200 OK for successful updates. The content of the updated object may also be returned.

To understand more about the differences, and when to use PUT or PATCH,
read this [blog post](https://blog.postman.com/http-patch-method/) which summarises the methods and
when to use each.

## Add functions to support the deletion of a new Games object

To do this you need:

1. A `.update_games()` method in the `GamesService` class in `games_service.py`.
2. An HTTP PUT route `@router.put()` and/or An HTTP PATCH route`@router.patch()` function in
   `games_router.py`

You will need an additional schema for the PATCH route that makes all fields optional. You could
create a further schema for the PUT route, however in this instance the existing GamesCreate schema
would work, so I am using this for convenience.

```python
class GamesUpdate(SQLModel):
    """ Schema for updating a Games record - all fields optional """
    event_type: Optional[str] = None
    year: Optional[int] = None
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
    def validate_event_type(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            allowed = ["winter", "summer"]
            value = value.lower()
            if value not in allowed:
                raise ValueError(f"{value} is not in {allowed}")
        return value

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: Optional[int]) -> Optional[int]:
        if value is not None:
            value = int(value)
            if value < 1960 or value > 9999:
                raise ValueError(f"{value} must be between 1960 and 9999")
        return value


class ResponseUpdate(SQLModel):
    """ Schema for updating a Response record - all fields optional """
    question_id: Optional[int] = None
    response_text: Optional[str] = None
    is_correct: Optional[bool] = None


class QuestionUpdate(SQLModel):
    """ Schema for updating a Question record - all fields optional """
    question_text: Optional[str] = None
```

### Create the `update_games()` method

The code below should function for either PUT or PATCH. You can create separate methods for each
if you prefer.

```python
def update_games(self, session: SessionDep, games_id: int, update_data: dict):
    """ Method to update a Games object.

    This method can be used by either PUT or PATCH. The route code will handle the
    validation against the schema.

    Args:
        session: FastAPI dependency with SQLModel session
        games_id: id of the Games to update
        update_data: data to update the Games object

    Returns:
        games: Paralympic Games object
        """
    games = self.get_games_by_id(session, games_id)
    if games is None:
        return None

    for key, value in update_data.items():
        setattr(games, key, value)

    session.commit()
    session.refresh(games)
    return games
```

### Create the PATCH route

The PATCH routes allows only some fields to be updated. The GamesUpdate schema allows for all to be
optional.

You only want to act on the values that have been provided, so use the
`update_data=data.model_dump(exclude_unset=True)` which avoids validation errors for fields that are
not present in the data.

The code looks like this:

```python
@router.patch("/games/{games_id}")
def update_games(games_id: int, data: GamesUpdate, session: SessionDep):
    """ Partial updates for a paralympic Games

    Note: data.model_dump(exclude_unset=True) allows for only some fields to be present in the data
    """
    games = crud.update_games(session=session, games_id=games_id,
                              update_data=data.model_dump(exclude_unset=True))
    return games
```

### Create the PUT route

The PUT routes allows some fields to be changed but expects all fields to be present as it replaces
the full resource. The following uses the GamesCreate schema which works in this instance.

You require values for all fields so this uses `update_data=data.model_dump()` 

The code looks like this:

```python
@router.put("/games/{games_id}")
def replace_games(games_id: int, data: GamesCreate, session: SessionDep):
    """ Updates a paralympic Games by replacing the entire resource

    Note: model_dump() expects all fields to be present in the data and applies the validation
    """
    games = crud.update_games(session=session, games_id=games_id, update_data=data.model_dump())
    return games
```

## Add PUT/PATCH routes for Question and Response

Using the approach above, add similar routes for the Question and Response in the quiz resource.

[Next activity](7-end.md)