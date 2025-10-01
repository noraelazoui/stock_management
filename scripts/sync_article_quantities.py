"""
Script pour vérifier et corriger la cohérence des quantités dans la collection 'articles'.
La quantité principale doit être égale à la somme des quantités des produits.
"""
from models.database import db

def sync_article_quantities():
    articles = db.articles.find({})
    for art in articles:
        produits = art.get("produits", [])
        total = sum(float(prod.get("Quantité", 0)) for prod in produits)
        if art.get("quantite", 0) != total:
            db.articles.update_one({"_id": art["_id"]}, {"$set": {"quantite": total}})
            print(f"Article {art.get('code', art['_id'])} corrigé: quantite={total}")

if __name__ == "__main__":
    sync_article_quantities()
    print("Vérification et correction terminées.")
