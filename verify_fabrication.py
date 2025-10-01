from models.database import db
from bson import ObjectId
import json

# Classe pour la sérialisation des ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# ID de la fabrication à vérifier
fabrication_id = "68bd45df9fd89d0d9561c5ad"

# Récupérer la fabrication
fabrication = db.fabrications.find_one({"_id": ObjectId(fabrication_id)})

# Afficher la fabrication avec ses détails
if fabrication:
    print("=== FABRICATION MISE À JOUR ===")
    print(json.dumps(fabrication, indent=2, cls=JSONEncoder))
    
    # Afficher spécifiquement les détails
    details = fabrication.get("detail-fabrication", {}).get("article", [])
    print(f"\nNombre de détails: {len(details)}")
    
    # Calculer le total des prix
    total_prix = sum(detail.get("prix_total", 0) for detail in details)
    print(f"Prix total de tous les composants: {total_prix}")
    
    # Afficher un récapitulatif des articles
    print("\n=== RÉCAPITULATIF DES ARTICLES ===")
    for i, detail in enumerate(details):
        article = detail.get("article", "")
        pourcentage = detail.get("pourcentage", 0)
        quantite = detail.get("quantite_fabrique", 0)
        prix = detail.get("prix_total", 0)
        print(f"{i+1}. {article}: {pourcentage}%, {quantite} kg, {prix} unités monétaires")
else:
    print(f"Fabrication avec ID {fabrication_id} non trouvée")
