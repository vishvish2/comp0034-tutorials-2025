# 5. Add the DELETE routes

Delete requests remove a resource. Deletion should return `204 No Content` to indicate successful
deletion.
REST convention is to return `404 Not Found` if the resource doesn't exist; though always returning
`204 No Content` is more strictly idempotent.

## Add functions to support the deletion of a new Games object

To do this you need:

1. A `.delete_games()` method in the `GamesService` class in `games_service.py`.
2. An HTTP DELETE route `@router.delete()` function in `games_router.py`

You do not need schemas for this activity.

### Create the `delete_games()` method

The following code returns None if the Games is not found, and an empty dict if it was
deleted. You could choose to just return the empty dict for either case.

```python
def delete_games(self, session: SessionDep, games_id: int) -> None:
    """ Delete a paralympic Games

    Args:
        session: FastAPI dependency with SQLModel session
        games_id: id of the Games to delete

    Returns:
        {} if the Games is deleted, or None if not found
        """
    games = self.get_games_by_id(session, games_id)
    if not games:
        return None
    else:
        session.delete(games)
        session.commit()
        return {}
```

The delete route code below returns 404 when the resource was not found, and 204 only when
deleted. You can choose to always return 204 if you prefer.

```python
@router.delete("/games/{games_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_games(session: SessionDep, games_id: int) -> None:
    """ Delete a new paralympic Games

    The version returns 404 if the Games was not found and 204 if it was deleted
    You could modify and return 204 in both cases

    Returns:
        Nothing as the 204 Method expects an empty body
    """
    games = crud.delete_games(session, games_id)
    if games is None:
        raise HTTPException(status_code=404, detail=f"Games with id {games_id} not found")
    else:
        return
```

Add the code. Make sure the app is running. Use the interactive docs to delete the new games you
added in activity 4.

## Add delete routes for Question and Response

Using the approach above, add delete routes for the Question and Response in the quiz resource.

A Response can be deleted and the Question remains.

If the Question is deleted - are the Responses also deleted? Check if this is implemented in the
database or not. If not, then handle it in the route.

[Next activity](6-put-patch-routes.md)