from fastapi import APIRouter, HTTPException, Cookie
from sqlmodel import select
from database import sesiune
from models.parcare_model import Parcare, ParcareCreate
from models.membru_parcare_model import MembruParcare
from models.istoric_model import Istoric
from models.bariera_model import Bariera


router = APIRouter(prefix="/api/parcari", tags=["Parcari"])

def verificare_acces(db, parcare_id: int, utilizator_id: int):
    # se verifica daca utilizatorul este membru al parcarii
    membru_validat = db.exec(
        select(MembruParcare)
        .where(MembruParcare.parcare_id == parcare_id)
        .where(MembruParcare.utilizator_id == utilizator_id)
    ).first()
    if not membru_validat: 
        raise HTTPException(status_code=403, detail="Acces interzis")
    return membru_validat


@router.get("/")
def ListeazaParcari(db: sesiune, utilizator_id: int = Cookie()):
    # se returneaza parcarile pentru care utilizatorul este membru
    parcari_permise = db.exec(
        select(Parcare)
        .join(MembruParcare)
        .where(MembruParcare.utilizator_id == utilizator_id)
    ).all()
    return parcari_permise


@router.post("/")
def CreareParcare(date_parcare: ParcareCreate, db: sesiune, utilizator_id: int = Cookie()):
    parcare_noua = Parcare.model_validate(date_parcare)
    parcare_noua.manager_id = utilizator_id
    
    db.add(parcare_noua)
    db.commit()
    db.refresh(parcare_noua)
    if parcare_noua.id is None:
        raise HTTPException(status_code=500, detail="Eroare la crearea parcarii")
        
    membru_admin = MembruParcare(
        parcare_id=parcare_noua.id, 
        utilizator_id=utilizator_id
    )
    db.add(membru_admin)
    db.commit()
    return parcare_noua


@router.get("/{parcare_id}")
def DetaliiParcare(parcare_id: int, db: sesiune, utilizator_id: int = Cookie()):
    verificare_acces(db, parcare_id, utilizator_id)
    return db.get(Parcare, parcare_id)


@router.delete("/{parcare_id}")
def StergeParcare(parcare_id: int, db: sesiune, utilizator_id: int = Cookie()):
    # se valideaza permisiunea de administrator
    parcare_gasita = db.get(Parcare, parcare_id)
    if not parcare_gasita or parcare_gasita.manager_id != utilizator_id:
        raise HTTPException(status_code=403, detail="Doar managerul poate sterge parcarea")
        
    db.delete(parcare_gasita)
    db.commit()
    return {"mesaj": "Parcare ștearsă complet"}


@router.get("/{parcare_id}/istoric")
def IstoricParcare(parcare_id: int, db: sesiune, utilizator_id: int = Cookie()):
    verificare_acces(db, parcare_id, utilizator_id)
    
    istoric_parcare = db.exec(
        select(Istoric)
        .join(Bariera)
        .where(Bariera.parcare_id == parcare_id)
    ).all()
    return istoric_parcare
