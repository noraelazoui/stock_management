# Script pour supprimer les champs racine 'dem', 'prix', 'quantite' des articles dans MongoDB
from models.database import db

def remove_root_fields():
    db.articles.update_many({}, {"$unset": {"dem": "", "prix": "", "quantite": ""}})
    print("Champs racine supprimés.")

if __name__ == "__main__":
    remove_root_fields()
