
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from calculs import simulation

app = FastAPI(title="Simulateur de procédés")

templates = Jinja2Templates(directory="templates")


# Afficher la page d'accueil
@app.get("/", response_class=HTMLResponse)
def accueil(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)



# Récupérer les données saisies par l'utilisateur
class Donnees(BaseModel):
    debit: float
    ajout: float
    concentration: float
    temperature: float


# Lancer la simulation
@app.post("/calcul")
def calculer(d: Donnees):

    resultats = simulation(
        d.debit,
        d.ajout,
        d.concentration,
        d.temperature
    )

    return resultats


