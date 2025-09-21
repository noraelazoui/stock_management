# Script to remove 'quantite' field from all articles in MongoDB
from models.database import db

def remove_article_quantite_field():
    result = db.articles.update_many({}, {"$unset": {"quantite": ""}})
    print(f"Articles updated: {result.modified_count}")

if __name__ == "__main__":
    remove_article_quantite_field()
