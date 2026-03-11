# 2. Create schemas

## Pydantic or SQLModel?

If you remember, SQLModel uses SQLAlchemy and Pydantic under the covers. If you are using
SQLModel you can use this for schemas and models.

You do not have to use SQLModel for the coursework. You may wish to use SQLAlchemy, particularly
if you plan to work with databases beyond this course as it is widely used so you may prefer to
learn the direct syntax now.

If you choose to use SQLAlchemy then use this for the model classes, and Pydantic for the schemas.
You could also search PyPi for packages that support generation of Pydantic schemas from
sqlalchemy models.

There is an example of Pydantic schemas in the tutor solutions for this week. You could also
use Copilot or other to generate schemas from the models. Note that in Read models, Copilot seems to
use `class Config:  from_attributes = True` whereas the
documentation suggests `model_config = ConfigDict(from_attributes=True)` is now preferred.

## Create the schemas using SQLModel

For each of the existing models, create a set of models and schemas:

- `BaseSomething(SQLModel)`: base schema with common attributes for all schemas
- `Something(BaseSomething, table=True)`: the database table model (if you prefer leave these as is,
  then don't inherit from BaseSomething, leave this as SQLModel)
- `SomethingCreate(BaseSomething)`: schema for creating new something
- `SomethingRead(BaseSomething)`: response schema
- `SomethingUpdate(SQLModel)`: schema for partial updates making all fields optional

Table 2 in the first activity gives more explanation of the differences.

Create schemas for the Paralympics API in `paralympics.models.schemas.py`.

The following is an example for the Games resource:

```python
from typing import Optional

from pydantic import ConfigDict, field_validator
from sqlmodel import SQLModel, CheckConstraint, Field, Relationship


# Schemas
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


class GamesUpdate(SQLModel):
    """Schema for updating a Games record - all fields optional"""
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

# Model
class Games(GamesBase, table=True):
    """SQLModel database table for Games"""
    __tablename__ = "games"
    id: Optional[int] = Field(default=None, primary_key=True)

    hosts: list["Host"] = Relationship(back_populates="games", link_model=GamesHost)
    disabilities: list["Disability"] = Relationship(
        back_populates="games", link_model=GamesDisability
    )
    teams: list["Team"] = Relationship(back_populates="games", link_model=GamesTeam)

    __table_args__ = (
        CheckConstraint("event_type IN ('winter', 'summer')"),
        CheckConstraint("year BETWEEN 1960 AND 9999"),
    )
```

[Next activity](3-get-routes.md)
