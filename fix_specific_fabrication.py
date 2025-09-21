from models.database import db
from bson import ObjectId
import json

# Classe pour permettre la sérialisation des ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Récupérer la fabrication qui a des problèmes
fabrication_id = "68bcc69883ac3787bb19353b"
fabrication = db.fabrications.find_one({"_id": ObjectId(fabrication_id)})

print("\n=== FABRICATION PROBLÉMATIQUE ===")
if fabrication:
    print(json.dumps(fabrication, indent=2, cls=JSONEncoder))
    
    # Vérifier si la formule associée existe
    formule = db.formules.find_one({"code": fabrication["code"], "optim": fabrication["optim"]})
    print(f"\nFormule trouvée: {formule is not None}")
    
    if formule:
        # Calculer manuellement les détails
        details = []
        composantes = formule.get("composantes", [])
        quantite_a_fabriquer = float(fabrication.get("quantite_a_fabriquer", 0))
        
        print("\n=== CALCUL MANUEL DES DÉTAILS ===")
        for comp in composantes:
            article_name = comp.get("article", "")
            article_code = article_name.split(" - ")[0] if " - " in article_name else article_name
            print(f"Recherche article: {article_code}")
            article = db.articles.find_one({"code": article_code})
            print(f"Article trouvé: {article is not None}")
            
            if article:
                pourcentage = float(comp.get("pourcentage", 0))
                quantite_fabrique = (pourcentage * quantite_a_fabriquer) / 100
                prix = float(article.get("prix", 0))
                detail = {
                    "article": comp.get("article", ""),
                    "dem": article.get("dem", ""),
                    "quantite_stock": article.get("quantite", 0),
                    "prix": prix,
                    "pourcentage": pourcentage,
                    "quantite_fabrique": quantite_fabrique,
                    "prix_total": (prix * pourcentage * quantite_a_fabriquer) / 100
                }
                details.append(detail)
                print(f"Détail calculé: {json.dumps(detail, indent=2)}")
        
        # Mettre à jour la fabrication avec les détails calculés
        if details:
            print("\n=== MISE À JOUR DE LA FABRICATION ===")
            result = db.fabrications.update_one(
                {"_id": ObjectId(fabrication_id)},
                {"$set": {"detail-fabrication": {"article": details}}}
            )
            print(f"Mise à jour réussie: {result.modified_count} document modifié")
            
            # Vérifier la fabrication mise à jour
            updated_fabrication = db.fabrications.find_one({"_id": ObjectId(fabrication_id)})
            print("\n=== FABRICATION APRÈS MISE À JOUR ===")
            print(json.dumps(updated_fabrication, indent=2, cls=JSONEncoder))
        else:
            print("Aucun détail n'a pu être calculé.")
    else:
        print("La formule associée n'a pas été trouvée.")
else:
    print("Fabrication non trouvée.")
