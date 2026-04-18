from fastapi import FastAPI
from database import pornire_baza_de_date

from routers.utilizator_api import router as utilizator_router

pornire_baza_de_date()

app = FastAPI()
app.include_router(utilizator_router)
