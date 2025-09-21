from models.database import db
from bson import ObjectId
import json

# Classe pour permettre la sérialisation des ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Récupérer la fabrication par son ID
fabrication_id = "68bd43628185aa424551d06a"  # L'ID spécifique fourni par l'utilisateur
fabrication = db.fabrications.find_one({"_id": ObjectId(fabrication_id)})

print("\n=== FABRICATION PAR ID ===")
if fabrication:
    print(json.dumps(fabrication, indent=2, cls=JSONEncoder))
    
    # Vérifier et calculer les détails si nécessaire
    if not fabrication.get("detail-fabrication", {}).get("article"):
        print("\n=== DÉTAILS MANQUANTS - RÉCUPÉRATION DE LA FORMULE ===")
        formule = db.formules.find_one({"code": fabrication["code"], "optim": fabrication["optim"]})
        
        if formule:
            print(f"Formule trouvée: code={formule['code']}, optim={formule['optim']}")
            print(f"Nombre de composantes: {len(formule.get('composantes', []))}")
            
            # Calculer les détails
            details = []
            quantite_a_fabriquer = float(fabrication.get("quantite_a_fabriquer", 0))
            
            for comp in formule.get("composantes", []):
                article_name = comp.get("article", "")
                article_code = article_name.split(" - ")[0] if " - " in article_name else article_name
                print(f"Recherche article: {article_code}")
                article = db.articles.find_one({"code": article_code})
                
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
            
            # Mettre à jour la fabrication
            if details:
                result = db.fabrications.update_one(
                    {"_id": ObjectId(fabrication_id)},
                    {"$set": {"detail-fabrication": {"article": details}}}
                )
                print(f"Mise à jour effectuée: {result.modified_count} document(s) modifié(s)")
                
                # Afficher la fabrication mise à jour
                updated_fabrication = db.fabrications.find_one({"_id": ObjectId(fabrication_id)})
                print("\n=== FABRICATION APRÈS MISE À JOUR ===")
                print(json.dumps(updated_fabrication, indent=2, cls=JSONEncoder))
            else:
                print("Aucun détail à ajouter à la fabrication.")
        else:
            print(f"Aucune formule trouvée pour code={fabrication['code']}, optim={fabrication['optim']}")
else:
    print(f"Aucune fabrication trouvée avec l'ID {fabrication_id}")
