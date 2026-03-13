from fastapi import APIRouter


from backend.services.games_service import GamesService, Games
from backend.dependencies import SessionDep

router = APIRouter()

# A more typical prefix, avoided to keep consistency with the front end app
# router = APIRouter(prefix="/api/games") 

service = GamesService()


@router.get("/", response_model=Games)
def read_game_all(session: SessionDep):
    return service.get_games(session)


@router.get("/chartdata", response_model=Games)
def read_chart_data(session: SessionDep):
    return service.get_chart_data(session)


@router.get("/{game_id}", response_model=Games)
def read_game(game_id: int, session: SessionDep):
    return service.get_games_by_id(session, game_id)
