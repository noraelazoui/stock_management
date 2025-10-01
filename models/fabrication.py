from datetime import datetime
from models.database import db
import uuid

class Fabrication:
    def __init__(self, code=None, optim=None, recette_code=None, nb_composantes=None, quantite_a_fabriquer=None, date_fabrication=None, lot="", prix_formule=""):
        self.code = code
        self.optim = optim
        self.recette_code = recette_code
        self.nb_composantes = nb_composantes
        self.quantite_a_fabriquer = quantite_a_fabriquer
        self.date_fabrication = date_fabrication if date_fabrication else datetime.now().strftime("%Y-%m-%d %H:%M")
        self.lot = lot
        self.prix_formule = prix_formule

    @staticmethod
    def get_by_code_optim_lot(code, optim, lot):
        """
        Recherche une fabrication par code, optim et lot (lot est requis).
        """
        print("\nDébut recherche fabrication avec lot ===")
        print(f"Recherche fabrication avec code='{code}', optim='{optim}', lot='{lot}'")

        # Essayer différents types pour optim et lot
        doc = db.fabrications.find_one({"code": code, "optim": optim, "lot": lot})
        print(f"\n docs  {doc} ")
        if not doc and isinstance(optim, str):
            try:
                numeric_optim = int(optim)
                doc = db.fabrications.find_one({"code": code, "optim": numeric_optim, "lot": lot})
                print(f"Tentative avec optim numérique: {numeric_optim}")
            except ValueError:
                pass

        if not doc and isinstance(optim, (int, float)):
            doc = db.fabrications.find_one({"code": code, "optim": str(optim), "lot": lot})
            print(f"Tentative avec optim string: {str(optim)}")

        print(f"\nRésultat de la recherche: {doc}")
        print("=== Fin recherche fabrication avec lot\n")

        return doc

    @staticmethod
    def creer_fabrication(code, optim, recette_code, nb_composantes, quantite_a_fabriquer=None, date_fabrication=None, lot="", prix_formule=""):
        fabrication_id = str(uuid.uuid4())
        details = []

        print(f"\n[DEBUG] Recherche de la formule : code={code}, optim={optim}, lot={lot}")
        formule = db.formules.find_one({"code": code, "optim": optim})
        if not formule:
            print(f"[DEBUG] Aucune formule trouvée pour code={code}, optim={optim}")
            return None

        try:
            composantes = formule.get("composantes", [])
            composantes2 = formule.get("detail-fabrication", [])
            print(f"[DEBUG] composantes: {composantes}")
            print(f"[DEBUG] composantes2: {composantes2}")
            if quantite_a_fabriquer and composantes:
                quantite = float(quantite_a_fabriquer)
                prix_total_somme = 0.0  # Initialiser la somme des prix_total
                for comp in composantes:
                    article_name = comp.get("article", "")
                    article_code = article_name.split(" - ")[0] if " - " in article_name else article_name
                    # Vérifier si c'est une formule
                    formule_doc = db.formules.find_one({"code": article_code})
                    pourcentage = float(comp.get("pourcentage", 0))
                    quantite_fabrique = (pourcentage * quantite) / 100
                    if formule_doc:
                        # Cas formule : récupérer les champs spécifiques
                        optim_value = formule_doc.get("optim", "")
                        recette_value = formule_doc.get("recette_code", "")
                        fabrication_formule = db.fabrications.find_one({"code": article_code, "optim": optim_value, "recette_code": recette_value})
                        print(f"[DEBUG] fabrication_formule: {fabrication_formule}")
                        if fabrication_formule:
                            prix_formule_composante = float(fabrication_formule.get("prix_formule", 0))
                            quantite_fabrique_composante = float(fabrication_formule.get("quantite_a_fabriquer", 0))
                            prix = round(prix_formule_composante / quantite_fabrique_composante, 4) if quantite_fabrique_composante else 0.0
                            quantite_stock = quantite_fabrique_composante
                        else:
                            prix = 0.0
                            quantite_stock = 0.0
                        prix_total = round((prix * pourcentage * quantite) / 100, 2)
                        prix_total_somme += prix_total  # Ajouter au total
                        detail = {
                            "article": article_code,
                            "prix": prix,
                            "quantite_stock": quantite_stock,
                            "pourcentage": pourcentage,
                            "optim": optim_value,
                            "recette": recette_value,
                            "quantite_fabrique": round(quantite_fabrique, 2),
                            "prix_total": prix_total,
                            "fabrication_id": fabrication_id
                        }
                        details.append(detail)
                        # Décrémenter le stock du premix utilisé
                        db.articles.update_one(
                            {"code": article_code},
                            {"$inc": {"quantite": -quantite_fabrique}}
                        )
                    else:
                        # Cas article classique
                        article = db.articles.find_one({"code": article_code})
                        if article:
                            prix = float(article.get("prix", 0))
                            prix_total = round((prix * pourcentage * quantite) / 100, 2)
                            prix_total_somme += prix_total  # Ajouter au total
                            detail = {
                                "article": article_name,
                                "dem": article.get("dem", ""),
                                "quantite_stock": article.get("quantite", 0),
                                "prix": prix,
                                "pourcentage": pourcentage,
                                "quantite_fabrique": round(quantite_fabrique, 2),
                                "prix_total": prix_total,
                                "fabrication_id": fabrication_id
                            }
                            details.append(detail)
                            # Décrémenter le stock de la matière première
                            db.articles.update_one(
                                {"code": article_code},
                                {"$inc": {"quantite": -quantite_fabrique}}
                            )
                # Calculer le prix_formule comme la somme des prix_total divisée par la quantité fabriquée
                prix_formule_initial = round(prix_total_somme / quantite, 4) if quantite else 0.0
                print(f"[DEBUG] Calcul prix_formule: somme_prix_total={prix_total_somme}, quantite_a_fabriquer={quantite}, prix_formule_calculé={prix_formule_initial}")
        except Exception as e:
            print(f"[DEBUG] Erreur lors du calcul des détails: {e}")

        # Calcul du prix_formule
        if prix_formule not in (None, "", 0):
            prix_formule_initial = prix_formule
        else:
            prix_formule_initial = round(prix_total_somme / quantite, 4) if quantite else 0.0
        fabrication = {
            "_id": fabrication_id,
            "code": code,
            "optim": optim,
            "recette_code": recette_code,
            "nb_composantes": nb_composantes,
            "quantite_a_fabriquer": quantite_a_fabriquer,
            "date_fabrication": date_fabrication or datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "lot": lot,
            "prix_formule": prix_formule_initial,
            "detail-fabrication": details
        }

        print(f"[DEBUG] Prix formule initial calculé: {prix_formule_initial}")
        print(f"[DEBUG] Lot: {lot}")

        # --- Validation des champs autorisés ---
        allowed_fields = {"_id", "code", "optim", "recette_code", "nb_composantes", "quantite_a_fabriquer", "date_fabrication", "lot", "prix_formule", "detail-fabrication"}
        fabrication = {k: v for k, v in fabrication.items() if k in allowed_fields}

        try:
            result = db.fabrications.insert_one(fabrication)
            print(f"[DEBUG] Fabrication insérée avec ID: {fabrication_id}")
        except Exception as e:
            print(f"[DEBUG] Erreur lors de l'insertion de la fabrication: {e}")

        return fabrication

    @staticmethod
    def get_details_fabrication(code, optim):
        fabrication = db.fabrications.find_one({"code": code, "optim": optim})
        if not fabrication:
            print(f"[DEBUG] Aucune fabrication trouvée pour code={code}, optim={optim}")
            return None

        details = fabrication.get("detail-fabrication", [])
        if details:
            print(f"[DEBUG] Détails récupérés pour la fabrication code={code}, optim={optim}")
        else:
            print(f"[DEBUG] Aucun détail trouvé pour la fabrication code={code}, optim={optim}")
        return details

    @staticmethod
    def set_details_fabrication(code, optim, lot, details):
        """
        Met à jour le champ 'details' d'une fabrication avec la liste des articles fournie.
        Enregistre sous la forme : { 'details': [ ... ] }
        Calcule et met à jour également le prix_formule comme la somme des prix_total.
        """
        # Nettoyer et standardiser les détails
        formatted_details = []
        prix_total_sum = 0.0  # Pour calculer la somme des prix_total

        # Récupérer la quantité à fabriquer globale depuis la fabrication
        fabrication = db.fabrications.find_one({"code": code, "optim": optim, "lot": lot})
        quantite_a_fabriquer_global = fabrication.get("quantite_a_fabriquer", 0) if fabrication else 0

        for detail in details:
            formatted_detail = {
                "article": detail.get("article", ""),
                "dem": detail.get("dem", ""),
                "lot": detail.get("lot", ""),
                "quantite_stock": detail.get("quantite_stock", 0),
                "prix": detail.get("prix", 0.0),
                "pourcentage": detail.get("pourcentage", 0.0),
                "quantite_fabrique": detail.get("quantite_fabrique", 0.0),
                "prix_total": detail.get("prix_total", 0.0)
            }
            formatted_details.append(formatted_detail)
            prix_total_sum += formatted_detail["prix_total"]

        # Calculer le prix formule comme la somme des prix_total divisée par la quantité à fabriquer globale
        prix_formule_final = round(prix_total_sum / quantite_a_fabriquer_global, 4) if quantite_a_fabriquer_global else 0.0

        # Mettre à jour dans la base de données avec le prix_formule calculé
        result = db.fabrications.update_one(
            {"code": code, "optim": optim, "lot": lot},
            {"$set": {
                "detail-fabrication": formatted_details,
                "prix_formule": prix_formule_final
            }}
        )

        if result.matched_count == 0:
            print(f"[DEBUG] Aucun enregistrement trouvé pour code={code}, optim={optim}")
        else:
            print(f"[DEBUG] Détails mis à jour pour la fabrication code={code}, optim={optim}")

        return result

    @staticmethod
    def get_all_fabrications():
        fabrications = list(db.fabrications.find())
        print("[DEBUG] Fabrications dans la base de données :")
        for fabrication in fabrications:
            print(fabrication)
        return fabrications

    @staticmethod
    def supprimer_fabrication(code, optim):
        """
        Supprime une fabrication spécifique de la base de données en fonction du code et de l'optim.
        """
        try:
            result = db.fabrications.delete_one({"code": code, "optim": optim})
            if result.deleted_count > 0:
                print(f"[DEBUG] Fabrication supprimée : code={code}, optim={optim}")
                return True
            else:
                print(f"[DEBUG] Aucune fabrication trouvée pour suppression : code={code}, optim={optim}")
                return False
        except Exception as e:
            print(f"[DEBUG] Erreur lors de la suppression de la fabrication : {e}")
            return False

    @staticmethod
    def update_quantite_a_fabriquer(code, optim):
        """
        Met à jour la quantite_a_fabriquer en fonction de la formule:
        quantite_a_fabriquer (nouvelle) = quantite_stock - quantite_a_fabriquer (ancienne)
        """
        try:
            # Récupérer l'enregistrement de fabrication
            fabrication = db.fabrications.find_one({"code": code, "optim": optim})
            if not fabrication:
                print(f"[DEBUG] Aucun enregistrement trouvé pour code={code}, optim={optim}")
                return False

            # Récupérer la quantite_a_fabriquer actuelle et quantite_stock
            details = fabrication.get("detail-fabrication", [])
            for detail in details:
                quantite_stock = detail.get("quantite_stock", 0)
                quantite_a_fabriquer_old = fabrication.get("quantite_a_fabriquer", 0)
                # Calculer la nouvelle quantite_a_fabriquer
                quantite_a_fabriquer_new = quantite_stock - quantite_a_fabriquer_old
                fabrication["quantite_a_fabriquer"] = quantite_a_fabriquer_new
                print(f"[DEBUG] Nouvelle quantite_a_fabriquer: {quantite_a_fabriquer_new}")

            # Mettre à jour l'enregistrement de fabrication dans la base de données
            db.fabrications.update_one(
                {"code": code, "optim": optim},
                {"$set": {"quantite_a_fabriquer": fabrication["quantite_a_fabriquer"]}}
            )
            print("[DEBUG] Mise à jour réussie de quantite_a_fabriquer")
            return True
        except Exception as e:
            print(f"[DEBUG] Erreur lors de la mise à jour de quantite_a_fabriquer: {str(e)}")
            return False

    @staticmethod
    def update_quantite_article(dem, quantite_utilisee):
        """
        Met à jour la quantité dans la table article et dans la liste produits pour un DEM spécifique.

        Args:
            dem (str): Le DEM à mettre à jour.
            quantite_utilisee (float): La quantité à déduire.
        """
        try:
            # Récupérer l'article correspondant au DEM
            article = db.articles.find_one({"produits.dem": dem})
            if not article:
                print(f"[DEBUG] Aucun article trouvé pour DEM: {dem}")
                return

            # Parcourir les produits pour trouver le DEM spécifique
            produits = article.get("produits", [])
            for produit in produits:
                if produit.get("dem") == dem:
                    produit["quantite"] = max(0, produit.get("quantite", 0) - quantite_utilisee)
                    print(f"[DEBUG] Mise à jour du produit DEM: {dem}, Nouvelle quantité: {produit['quantite']}")
                    break

            # Mettre à jour l'article dans la base de données
            db.articles.update_one(
                {"_id": article["_id"]},
                {"$set": {"produits": produits}}
            )
            print(f"[DEBUG] Article mis à jour avec succès pour DEM: {dem}")
        except Exception as e:
            print(f"[DEBUG] Erreur lors de la mise à jour de l'article pour DEM: {dem} : {e}")
