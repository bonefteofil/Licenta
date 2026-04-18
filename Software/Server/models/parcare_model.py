from sqlmodel import SQLModel, Field


class Parcare(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    manager_id: int = Field(default=None, foreign_key="utilizator.id", ondelete="CASCADE")
    denumire: str
    capacitate: int | None
    ocupare: int = Field(default=0)


class ParcareCreate(SQLModel):
    manager_id: int = Field(default=None, foreign_key="utilizator.id")
    denumire: str
    capacitate: int | None
