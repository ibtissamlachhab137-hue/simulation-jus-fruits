
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from database import get_db
from models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")
password_hasher = PasswordHash.recommended()


# Page d'inscription
@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


# Traitement de l'inscription
@router.post("/register")
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    email = email.strip().lower()

    if len(password) < 8:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Le mot de passe doit contenir au moins 8 caractères."},
            status_code=400
        )

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Cette adresse e-mail est déjà utilisée."},
            status_code=400
        )

    hashed_password = password_hasher.hash(password)

    new_user = User(
        email=email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    request.session["user_id"] = new_user.id

    return RedirectResponse("/", status_code=303)


# Page de connexion
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# Traitement de la connexion
@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    email = email.strip().lower()

    user = db.query(User).filter(User.email == email).first()

    if not user or not password_hasher.verify(
        password,
        user.password_hash
    ):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Adresse e-mail ou mot de passe incorrect."},
            status_code=400
        )

    request.session["user_id"] = user.id

    return RedirectResponse("/", status_code=303)


# Déconnexion
@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)
