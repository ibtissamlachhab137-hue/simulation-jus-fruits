
import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base

# Récupération des informations depuis les variables Vercel
host = os.environ["MYSQLHOST"]
port = int(os.environ["MYSQLPORT"])
user = os.environ["MYSQLUSER"]
password = os.environ["MYSQLPASSWORD"]
database = os.environ["MYSQLDATABASE"]

# Création de l'URL de connexion
database_url = URL.create(
    drivername="mysql+pymysql",
    username=user,
    password=password,
    host=host,
    port=port,
    database=database,
    query={"charset": "utf8mb4"}
)

# Connexion à MySQL
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_size=1,
    max_overflow=0
)

# Gestion des sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base des modèles
Base = declarative_base()


# Fonction pour obtenir une session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

