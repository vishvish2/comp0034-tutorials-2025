from typing import Optional, Any
from fastapi import HTTPException
from sqlmodel import select

from backend.models.models import Games, Host, Country
from backend.dependencies import SessionDep


class GamesService:

    @staticmethod
    def get_games_by_id(session: SessionDep, game_id: int) -> Games:
        """ Method to retrieve a game by its ID.
        Args:
            session: SQLModel session
            game_id: Games.id

        Returns:
            Games: Paralympic Games object

        Raises:
            HTTPException 404 Not Found
            """
        result: Optional[Games] = session.get(Games, game_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Games with id {game_id} not found")
        return result
    

    @staticmethod
    def get_games(session: SessionDep) -> Games:
        """ Method to retrieve a game by its ID.
        Args:
            session: SQLModel session
            game_id: Games.id

        Returns:
            Games: Paralympic Games object

        Raises:
            HTTPException 404 Not Found
            """
        result: list[Games] = session.exec(select(Games)).all()
        if not result:
            return []
        return result
    

    @staticmethod
    def get_chart_data(session: SessionDep) -> list[dict[str, Any]]:
        """ Method to return all data from the paralympics database for the charts."""
        statement = select(
            Country.country_name,
            Games.event_type,
            Games.year,
            Games.start_date,
            Games.end_date,
            Host.place_name,
            Games.events,
            Games.sports,
            Games.countries,
            Games.participants_m,
            Games.participants_f,
            Games.participants,
            Host.latitude,
            Host.longitude,
        ).select_from(Games).join(Games.hosts).join(Country, Host.country_id == Country.id)

        result = session.exec(statement).all()
        data = [dict(row) for row in result]
        if not data:
            return []
        return data