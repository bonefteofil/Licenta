from fastapi import APIRouter, HTTPException, Cookie
from database import sesiune
from sqlmodel import select
from models.membru_parcare_model import MembruParcare, MembruParcareInfo
from models.parcare_model import Parcare


router = APIRouter(prefix="/api/membri", tags=["Membri"])

@router.get("/{parcare_id}")
def ListeazaMembri(parcare_id: int, db: sesiune, utilizator_id: int = Cookie()):
    # se verifica daca utilizatorul este membru al parcarii
    membru_validat = db.exec(
        select(MembruParcare)
        .where(MembruParcare.parcare_id == parcare_id)
        .where(MembruParcare.utilizator_id == utilizator_id)
    ).first()
    if not membru_validat: 
        raise HTTPException(status_code=403, detail="Acces interzis")
    
    # se returneaza toti membrii parcarii
    toti_membrii = db.exec(
        select(MembruParcare)
        .where(MembruParcare.parcare_id == parcare_id)
    ).all()
    return toti_membrii


@router.post("/")
def AdaugaMembru(date_membru: MembruParcareInfo, db: sesiune, utilizator_id: int = Cookie()):
    # se verifica permisiunea de manager
    parcare_gasita = db.get(Parcare, date_membru.parcare_id)
    if not parcare_gasita or parcare_gasita.manager_id != utilizator_id: 
        raise HTTPException(status_code=403, detail="Doar managerul poate adăuga membri")
    
    # se verifica daca utilizatorul este deja membru
    membru_existent = db.exec(
        select(MembruParcare)
        .where(MembruParcare.parcare_id == date_membru.parcare_id)
        .where(MembruParcare.utilizator_id == date_membru.utilizator_id)
    ).first()
    if membru_existent:
        raise HTTPException(status_code=400, detail="Utilizatorul este deja membru")
    
    # se adauga membrul nou
    membru_nou = MembruParcare.model_validate(date_membru)
    db.add(membru_nou)
    db.commit()
    return {"mesaj": "Membru adăugat cu succes"}


@router.delete("/")
def EliminaMembru(date_membru: MembruParcareInfo, db: sesiune, utilizator_id: int = Cookie()):
    # se verifica permisiunea
    parcare_gasita = db.get(Parcare, date_membru.parcare_id)
    este_manager = parcare_gasita and parcare_gasita.manager_id == utilizator_id
    este_parasire = date_membru.utilizator_id == utilizator_id
    if not este_manager and not este_parasire:
        raise HTTPException(status_code=403, detail="Nu ai permisiunea să elimini acest membru")
        
    # se verifica daca membrul exista
    membru_actual = db.exec(
        select(MembruParcare)
        .where(MembruParcare.parcare_id == date_membru.parcare_id)
        .where(MembruParcare.utilizator_id == date_membru.utilizator_id)
    ).first()
    if not membru_actual:
        raise HTTPException(status_code=404, detail="Membru negasit")
    
    # se elimina membrul
    db.delete(membru_actual)
    db.commit()
    return {"mesaj": "Membru eliminat din parcare"}
