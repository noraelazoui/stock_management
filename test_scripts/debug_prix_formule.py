from models.database import db
from bson import ObjectId
import json

# Fonction pour afficher les valeurs avec leur type
def print_value_with_type(value):
    return f"{value} ({type(value).__name__})"

# Classe pour sérialiser les ObjectId en JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Récupérer toutes les fabrications pour le code spécifié
code = "mama"
optim = "1"

print(f"\n=== RECHERCHE DES FABRICATIONS AVEC CODE={code}, OPTIM={optim} ===")
fabrications = list(db.fabrications.find({"code": code, "optim": optim}))

for i, fab in enumerate(fabrications):
    print(f"\nFabrication {i+1}/{len(fabrications)}")
    print(f"ID: {fab.get('_id')}")
    print(f"Code: {print_value_with_type(fab.get('code'))}")
    print(f"Optim: {print_value_with_type(fab.get('optim'))}")
    print(f"Prix Formule: {print_value_with_type(fab.get('prix_formule'))}")
    
    # Analyser les détails
    details = fab.get("detail-fabrication", {}).get("article", [])
    prix_total_sum = 0
    
    print(f"\nDétails ({len(details)}):")
    for j, detail in enumerate(details):
        article = detail.get("article", "")
        prix_total = detail.get("prix_total", 0)
        if isinstance(prix_total, str):
            try:
                prix_total = float(prix_total)
            except ValueError:
                prix_total = 0
        
        prix_total_sum += prix_total
        print(f"  {j+1}. {article}: Prix Total = {print_value_with_type(detail.get('prix_total'))}")
    
    print(f"\nSomme calculée des prix totaux: {prix_total_sum}")
    
    # Si le prix_formule est vide ou différent de la somme calculée
    if fab.get('prix_formule') != prix_total_sum:
        print(f"DIFFÉRENCE DÉTECTÉE: prix_formule={fab.get('prix_formule')}, somme calculée={prix_total_sum}")
        
        # Tester une mise à jour
        print(f"\nTentative de mise à jour...")
        result = db.fabrications.update_one(
            {"_id": fab.get("_id")},
            {"$set": {"prix_formule": prix_total_sum}}
        )
        print(f"Résultat: matched_count={result.matched_count}, modified_count={result.modified_count}")
        
        # Vérifier la mise à jour
        updated_fab = db.fabrications.find_one({"_id": fab.get("_id")})
        print(f"Nouveau prix_formule: {print_value_with_type(updated_fab.get('prix_formule'))}")

print("\n=== FIN DU DIAGNOSTIC ===")
