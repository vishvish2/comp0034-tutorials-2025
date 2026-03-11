# 3. Update the GET routes

Make sure you have the following schemas:

- GamesRead
- ParalympicsRead

ParalympicsRead is a schema only and does not have a corresponding ORM model. The data is from a
query that joins data from several tables. It is used to provide the data that was used in the front
end app to generate the charts.

```python
class ParalympicsRead(SQLModel):
    """Response model for 'all data' endpoint"""
    country_name: str
    event_type: str
    year: Optional[int] = None
    place_name: Optional[str] = None
    events: Optional[int] = None
    sports: Optional[int] = None
    countries: Optional[int] = None
    participants_m: Optional[int] = None
    participants_f: Optional[int] = None
    participants: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
```

The current routes in `games_router.py` are:

```python
@router.get("/games", response_model=list[Games])
def get_games(session: SessionDep):
    """ Returns the data for all Paralympics"""
    games = crud.get_games(session)
    return games


@router.get("/all", response_model=list[Paralympics])
def get_chart_data(session: SessionDep):
    """ Returns data for the charts

    The data is from a query that joins the Games, Host and Country tables. The result
    has the same data attributes as used for creating the charts in the
    Dash/Streamlit/Flask activities in weeks 1 to 5
    """
    data = crud.get_chart_data(session)
    return data


@router.get("/games/{games_id}", response_model=Games)
def get_games_by_id(session: SessionDep, games_id: int):
    """ Returns the data for one Paralympics by its id """
    games = crud.get_games_by_id(session, games_id)
    return games
```

Modify these so that the `response_model` uses the GamesRead and ParalympicsRead schemas instead.

For example, this is the first of those routes with the updated imports:

```python
from backend.models.schemas import GamesRead, ParalympicsRead
from backend.services.games_service import GamesService

router = APIRouter()

crud = GamesService()


@router.get("/games", response_model=list[GamesRead])
def get_games(session: SessionDep):
    """ Returns the data for all Paralympics"""
    games = crud.get_games(session)
    return games
```

Repeat for the routes in the `quiz_router.py` where the schemas will be QuestionRead and
ResponseRead.

```python
from fastapi import APIRouter

from backend.core.deps import SessionDep
from backend.models.schemas import QuestionRead, ResponseRead
from backend.services.quiz_service import QuizService

router = APIRouter()

crud = QuizService()


@router.get("/questions", response_model=list[QuestionRead])
def get_questions(session: SessionDep):
    """ Returns the data for all questions

    NB: Front-end route needs to be changed from '/question' to '/questions'
    """
    questions = crud.get_questions(session)
    return questions


@router.get("/questions/{q_id}", response_model=QuestionRead)
def get_question(session: SessionDep, q_id: int):
    """ Returns the data for one questions

    NB: Front-end route needs to be changed from '/question/q_id' to '/questions/{q_id}'
    """
    question = crud.get_question(session, q_id=q_id)
    return question


@router.get("/questions/{q_id}/responses", response_model=list[ResponseRead])
def get_responses_for_question(session: SessionDep, q_id: int):
    """ Returns the data for all responses for a given question

    NB: Front-end route needs to be changed from '/question/search' to '/questions/{q_id}/responses'
    """
    responses = crud.get_responses_by_question(session, q_id)
    return responses

```

Once you have made the changes, run the FastAPI app and check the routes using the docs
at http://127.0.0.1:8000/docs

[Next activity](4-post-routes.md)