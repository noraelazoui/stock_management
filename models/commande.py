from models.database import db

class CommandeModel:
    def __init__(self):
        self.collection = db.commandes

    @property
    def commandes(self):
        return list(self.collection.find({}, {"_id": 0}))

    def add_commande(self, cmd):
        """Ajoute une nouvelle commande avec structure complète"""
        # S'assurer que la structure est complète
        cmd_structure = {
            "ref": cmd.get("ref", ""),
            "date_reception": cmd.get("date_reception", ""),
            "produits": cmd.get("produits", []),
            "infos_commande": cmd.get("infos_commande", []),  # Statut, Remarque, Utilisateur
            "infos_commande_detail": cmd.get("infos_commande_detail", []),  # Mode, Date, Fournisseur, etc.
            "statut": cmd.get("statut", "Créé"),
            "fournisseur": cmd.get("fournisseur", "")
        }
        self.collection.insert_one(cmd_structure)

    def update_commande(self, ref, new_cmd):
        """Met à jour une commande existante"""
        self.collection.update_one({"ref": ref}, {"$set": new_cmd})

    def delete_commande(self, ref):
        """Supprime une commande"""
        self.collection.delete_one({"ref": ref})

    def get_commande(self, ref):
        """Récupère une commande complète par référence"""
        return self.collection.find_one({"ref": ref}, {"_id": 0})

    def get_detail_commande(self, ref):
        """Retourne la liste des lignes du champ 'detail_commande' pour une commande donnée"""
        doc = self.collection.find_one({"ref": ref}, {"_id": 0, "detail_commande": 1})
        return doc.get("detail_commande", []) if doc else []

    def get_produits_commande(self, ref):
        """Retourne la liste des produits pour une commande donnée"""
        doc = self.collection.find_one({"ref": ref}, {"_id": 0, "produits": 1})
        return doc.get("produits", []) if doc else []

    def get_infos_commande(self, ref):
        """Retourne la liste des infos_commande pour une commande donnée"""
        doc = self.collection.find_one({"ref": ref}, {"_id": 0, "infos_commande": 1})
        return doc.get("infos_commande", []) if doc else []

    # === GESTION DES PRODUITS ===
    def add_produit_to_commande(self, ref, product_data):
        """Ajoute un produit à une commande"""
        self.collection.update_one(
            {"ref": ref}, 
            {"$push": {"produits": product_data}}
        )

    def update_produit_in_commande(self, ref, old_product, new_product):
        """Modifie un produit dans une commande"""
        # Utilise l'index pour identifier le produit à modifier
        commande = self.get_commande(ref)
        if commande and "produits" in commande:
            produits = commande["produits"]
            for i, produit in enumerate(produits):
                if produit == old_product:
                    self.collection.update_one(
                        {"ref": ref}, 
                        {"$set": {f"produits.{i}": new_product}}
                    )
                    break

    def delete_produit_from_commande(self, ref, product_data):
        """Supprime un produit d'une commande"""
        self.collection.update_one(
            {"ref": ref}, 
            {"$pull": {"produits": product_data}}
        )

    # === GESTION DES INFOS COMMANDE DETAIL (Mode, Date, Fournisseur, etc.) ===
    def add_info_commande_detail(self, ref, info_data):
        """Ajoute une info détaillée à la commande (Mode, Date, Fournisseur, etc.)"""
        self.collection.update_one(
            {"ref": ref}, 
            {"$push": {"infos_commande_detail": info_data}}
        )

    def update_info_commande_detail(self, ref, old_info, new_info):
        """Modifie une info détaillée dans la commande"""
        commande = self.get_commande(ref)
        if commande and "infos_commande_detail" in commande:
            infos = commande["infos_commande_detail"]
            for i, info in enumerate(infos):
                if info == old_info:
                    self.collection.update_one(
                        {"ref": ref}, 
                        {"$set": {f"infos_commande_detail.{i}": new_info}}
                    )
                    break

    def delete_info_commande_detail(self, ref, info_data):
        """Supprime une info détaillée de la commande"""
        self.collection.update_one(
            {"ref": ref}, 
            {"$pull": {"infos_commande_detail": info_data}}
        )

    # === GESTION DES INFOS GENERALES ===
    def add_infos_commande(self, ref, infos_data):
        """Ajoute des infos générales à la commande"""
        self.collection.update_one(
            {"ref": ref}, 
            {"$push": {"infos_commande": infos_data}}
        )

    def update_infos_commande(self, ref, old_infos, new_infos):
        """Modifie des infos générales dans la commande"""
        commande = self.get_commande(ref)
        if commande and "infos_commande" in commande:
            infos = commande["infos_commande"]
            for i, info in enumerate(infos):
                if info == old_infos:
                    self.collection.update_one(
                        {"ref": ref}, 
                        {"$set": {f"infos_commande.{i}": new_infos}}
                    )
                    break

    def delete_infos_commande(self, ref, infos_data):
        """Supprime des infos générales de la commande"""
        self.collection.update_one(
            {"ref": ref}, 
            {"$pull": {"infos_commande": infos_data}}
        )

    # === UTILITAIRES ===
    def get_article_codes_by_type(self):
        """Retourne une liste de codes d'articles organisée par type"""
        articles_db = list(db.articles.find({}, {"_id": 0, "code": 1, "type": 1}))
        mp_codes = [a["code"] for a in articles_db if a.get("type") == "Matière première" and a.get("code")]
        add_codes = [a["code"] for a in articles_db if a.get("type") == "Additif" and a.get("code")]
        
        article_codes = []
        if mp_codes:
            article_codes.append("--- Matières premières ---")
            article_codes.extend(mp_codes)
        if add_codes:
            article_codes.append("--- Additifs ---")
            article_codes.extend(add_codes)
        if not article_codes:
            article_codes = ["Aucun article"]
        return article_codes

    def get_fournisseurs(self):
        """Retourne la liste des noms des fournisseurs"""
        fournisseurs_db = list(db.fournisseurs.find({}, {"_id": 0, "Nom": 1}))
        noms = [f.get("Nom", "") for f in fournisseurs_db if f.get("Nom", "")]
        return noms

    def get_article_designation(self, code):
        """Retourne la désignation d'un article par son code"""
        article = db.articles.find_one({"code": code}, {"_id": 0, "designation": 1})
        return article.get("designation", "") if article else ""