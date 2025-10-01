
from models.database import db


class ArticleModel:
    def __init__(self):
        self.collection = db.articles

    def add_article(self, art):
        if self.collection.find_one({"code": art["code"]}):
            return False
        self.collection.insert_one(art)
        return True

    def modify_article(self, art_code, new_data):
        result = self.collection.update_one({"code": art_code}, {"$set": new_data})
        return result.modified_count > 0

    def delete_article(self, art_code):
        self.collection.delete_one({"code": art_code})

    def get_article(self, art_code):
        return self.collection.find_one({"code": art_code})

    @property
    def articles(self):
        # Retourne tous les champs pour chaque article
        return [
            {k: v for k, v in art.items() if k != "_id"}
            for art in self.collection.find({
                "code": {"$exists": True},
                "designation": {"$exists": True},
                "type": {"$exists": True}
            })
        ]

    def get_article_dems(self, art_id):
        """Récupère toutes les DEM pour un article donné, peu importe le format du code."""
        print(f"\n=== Recherche des DEM pour l'article {art_id} ===")
        # Toujours extraire le code (avant le tiret si présent)
        code = art_id.split(' - ')[0].strip() if ' - ' in art_id else art_id.strip()
        articles = list(self.collection.find({"code": code}))
        dems = []
        for article in articles:
            # Vérifier si l'article a un champ produits
            if "produits" in article:
                for prod in article["produits"]:
                    if "DEM" in prod:
                        dems.append(prod["DEM"])
            # Vérifier si l'article a un champ dem direct
            if "dem" in article:
                dems.append(article["dem"])
        print(f"DEM trouvées: {dems}")
        print("=== Fin de la recherche ===\n")
        return list(set(dems))  # Retourne les DEM uniques

    def get_all_articles(self):
        """Retourne tous les articles sous forme de liste de dictionnaires."""
        return list(self.collection.find({}))

    @staticmethod
    def update_product_details(article_code, product_index, quantity_to_deduct):
        """
        Update the product details by deducting the specified quantity from the product at the given index.
        Dynamically recalculate the main quantity after the update.
        """
        from models.database import db

        # Fetch the article by code
        article = db.articles.find_one({"code": article_code})
        if not article:
            print(f"[DEBUG] Article with code {article_code} not found.")
            return False

        # Get the products list
        products = article.get("produits", [])
        if product_index < 0 or product_index >= len(products):
            print(f"[DEBUG] Invalid product index {product_index} for article {article_code}.")
            return False

        # Deduct the quantity from the specified product
        try:
            product = products[product_index]
            current_quantity = float(product.get("Quantité", 0))
            new_quantity = current_quantity - quantity_to_deduct

            if new_quantity < 0:
                print(f"[DEBUG] Quantity deduction exceeds available stock for product {product_index}.")
                return False

            product["Quantité"] = str(new_quantity)  # Update the product quantity

            # Recalculate the main quantity as the sum of all product quantities
            total_quantity = sum(float(p.get("Quantité", 0)) for p in products)

            # Update the article in the database
            db.articles.update_one(
                {"code": article_code},
                {"$set": {"produits": products, "quantite": total_quantity}}
            )

            print(f"[DEBUG] Updated product {product_index} for article {article_code}. New quantity: {new_quantity}.")
            return True

        except Exception as e:
            print(f"[DEBUG] Error updating product details: {e}")
            return False

    @staticmethod
    def recalculate_main_quantity(article_code):
        """
        Recalculate the main quantity (`quantite`) as the sum of all product quantities in the `produits` list.
        """
        from models.database import db

        # Fetch the article by code
        article = db.articles.find_one({"code": article_code})
        if not article:
            print(f"[DEBUG] Article with code {article_code} not found.")
            return False

        # Get the products list
        products = article.get("produits", [])

        # Calculate the total quantity
        try:
            total_quantity = sum(float(product.get("Quantité", 0)) for product in products)

            # Update the main quantity in the database
            db.articles.update_one(
                {"code": article_code},
                {"$set": {"quantite": total_quantity}}
            )

            print(f"[DEBUG] Recalculated main quantity for article {article_code}. New quantity: {total_quantity}.")
            return True

        except Exception as e:
            print(f"[DEBUG] Error recalculating main quantity: {e}")
            return False
