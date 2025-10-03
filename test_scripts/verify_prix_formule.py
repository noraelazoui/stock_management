from models.database import db
from bson import ObjectId
import json

# Classe pour sérialiser les ObjectId en JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Paramètres de recherche
code = "mama"
optim = "1"

print(f"=== VÉRIFICATION DES FABRICATIONS AVEC CODE={code}, OPTIM={optim} ===")
fabrications = list(db.fabrications.find({"code": code, "optim": optim}))

print(f"Nombre de fabrications trouvées: {len(fabrications)}")

for i, fab in enumerate(fabrications):
    fab_id = fab.get("_id")
    prix_formule = fab.get("prix_formule", "Non défini")
    
    # Type de prix_formule
    prix_formule_type = type(prix_formule).__name__
    
    # Convertir en float si possible
    if isinstance(prix_formule, (str, int)):
        try:
            prix_formule_float = float(prix_formule)
        except (ValueError, TypeError):
            prix_formule_float = "Impossible à convertir"
    else:
        prix_formule_float = prix_formule
    
    # Récupérer les détails
    details = fab.get("detail-fabrication", {}).get("article", [])
    
    # Calculer la somme des prix_total
    prix_total_sum = 0.0
    for detail in details:
        prix_total = detail.get("prix_total", 0)
        if isinstance(prix_total, (str, int)):
            try:
                prix_total = float(prix_total)
            except (ValueError, TypeError):
                prix_total = 0.0
        prix_total_sum += prix_total
    
    # Arrondir à 2 décimales
    prix_total_sum = round(prix_total_sum, 2)
    
    print(f"\nFabrication {i+1}/{len(fabrications)}")
    print(f"ID: {fab_id}")
    print(f"Prix formule: {prix_formule} (type: {prix_formule_type})")
    if prix_formule_float != prix_formule:
        print(f"Prix formule converti en float: {prix_formule_float}")
    print(f"Nombre de détails: {len(details)}")
    print(f"Somme calculée des prix totaux: {prix_total_sum}")
    
    # Vérifier si le prix_formule correspond à la somme des prix_total
    if prix_formule_float != prix_total_sum:
        print(f"DIFFÉRENCE DÉTECTÉE! prix_formule={prix_formule_float}, somme calculée={prix_total_sum}")
        
        # Afficher plus de détails pour aider au diagnostic
        print("\nDétails des prix totaux:")
        for j, detail in enumerate(details):
            article = detail.get("article", "")
            prix = detail.get("prix", 0)
            quantite = detail.get("quantite_fabrique", 0)
            prix_total = detail.get("prix_total", 0)
            print(f"  {j+1}. {article}: prix={prix}, quantité={quantite}, prix_total={prix_total}")
    else:
        print("OK - Le prix formule correspond à la somme des prix totaux")

print("\n=== FIN DE LA VÉRIFICATION ===")
