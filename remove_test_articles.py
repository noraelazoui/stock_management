from models.database import db

# Supprimer les articles de test insérés
codes = ["A001", "A002", "A003"]
db.articles.delete_many({"code": {"$in": codes}})

print("Articles de test supprimés de MongoDB.")
