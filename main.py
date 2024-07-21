# main.py ou l'équivalent dans votre application

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from controllers.code_comptable_controller import CodeComptableController

DATABASE_URL = "sqlite:///hotua_db.sqlite3"
# Configurer la base de données
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def initialize_data_if_needed():
    code_comptable_controller = CodeComptableController(db)
    codes_comptables = code_comptable_controller.get_all_codes_comptables()

    if not codes_comptables:
        # Si la table est vide, insérez les données de base
        code_comptable_controller.initialize_codes_comptables()
        print("Codes comptables initialisés.")

def main():
    # Vérifiez si les données doivent être initialisées
    initialize_data_if_needed()
    # Lancer le reste de l'application
    # ...

if __name__ == "__main__":
    main()
