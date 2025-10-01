from models.database import db

# Insérer des articles de test dans MongoDB
articles = [
    {"code": "A001", "designation": "Additif X", "type": "Additif", "unite": "usine"},
    {"code": "A002", "designation": "Matière Y", "type": "Matière première", "unite": "premix"},
    {"code": "A003", "designation": "Formule Z", "type": "Formule", "unite": "usine"}
]

for art in articles:
    if not db.articles.find_one({"code": art["code"]}):
        db.articles.insert_one(art)

print("Articles de test insérés dans MongoDB.")
