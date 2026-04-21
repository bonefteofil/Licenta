from sqlmodel import SQLModel, Field
from models.bariera_model import TipBariera
from datetime import datetime, timezone


class Istoric(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    utilizator_id: int = Field(default=None, foreign_key="utilizator.id", ondelete="CASCADE")
    bariera_id: int = Field(default=None, foreign_key="bariera.id", ondelete="CASCADE")
    actiune: TipBariera
    data: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class IstoricCreate(SQLModel):
    utilizator_id: int = Field(default=None, foreign_key="utilizator.id")
    bariera_id: int = Field(default=None, foreign_key="bariera.id")
    actiune: TipBariera
    ora: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
