import json
import os

CARTELLA = os.path.expanduser("~/.local/share/zenith-stashbar")
FILE = os.path.join(CARTELLA, "stash.json")

def carica():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def salva(elementi):
    os.makedirs(CARTELLA, exist_ok=True)
    with open(FILE, "w") as f:
        json.dump(elementi, f, indent=2)

def aggiungi(contenuto, tipo):
    elementi = carica()
    elementi.append({
        "contenuto": contenuto,
        "tipo": tipo
    })
    salva(elementi)

def rimuovi(indice):
    elementi = carica()
    if 0 <= indice < len(elementi):
        elementi.pop(indice)
        salva(elementi)
