from models.database import db
from bson.objectid import ObjectId
from models.fabrication import Fabrication

def update_fabrication_details():
    # Get the details
    fabrication = db.fabrications.find_one({"code": "mama", "optim": "1"})
    if not fabrication:
        print("Fabrication not found")
        return

    # Get the formula
    formule = db.formules.find_one({"code": "mama", "optim": "1"})
    if not formule:
        print("Formula not found")
        return

    details = []
    composantes = formule.get("composantes", [])
    
    for comp in composantes:
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

    # Update MongoDB with proper error checking
    result = db.fabrications.update_one(
        {"_id": fabrication["_id"]},
        {"$set": {"detail-fabrication": {"article": details}}}
    )
    
    print(f"Modified count: {result.modified_count}")
    print(f"Matched count: {result.matched_count}")
    
    # Verify the update
    updated_fab = db.fabrications.find_one({"_id": fabrication["_id"]})
    print("\nUpdated fabrication:", updated_fab.get("detail-fabrication", {}))

update_fabrication_details()
