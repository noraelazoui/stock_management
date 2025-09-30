import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.database import db
from models.fabrication import Fabrication
import datetime
def insert_fournisseurs():
    db.fournisseurs.delete_many({})
    fournisseurs = [
        {"Nom": "Fournisseur A", "Téléphone": "0123456789", "Email": "a@demo.com", "Date création": datetime.datetime.now().strftime("%Y-%m-%d")},
        {"Nom": "Fournisseur B", "Téléphone": "0987654321", "Email": "b@demo.com", "Date création": datetime.datetime.now().strftime("%Y-%m-%d")}
    ]
    db.fournisseurs.insert_many(fournisseurs)
def insert_articles():
    db.articles.delete_many({})
    articles = [
        {"code": "MPA", "designation": "Matière A", "type": "matiere", "quantite": 100, "fournisseur": "Fournisseur A"},
        {"code": "MPB", "designation": "Matière B", "type": "matiere", "quantite": 200, "fournisseur": "Fournisseur B"},
        {"code": "MPC", "designation": "Matière C", "type": "matiere", "quantite": 150, "fournisseur": "Fournisseur A"},
        {"code": "ADD1", "designation": "Additif 1", "type": "additif", "quantite": 50, "fournisseur": "Fournisseur B"},
    ]
    db.articles.insert_many(articles)

def make_produit(code, designation, dem, quantite_commande, quantite_reel, prix_uni, tva):
    prix_uni = float(prix_uni)
    tva = float(tva)
    prix_ttc = round(prix_uni * (1 + tva / 100), 2)
    montant = round(quantite_commande * prix_ttc, 2)
    montant_reel = round(quantite_reel * prix_ttc, 2)
    return {
        "code": code,
        "designation": designation,
        "dem": dem,
        "quantite_commande": quantite_commande,
        "quantite_reel": quantite_reel,
        "prix_uni": prix_uni,
        "tva": tva,
        "prix_ttc": prix_ttc,
        "montant": montant,
        "montant_reel": montant_reel
    }

def insert_commandes():
    db.commandes.delete_many({})
    commandes = [
        {
            "ref": "CMD001",
            "date_reception": datetime.datetime.now().strftime("%Y-%m-%d"),
            "produits": [
                {**make_produit("MPA", "Matière A", "DEM001", 100, 100, 10, 20), "optim_formule": "1", "recette_formule": "R001"},
                {**make_produit("MPA", "Matière A", "DEM002", 50, 50, 11, 20), "optim_formule": "1", "recette_formule": "R001"},
                {**make_produit("MPA", "Matière A", "DEM003", 30, 30, 12, 20), "optim_formule": "1", "recette_formule": "R001"},
            ],
            "infos_commande": [
                {"statut": "Validée", "remarque": "Livraison rapide", "utilisateur": "admin"}
            ],
            "infos_commande_detail": [
                {"mode": "Express", "date": datetime.datetime.now().strftime("%Y-%m-%d"), "fournisseur": "Fournisseur A", "payement": "CB", "adresse": "1 rue Alpha", "transport": "Camion", "numero": "BR001"}
            ],
            "statut": "Créé",
            "fournisseur": "Fournisseur A"
        },
        {
            "ref": "CMD002",
            "date_reception": datetime.datetime.now().strftime("%Y-%m-%d"),
            "produits": [
                {**make_produit("MPB", "Matière B", "DEM004", 200, 200, 12, 20), "optim_formule": "1", "recette_formule": "R002"},
                {**make_produit("MPB", "Matière B", "DEM005", 80, 80, 13, 20), "optim_formule": "1", "recette_formule": "R002"},
                {**make_produit("MPC", "Matière C", "DEM006", 150, 150, 8, 10), "optim_formule": "1", "recette_formule": "R002"},
                {**make_produit("ADD1", "Additif 1", "DEM007", 50, 50, 5, 10), "optim_formule": "1", "recette_formule": "R002"},
            ],
            "infos_commande": [
                {"statut": "En attente", "remarque": "Paiement à la livraison", "utilisateur": "user1"}
            ],
            "infos_commande_detail": [
                {"mode": "Standard", "date": datetime.datetime.now().strftime("%Y-%m-%d"), "fournisseur": "Fournisseur B", "payement": "Virement", "adresse": "2 rue Beta", "transport": "Train", "numero": "BR002"}
            ],
            "statut": "Créé",
            "fournisseur": "Fournisseur B"
        }
    ]
    db.commandes.insert_many(commandes)
    # Les commandes servent uniquement à la traçabilité, pas de modification du stock ici

