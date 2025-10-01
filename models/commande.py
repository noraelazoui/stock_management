from models.database import db
from models.schemas import CommandeSchema as Schema, get_field_value

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
            Schema.REF: get_field_value(cmd, Schema.REF, "ref", default=""),
            Schema.RECEPTION_DATE: get_field_value(cmd, Schema.RECEPTION_DATE, "date_reception", default=""),
            Schema.PRODUCTS: get_field_value(cmd, Schema.PRODUCTS, "produits", default=[]),
            Schema.ORDER_INFO: get_field_value(cmd, Schema.ORDER_INFO, "infos_commande", default=[]),
            Schema.ORDER_DETAIL: get_field_value(cmd, Schema.ORDER_DETAIL, "infos_commande_detail", default=[]),
            Schema.STATUS: get_field_value(cmd, Schema.STATUS, "statut", default="Créé"),
            Schema.SUPPLIER: get_field_value(cmd, Schema.SUPPLIER, "fournisseur", default="")
        }
        self.collection.insert_one(cmd_structure)

    def update_commande(self, ref, new_cmd):
        """Met à jour une commande existante"""
        self.collection.update_one({Schema.REF: ref}, {"$set": new_cmd})

    def delete_commande(self, ref):
        """Supprime une commande"""
        self.collection.delete_one({Schema.REF: ref})

    def get_commande(self, ref):
        """Récupère une commande complète par référence"""
        return self.collection.find_one({Schema.REF: ref}, {"_id": 0})

    def get_detail_commande(self, ref):
        """Retourne la liste des lignes du champ 'detail_commande' pour une commande donnée"""
        doc = self.collection.find_one({Schema.REF: ref}, {"_id": 0, "detail_commande": 1})
        return get_field_value(doc, "detail_commande", default=[]) if doc else []

    def get_produits_commande(self, ref):
        """Retourne la liste des produits pour une commande donnée"""
        doc = self.collection.find_one({Schema.REF: ref}, {"_id": 0, Schema.PRODUCTS: 1})
        return get_field_value(doc, Schema.PRODUCTS, "produits", default=[]) if doc else []

    def get_infos_commande(self, ref):
        """Retourne la liste des infos_commande pour une commande donnée"""
        doc = self.collection.find_one({Schema.REF: ref}, {"_id": 0, Schema.ORDER_INFO: 1})
        return get_field_value(doc, Schema.ORDER_INFO, "infos_commande", default=[]) if doc else []

    # === GESTION DES PRODUITS ===
    def add_produit_to_commande(self, ref, product_data):
        """Ajoute un produit à une commande"""
        self.collection.update_one(
            {Schema.REF: ref}, 
            {"$push": {Schema.PRODUCTS: product_data}}
        )

    def update_produit_in_commande(self, ref, old_product, new_product):
        """Modifie un produit dans une commande"""
        # Utilise l'index pour identifier le produit à modifier
        commande = self.get_commande(ref)
        if commande:
            produits = get_field_value(commande, Schema.PRODUCTS, "produits", default=[])
            for i, produit in enumerate(produits):
                if produit == old_product:
                    self.collection.update_one(
                        {Schema.REF: ref}, 
                        {"$set": {f"{Schema.PRODUCTS}.{i}": new_product}}
                    )
                    break

    def delete_produit_from_commande(self, ref, product_data):
        """Supprime un produit d'une commande"""
        self.collection.update_one(
            {Schema.REF: ref}, 
            {"$pull": {Schema.PRODUCTS: product_data}}
        )

    # === GESTION DES INFOS COMMANDE DETAIL (Mode, Date, Fournisseur, etc.) ===
    def add_info_commande_detail(self, ref, info_data):
        """Ajoute une info détaillée à la commande (Mode, Date, Fournisseur, etc.)"""
        self.collection.update_one(
            {Schema.REF: ref}, 
            {"$push": {Schema.ORDER_DETAIL: info_data}}
        )

    def update_info_commande_detail(self, ref, old_info, new_info):
        """Modifie une info détaillée dans la commande"""
        commande = self.get_commande(ref)
        if commande:
            infos = get_field_value(commande, Schema.ORDER_DETAIL, "infos_commande_detail", default=[])
            for i, info in enumerate(infos):
                if info == old_info:
                    self.collection.update_one(
                        {Schema.REF: ref}, 
                        {"$set": {f"{Schema.ORDER_DETAIL}.{i}": new_info}}
                    )
                    break

    def delete_info_commande_detail(self, ref, info_data):
        """Supprime une info détaillée de la commande"""
        self.collection.update_one(
            {Schema.REF: ref}, 
            {"$pull": {Schema.ORDER_DETAIL: info_data}}
        )

    # === GESTION DES INFOS GENERALES ===
    def add_infos_commande(self, ref, infos_data):
        """Ajoute des infos générales à la commande"""
        self.collection.update_one(
            {Schema.REF: ref}, 
            {"$push": {Schema.ORDER_INFO: infos_data}}
        )

    def update_infos_commande(self, ref, old_infos, new_infos):
        """Modifie des infos générales dans la commande"""
        commande = self.get_commande(ref)
        if commande:
            infos = get_field_value(commande, Schema.ORDER_INFO, "infos_commande", default=[])
            for i, info in enumerate(infos):
                if info == old_infos:
                    self.collection.update_one(
                        {Schema.REF: ref}, 
                        {"$set": {f"{Schema.ORDER_INFO}.{i}": new_infos}}
                    )
                    break

    def delete_infos_commande(self, ref, infos_data):
        """Supprime des infos générales de la commande"""
        self.collection.update_one(
            {Schema.REF: ref}, 
            {"$pull": {Schema.ORDER_INFO: infos_data}}
        )

    # === UTILITAIRES ===
    def get_article_codes_by_type(self):
        """Retourne une liste de codes d'articles organisée par type"""
        from models.schemas import ArticleSchema as ArtSchema
        articles_db = list(db.articles.find({}, {"_id": 0, ArtSchema.CODE: 1, ArtSchema.TYPE: 1}))
        mp_codes = [get_field_value(a, ArtSchema.CODE, "code") for a in articles_db if get_field_value(a, ArtSchema.TYPE, "type") == "Matière première" and get_field_value(a, ArtSchema.CODE, "code")]
        add_codes = [get_field_value(a, ArtSchema.CODE, "code") for a in articles_db if get_field_value(a, ArtSchema.TYPE, "type") == "Additif" and get_field_value(a, ArtSchema.CODE, "code")]
        
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
        from models.schemas import SupplierSchema as SSchema
        fournisseurs_db = list(db.fournisseurs.find({}, {"_id": 0, SSchema.NAME: 1}))
        noms = [get_field_value(f, SSchema.NAME, "Nom", default="") for f in fournisseurs_db if get_field_value(f, SSchema.NAME, "Nom")]
        return noms

    def get_article_designation(self, code):
        """Retourne la désignation d'un article par son code"""
        from models.schemas import ArticleSchema as ArtSchema
        article = db.articles.find_one({ArtSchema.CODE: code}, {"_id": 0, ArtSchema.DESIGNATION: 1})
        return article.get("designation", "") if article else ""