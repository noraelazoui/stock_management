# model.py
from models.database import db
from datetime import datetime
from dateutil.relativedelta import relativedelta

class StockModel:
    def get_repartition_quantite_par_article(self):
        # Agrège les quantités par article depuis MongoDB, nettoie et trie
        articles = list(self.db.articles.find({}, {"_id": 0, "designation": 1, "name": 1, "code": 1, "quantite": 1, "quantity": 1}))
        repartition = {}
        for art in articles:
            nom = art.get("designation") or art.get("name") or art.get("code") or "-"
            nom = str(nom).strip()
            qte = art.get("quantite")
            if qte is None:
                qte = art.get("quantity", 0)
            try:
                qte = float(qte)
            except Exception:
                qte = 0
            if nom and qte > 0:
                repartition[nom] = repartition.get(nom, 0) + qte
        # Trier par quantité décroissante
        repartition_sorted = dict(sorted(repartition.items(), key=lambda x: x[1], reverse=True))
        return repartition_sorted
    def __init__(self):
        self.stock_premix = {"Sucre": 500, "Cacao": 300, "Additifs": 200}
        self.stock_usine = {"Produit A": 150, "Produit B": 100, "Produit C": 50}
        self.seuil_premix = 100
        self.seuil_usine = 50
        self.ratios_transformation = {"Sucre": 0.6, "Cacao": 0.7, "Additifs": 0.5}
        self.db = db

    def calcul_stock_global(self):
        global_stock = {}
        for key, value in self.stock_premix.items():
            global_stock[key] = value
        for key, value in self.stock_usine.items():
            global_stock[key] = global_stock.get(key, 0) + value
        return global_stock

    def calcul_taux_transformation(self):
        # Utilise les données MongoDB
        premix = list(self.db.articles.find({"type": "Premix"}, {"_id": 0, "designation": 1, "quantite": 1, "quantity": 1}))
        usine = list(self.db.articles.find({"type": "Usine"}, {"_id": 0, "designation": 1, "quantite": 1, "quantity": 1}))
        taux = {}
        for art_premix in premix:
            nom = art_premix.get("designation", "-")
            qte_premix = art_premix.get("quantite")
            if qte_premix is None:
                qte_premix = art_premix.get("quantity", 0)
            try:
                qte_premix = float(qte_premix)
            except Exception:
                qte_premix = 0
            # On cherche la quantité correspondante en usine (même nom si possible)
            qte_usine = 0
            for art_usine in usine:
                if art_usine.get("designation", "-") == nom:
                    qte_usine = art_usine.get("quantite")
                    if qte_usine is None:
                        qte_usine = art_usine.get("quantity", 0)
                    try:
                        qte_usine = float(qte_usine)
                    except Exception:
                        qte_usine = 0
                    break
            total = qte_premix + qte_usine
            if total > 0:
                taux[nom] = round((qte_usine / total) * 100, 2)
        return taux

    def calcul_jours_production(self):
        # Utilise les données MongoDB
        usine = list(self.db.articles.find({"type": "Usine"}, {"_id": 0, "designation": 1, "quantite": 1, "quantity": 1}))
        jours = {}
        for art_usine in usine:
            nom = art_usine.get("designation", "-")
            qte = art_usine.get("quantite")
            if qte is None:
                qte = art_usine.get("quantity", 0)
            try:
                qte = float(qte)
            except Exception:
                qte = 0
            jours[nom] = int(qte // 50) if qte > 0 else 0
        return jours

    def verifier_alertes(self):
        """Vérifie les alertes de stock bas et d'expiration imminente"""
        alertes = {
            'stock_bas': [],
            'expiration': []
        }
        
        today = datetime.now()
        
        # Parcourir tous les articles avec produits
        for article in self.db.articles.find({"produits": {"$exists": True, "$ne": []}}):
            designation = article.get('designation', article.get('name', 'Article sans nom'))
            code = article.get('code', '-')
            
            for prod in article.get('produits', []):
                dem = prod.get('dem', '-')
                quantity = prod.get('quantity', 0)
                threshold = prod.get('threshold', 10)
                exp_date_str = prod.get('expiration_date')
                alert_months = prod.get('alert_months', 3)
                batch = prod.get('batch', prod.get('lot', '-'))
                
                # Vérifier stock bas
                try:
                    if float(quantity) <= float(threshold):
                        alertes['stock_bas'].append({
                            'article': designation,
                            'code': code,
                            'dem': dem,
                            'batch': batch,
                            'quantity': float(quantity),
                            'threshold': float(threshold),
                            'pourcentage': round((float(quantity) / float(threshold)) * 100, 1) if threshold > 0 else 0
                        })
                except (ValueError, TypeError):
                    pass
                
                # Vérifier expiration
                if exp_date_str:
                    try:
                        exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d')
                        alert_date = exp_date - relativedelta(months=int(alert_months))
                        
                        if today >= alert_date:
                            days_until_exp = (exp_date - today).days
                            
                            # Déterminer le niveau de criticité
                            if days_until_exp < 0:
                                niveau = 'EXPIRÉ'
                            elif days_until_exp <= 30:
                                niveau = 'CRITIQUE'
                            elif days_until_exp <= 90:
                                niveau = 'ATTENTION'
                            else:
                                niveau = 'AVERTISSEMENT'
                            
                            alertes['expiration'].append({
                                'article': designation,
                                'code': code,
                                'dem': dem,
                                'batch': batch,
                                'exp_date': exp_date_str,
                                'days_left': days_until_exp,
                                'niveau': niveau,
                                'quantity': float(quantity) if quantity else 0
                            })
                    except (ValueError, TypeError):
                        pass
        
        # Trier par criticité
        alertes['stock_bas'].sort(key=lambda x: x['pourcentage'])
        alertes['expiration'].sort(key=lambda x: x['days_left'])
        
        return alertes

    def get_stock_premix(self):
        # Lire les articles dont unite = 'premix' (insensible à la casse)
        return list(self.db.articles.find({"unite": {"$regex": "^premix$", "$options": "i"}}, {"_id": 0}))

    def get_stock_usine(self):
        # Lire les articles dont unite = 'usine' (insensible à la casse)
        return list(self.db.articles.find({"unite": {"$regex": "^usine$", "$options": "i"}}, {"_id": 0}))

    def get_stock_global(self):
        # Regroupe tous les articles
        return list(self.db.articles.find({}, {"_id": 0}))

    def get_fournisseur(self, nom):
        # Retourne le fournisseur d'un article
        f = self.db.fournisseurs.find_one({"Nom": nom}, {"_id": 0})
        if f:
            return f.get("Nom", f.get("name", "-"))
        return "-"

    def get_inventaire(self):
        # Retourne tous les articles pour l'inventaire
        return list(self.db.articles.find({}, {"_id": 0}))
