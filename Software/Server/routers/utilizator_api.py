from fastapi import APIRouter, HTTPException, Response, Cookie
from sqlmodel import select
from database import sesiune
from models.utilizator_model import UtilizatorCreate, UtilizatorCredentiale, Utilizator


router = APIRouter(prefix="/api/utilizatori", tags=["Utilizatori"])

@router.post("/inregistrare")
def Inregistrare(date_utilizator: UtilizatorCreate, db: sesiune, response: Response):
    utilizator_nou = Utilizator.model_validate(date_utilizator)
    db.add(utilizator_nou)
    db.commit()
    db.refresh(utilizator_nou)
    
    response.set_cookie(key="utilizator_id", value=str(utilizator_nou.id))
    return utilizator_nou


@router.post("/autentificare")
def Autentificare(credentiale: UtilizatorCredentiale, db: sesiune, response: Response):
    utilizator_gasit = db.exec(
        select(Utilizator)
        .where(Utilizator.nume == credentiale.nume)
        .where(Utilizator.parola == credentiale.parola)
    ).first()
    if not utilizator_gasit: 
        raise HTTPException(status_code=401, detail="Date incorecte")
        
    response.set_cookie(key="utilizator_id", value=str(utilizator_gasit.id))
    return utilizator_gasit


@router.get("/cont")
def DateleContului(db: sesiune, utilizator_id: str = Cookie()):
    utilizator_curent = db.get(Utilizator, int(utilizator_id))
    if not utilizator_curent: 
        raise HTTPException(status_code=404, detail="Utilizator inexistent")
    return utilizator_curent


@router.post("/deconectare")
def Deconectare(response: Response):
    response.delete_cookie(key="utilizator_id")
    return {"mesaj": "Deconectat"}


@router.delete("/")
def StergeCont(db: sesiune, utilizator_id: str = Cookie()):
    utilizator_curent = db.get(Utilizator, int(utilizator_id))
    if not utilizator_curent: 
        raise HTTPException(status_code=404, detail="Utilizator inexistent")
    
    db.delete(utilizator_curent)
    db.commit()
    return {"mesaj": "Cont sters"}
