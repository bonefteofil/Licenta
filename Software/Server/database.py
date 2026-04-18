from fastapi.params import Depends
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy import event
from typing import Annotated

from models.utilizator_model import Utilizator


baza_de_date = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})


# verificarea cheilor externe in SQLite
@event.listens_for(baza_de_date, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def pornire_baza_de_date():
    SQLModel.metadata.create_all(baza_de_date)


def get_db():
    with Session(baza_de_date) as session:
        yield session


sesiune = Annotated[Session, Depends(get_db)]
