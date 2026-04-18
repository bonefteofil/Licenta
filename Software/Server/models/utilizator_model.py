from sqlmodel import SQLModel, Field


class Utilizator(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nume: str = Field(unique=True)
    parola: str
    numar_inmatriculare: str


class UtilizatorCreate(SQLModel):
    nume: str
    parola: str
    numar_inmatriculare: str


class UtilizatorCredentiale(SQLModel):
    nume: str
    parola: str
