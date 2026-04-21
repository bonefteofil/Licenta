from sqlmodel import SQLModel, Field
from enum import Enum


class TipBariera(str, Enum):
    intrare = "intrare"
    iesire = "iesire"


class Bariera(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parcare_id: int = Field(default=None, foreign_key="parcare.id", ondelete="CASCADE")
    nr_deschideri: int = Field(default=0)
    tip: TipBariera


class BarieraCreate(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    parcare_id: int = Field(default=None, foreign_key="parcare.id")
    tip: TipBariera
