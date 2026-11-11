
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


# Table des utilisateurs
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    simulations = relationship(
        "Simulation",
        back_populates="user"
    )


# Table de l'historique des simulations
class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    debit = Column(Float, nullable=False)
    ajout = Column(Float, nullable=False)
    concentration = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)

    resultats = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship(
        "User",
        back_populates="simulations"
    )

