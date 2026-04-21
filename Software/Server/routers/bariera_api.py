from fastapi import APIRouter, HTTPException, Cookie
from database import sesiune
from sqlmodel import select 
from models.bariera_model import Bariera, BarieraCreate
from models.utilizator_model import Utilizator
from models.membru_parcare_model import MembruParcare
from models.istoric_model import Istoric
from models.parcare_model import Parcare


router = APIRouter(prefix="/api/bariere", tags=["Bariere"])

@router.get("/{parcare_id}")
def ListeazaBariere(parcare_id: int, db: sesiune, utilizator_id: int = Cookie()):
    membru_validat = db.exec(
        select(MembruParcare)
        .where(MembruParcare.parcare_id == parcare_id)
        .where(MembruParcare.utilizator_id == utilizator_id)
    ).first()
    
    if not membru_validat: 
        raise HTTPException(status_code=403, detail="Acces interzis")
        
    bariere_gasite = db.exec(
        select(Bariera)
        .where(Bariera.parcare_id == parcare_id)
    ).all()
    return bariere_gasite


@router.post("/")
def AdaugaBariera(date_bariera: BarieraCreate, db: sesiune, utilizator_id: int = Cookie()):
    parcare_gasita = db.get(Parcare, date_bariera.parcare_id)
    
    if not parcare_gasita or parcare_gasita.manager_id != utilizator_id:
        raise HTTPException(status_code=403, detail="Doar managerul poate instala bariere")
        
    bariera_noua = Bariera.model_validate(date_bariera)
    db.add(bariera_noua)
    db.commit()
    return {"mesaj": "Barieră instalată cu succes"}


@router.delete("/{bariera_id}")
def DemonteazaBariera(bariera_id: int, db: sesiune, utilizator_id: int = Cookie()):
    bariera_gasita = db.get(Bariera, bariera_id)
    if not bariera_gasita: 
        raise HTTPException(status_code=404, detail="Bariera nu există")
        
    parcare_gasita = db.get(Parcare, bariera_gasita.parcare_id)
    if not parcare_gasita or parcare_gasita.manager_id != utilizator_id:
        raise HTTPException(status_code=403, detail="Acțiune nepermisă")
        
    db.delete(bariera_gasita)
    db.commit()
    return {"mesaj": "Barieră demontată"}


@router.post("/{bariera_id}/validare")
def ValidareAccesBariera(bariera_id: int, numar_inmatriculare: str, db: sesiune):

    # validam bariera si utilizatorul
    bariera_curenta = db.get(Bariera, bariera_id)
    utilizator_curent = db.exec(
        select(Utilizator)
        .where(Utilizator.numar_inmatriculare == numar_inmatriculare)
    ).first()
    if not bariera_curenta or not utilizator_curent or not bariera_curenta.id or not utilizator_curent.id:
        raise HTTPException(status_code=404, detail="Informatii gresite")

    # validam membru si parcare
    parcare_curenta = db.get(Parcare, bariera_curenta.parcare_id)
    membru_curent = db.exec(
        select(MembruParcare)
        .where(MembruParcare.parcare_id == bariera_curenta.parcare_id)
        .where(MembruParcare.utilizator_id == utilizator_curent.id)
    ).first()
    if not membru_curent or not parcare_curenta:
        raise HTTPException(status_code=403, detail="Acces refuzat la barieră")
    
    # inregistram istoricul si actualizam ocuparea
    inregistrare_istoric = Istoric(
        utilizator_id=utilizator_curent.id, 
        bariera_id=bariera_curenta.id, 
        actiune=bariera_curenta.tip
    )
    parcare_curenta.ocupare += 1 if bariera_curenta.tip == "intrare" else -1
    db.add(inregistrare_istoric)
    db.add(parcare_curenta)
    db.commit()
    
    return {"status": "deschis", "mesaj": "Acces permis"}