def insert_formules():
    db.formules.delete_many({})
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    db.formules.insert_one({
        "code": "PREMIX1",
        "type": "formule",
        "optim": "1",
        "recette_code": "R001",
        "recette_formule": "R001",  # Ajout
        "optim_formule": "1",       # Ajout
        "designation": "Premix 1",
        "description": "Premix de matières premières A et B.",
        "date_creation": now,
        "composantes": [
            {"article": "MPA", "pourcentage": 60, "type": "simple"},
            {"article": "MPB", "pourcentage": 40, "type": "simple"}
        ]
    })
    db.formules.insert_one({
        "code": "PREMIX2",
        "type": "formule",
        "optim": "1",
        "recette_code": "R002",
        "recette_formule": "R002",  # Ajout
        "optim_formule": "1",       # Ajout
        "designation": "Premix 2",
        "description": "Premix de matières premières C et additif 1.",
        "date_creation": now,
        "composantes": [
            {"article": "MPC", "pourcentage": 50, "type": "simple"},
            {"article": "ADD1", "pourcentage": 50, "type": "simple"}
        ]
    })
    db.formules.insert_one({
        "code": "PRODFIN1",
        "type": "formule",
        "optim": "1",
        "recette_code": "R003",
        "designation": "Produit Fini 1",
        "description": "Produit fini à base de premix et MPB.",
        "date_creation": now,
        "composantes": [
            {"article": "PREMIX1", "pourcentage": 70, "type": "formule", "optim": "1", "recette_code": "R001"},
            {"article": "PREMIX2", "pourcentage": 20, "type": "formule", "optim": "1", "recette_code": "R002"},
            {"article": "MPB", "pourcentage": 10, "type": "simple"}
        ]
    })

    # Ajout : pour chaque formule, ajoute optim et recette_code sur les composantes de type formule
    for formule in db.formules.find({}):
        updated = False
        for comp in formule.get("composantes", []):
            if comp.get("type") == "formule":
                if "optim" not in comp:
                    comp["optim"] = db.formules.find_one({"code": comp["article"]}).get("optim", "")
                    updated = True
                if "recette_code" not in comp:
                    comp["recette_code"] = db.formules.find_one({"code": comp["article"]}).get("recette_code", "")
                    updated = True
        if updated:
            db.formules.update_one({"_id": formule["_id"]}, {"$set": {"composantes": formule["composantes"]}})

