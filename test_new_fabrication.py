from models.fabrication import Fabrication
import json
from bson import ObjectId
from datetime import datetime

# Classe pour la sérialisation des ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, o)

# Tester la création d'une fabrication avec le code amélioré
print("=== TEST DE CRÉATION D'UNE NOUVELLE FABRICATION ===")

# Paramètres de la fabrication
code = "mama"
optim = "1"
recette_code = "R003"
nb_composantes = "2"
quantite_a_fabriquer = "100"  # 100 kg
date_fabrication = datetime.now().strftime("%Y-%m-%d %H:%M")

# Créer la fabrication
fabrication = Fabrication.creer_fabrication(
    code=code,
    optim=optim,
    recette_code=recette_code,
    nb_composantes=nb_composantes,
    quantite_a_fabriquer=quantite_a_fabriquer,
    date_fabrication=date_fabrication
)

# Afficher le résultat
print("\n=== RÉSULTAT DE LA CRÉATION ===")
print(json.dumps(fabrication, indent=2, cls=JSONEncoder))

# Vérifier les détails
details = fabrication.get("detail-fabrication", {}).get("article", [])
print(f"\nNombre de détails créés: {len(details)}")

# Afficher les détails
if details:
    print("\n=== DÉTAILS DE LA FABRICATION ===")
    for i, detail in enumerate(details):
        article = detail.get("article", "")
        pourcentage = detail.get("pourcentage", 0)
        quantite = detail.get("quantite_fabrique", 0)
        prix_total = detail.get("prix_total", 0)
        print(f"{i+1}. {article}: {pourcentage}%, {quantite} kg, {prix_total} unités monétaires")
else:
    print("\nAUCUN DÉTAIL TROUVÉ !")
