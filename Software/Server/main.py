from fastapi import FastAPI
from database import pornire_baza_de_date


app = FastAPI()

pornire_baza_de_date()
