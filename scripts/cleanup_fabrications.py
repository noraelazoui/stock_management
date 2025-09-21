"""
Script pour nettoyer la collection 'fabrications' en supprimant les champs non autorisés.
"""
from models.database import db

# Liste des champs autorisés
ALLOWED_FIELDS = {"_id", "code", "optim", "recette_code", "nb_composantes", "quantite_a_fabriquer", "date_fabrication", "lot", "prix_formule", "detail-fabrication"}

def cleanup_fabrications():
    fabrications = db.fabrications.find({})
    for fab in fabrications:
        update_fields = {k: v for k, v in fab.items() if k in ALLOWED_FIELDS}
        db.fabrications.replace_one({"_id": fab["_id"]}, update_fields)
        print(f"Nettoyé fabrication: {fab.get('code', fab['_id'])}")

if __name__ == "__main__":
    cleanup_fabrications()
    print("Nettoyage terminé.")
