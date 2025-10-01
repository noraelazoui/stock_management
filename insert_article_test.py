from models.database import db

# Insère un article complet pour test affichage data grid
article = {
    "code": "A100",
    "designation": "Test Grid",
    "type": "Additif",
    "unite": "usine",
    "prix": 10.5,
    "quantite": 50,
    "dem": "",
    "batch": "B001",
    "fab": "2025-08-26",
    "exp": "2026-08-26"
}
if not db.articles.find_one({"code": article["code"]}):
    db.articles.insert_one(article)
print("Article de test inséré.")
