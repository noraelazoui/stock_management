from models.database import db
from bson.objectid import ObjectId
import json
from datetime import datetime

def print_json(obj):
    print(json.dumps(obj, indent=2, default=str))

print("1. Checking fabrication document:")
fabrication = db.fabrications.find_one({"_id": ObjectId("68bc624a6086478eaa6ba373")})
print_json(fabrication)

print("\n2. Checking corresponding formula:")
formule = db.formules.find_one({"code": "mama", "optim": "1"})
print_json(formule)

print("\n3. Attempting direct update:")
details = []
if formule and formule.get("composantes"):
    for comp in formule["composantes"]:
        article_code = comp.get("article", "").split(" - ")[0] if " - " in comp.get("article", "") else comp.get("article", "")
        article = db.articles.find_one({"code": article_code})
        if article:
            detail = {
                "article": comp.get("article", ""),
                "dem": article.get("dem", ""),
                "quantite_stock": article.get("quantite", 0),
                "prix": article.get("prix", 0),
                "pourcentage": float(comp.get("pourcentage", 0)),
                "quantite_fabrique": (float(comp.get("pourcentage", 0)) * float(fabrication.get("quantite_a_fabriquer", 0))) / 100,
                "prix_total": (float(article.get("prix", 0)) * float(comp.get("pourcentage", 0)) * float(fabrication.get("quantite_a_fabriquer", 0))) / 100
            }
            details.append(detail)

result = db.fabrications.update_one(
    {"_id": ObjectId("68bc624a6086478eaa6ba373")},
    {"$set": {"detail-fabrication.article": details}}
)
print(f"Update result - Modified count: {result.modified_count}, Matched count: {result.matched_count}")

print("\n4. Verifying update:")
updated_fab = db.fabrications.find_one({"_id": ObjectId("68bc624a6086478eaa6ba373")})
print_json(updated_fab.get("detail-fabrication", {}))
