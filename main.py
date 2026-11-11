

import os
import json

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from calculs import simulation
from database import Base, engine, get_db
from models import User, Simulation
from auth import router as auth_router

app = FastAPI(title="Simulateur de procédés")

templates = Jinja2Templates(directory="templates")

# Gestion des sessions utilisateur
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SECRET_KEY"],
    same_site="lax",
    https_only=os.getenv("VERCEL") == "1"
)

# Création des tables MySQL au démarrage
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

# Activation des routes d'inscription et de connexion
app.include_router(auth_router)


# Vérifier si l'utilisateur est connecté
def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Connexion nécessaire")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        request.session.clear()
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")

    return user


# Page principale
@app.get("/", response_class=HTMLResponse)
def accueil(
    request: Request,
    user=Depends(get_current_user)
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"user": user}
    )


# Données reçues du formulaire de simulation
class Donnees(BaseModel):
    debit: float
    ajout: float
    concentration: float
    temperature: float


# Effectuer une simulation et enregistrer son résultat
@app.post("/calcul")
def calculer(
    d: Donnees,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resultats = simulation(
        d.debit,
        d.ajout,
        d.concentration,
        d.temperature
    )

    nouvelle_simulation = Simulation(
        user_id=user.id,
        debit=d.debit,
        ajout=d.ajout,
        concentration=d.concentration,
        temperature=d.temperature,
        resultats=json.dumps(resultats, ensure_ascii=False)
    )

    db.add(nouvelle_simulation)
    db.commit()

    return resultats

# Historique des simulations de l'utilisateur connecté
@app.get("/historique", response_class=HTMLResponse)
def afficher_historique(
    request: Request,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    simulations = (
        db.query(Simulation)
        .filter(Simulation.user_id == user.id)
        .order_by(Simulation.created_at.desc())
        .all()
    )

    historique = []

    for sim in simulations:
        historique.append({
            "simulation": sim,
            "resultats": json.loads(sim.resultats)
        })

    return templates.TemplateResponse(
        request=request,
        name="historique.html",
        context={
            "user": user,
            "historique": historique
        }
    )