def insert_fabrications():
    fab_premix1 = Fabrication.creer_fabrication(
        code="PREMIX1", optim="1", recette_code="R001", nb_composantes=2, quantite_a_fabriquer=20, lot="L001"
    )
    prix_total_fab_premix1 = 0
    if hasattr(fab_premix1, 'detail-fabrication'):
        for comp in fab_premix1['detail-fabrication']:
            comp['optim'] = "1"
            comp['recette_code'] = "R001"
            comp['lot'] = "L001"
            if comp['type'] == 'simple':
                # Use DEM002 for MPA if available, else DEM001
                if comp['article'] == 'MPA':
                    comp['dem'] = 'DEM002'
                    comp['prix_uni'] = 11
                    comp['quantite_stock'] = 50
                elif comp['article'] == 'MPB':
                    comp['dem'] = 'DEM004'
                    comp['prix_uni'] = 12
                    comp['quantite_stock'] = 200
                else:
                    comp['dem'] = f"DEM_{comp['article']}"
                    comp['prix_uni'] = 0
                    comp['quantite_stock'] = 0
                quantite_utilisee = comp.get('quantite_utilisee', 0) or 12
                prix_total_fab_premix1 += comp['prix_uni'] * quantite_utilisee
            elif comp['type'] == 'formule':
                comp['optim'] = "1"
                comp['recette_code'] = "R001"
                comp['lot'] = "L001"
    fab_premix1['prix_total_fabrication'] = prix_total_fab_premix1
    db.articles.update_one({"code": "MPA"}, {"$set": {"quantite": 88}})
    db.articles.update_one({"code": "MPB"}, {"$set": {"quantite": 192}})
    fab_premix2 = Fabrication.creer_fabrication(
        code="PREMIX2", optim="1", recette_code="R002", nb_composantes=2, quantite_a_fabriquer=10, lot="L002"
    )
    prix_total_fab_premix2 = 0
    if hasattr(fab_premix2, 'detail-fabrication'):
        for comp in fab_premix2['detail-fabrication']:
            comp['optim'] = "1"
            comp['recette_code'] = "R002"
            comp['lot'] = "L002"
            if comp['type'] == 'simple':
                if comp['article'] == 'MPC':
                    comp['dem'] = 'DEM006'
                    comp['prix_uni'] = 8
                    comp['quantite_stock'] = 150
                elif comp['article'] == 'ADD1':
                    comp['dem'] = 'DEM007'
                    comp['prix_uni'] = 5
                    comp['quantite_stock'] = 50
                else:
                    comp['dem'] = f"DEM_{comp['article']}"
                    comp['prix_uni'] = 0
                    comp['quantite_stock'] = 0
                quantite_utilisee = comp.get('quantite_utilisee', 0) or 5
                prix_total_fab_premix2 += comp['prix_uni'] * quantite_utilisee
            elif comp['type'] == 'formule':
                comp['optim'] = "1"
                comp['recette_code'] = "R002"
                comp['lot'] = "L002"
    fab_premix2['prix_total_fabrication'] = prix_total_fab_premix2
    db.articles.update_one({"code": "MPC"}, {"$set": {"quantite": 145}})
    db.articles.update_one({"code": "ADD1"}, {"$set": {"quantite": 45}})
    fab_prod = Fabrication.creer_fabrication(
        code="PRODFIN1", optim="1", recette_code="R003", nb_composantes=3, quantite_a_fabriquer=5, lot="L003"
    )
    prix_total_fab_prod = 0
    if hasattr(fab_prod, 'detail-fabrication'):
        for comp in fab_prod['detail-fabrication']:
            comp['optim'] = "1"
            comp['recette_code'] = "R003"
            comp['lot'] = "L003"
            if comp['type'] == 'simple':
                if comp['article'] == 'MPB':
                    comp['dem'] = 'DEM004'
                    comp['prix_uni'] = 12
                elif comp['article'] == 'MPA':
                    comp['dem'] = 'DEM003'
                    comp['prix_uni'] = 12
                else:
                    comp['dem'] = f"DEM_{comp['article']}"
                    comp['prix_uni'] = 0
                quantite_utilisee = comp.get('quantite_utilisee', 0) or 2
                prix_total_fab_prod += comp['prix_uni'] * quantite_utilisee
            elif comp['type'] == 'formule':
                comp['optim'] = "1"
                comp['recette_code'] = "R003"
                comp['lot'] = "L003"
                if comp['article'] == 'PREMIX1':
                    prix_total_fab_prod += prix_total_fab_premix1
                elif comp['article'] == 'PREMIX2':
                    prix_total_fab_prod += prix_total_fab_premix2
    fab_prod['prix_total_fabrication'] = prix_total_fab_prod

def insert_demo_data():

    
    db.fournisseurs.delete_many({})
    db.articles.delete_many({}) 
    db.commandes.delete_many({})
    db.formules.delete_many({})
    db.fabrications.delete_many({})
    #insert_formules()
    #insert_fabrications()
    
    insert_fournisseurs()
    insert_articles()
    insert_commandes()
    insert_formules()
    print("Données de démonstration insérées avec succès.")



if __name__ == "__main__":
    insert_demo_data()
    insert_demo_data()
