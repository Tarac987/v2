import os
from datetime import datetime

# Définir le chemin du répertoire 'data'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
COUNTER_FILE = os.path.join(DATA_DIR, "numero_piece.txt")

# Créer le dossier 'data' s'il n'existe pas
os.makedirs(DATA_DIR, exist_ok=True)

def get_numero_piece():
    # Vérifie si le fichier existe
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            data = f.read().strip().split(',')
            last_year, last_numero_piece = int(data[0]), int(data[1])
            current_year = datetime.now().year
            # Si l'année a changé, on réinitialise le compteur
            if current_year != last_year:
                return 1
            return last_numero_piece + 1
    else:
        return 1

def save_numero_piece(numero_piece):
    current_year = datetime.now().year
    with open(COUNTER_FILE, 'w') as f:
        f.write(f"{current_year},{numero_piece}")
