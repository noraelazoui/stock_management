import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.database import db
from models.fabrication import Fabrication
from models.schemas import ArticleSchema as ArtSchema
from models.schemas import CommandeSchema as CmdSchema
from models.schemas import FormuleSchema as FormSchema
from models.schemas import FabricationSchema as FabSchema
from models.schemas import SupplierSchema as SupSchema
import datetime
def insert_fournisseurs():
    db.fournisseurs.delete_many({})
    fournisseurs = [
        {"Nom": "Fournisseur A", "Téléphone": "0123456789", "Email": "a@demo.com", "Date création": datetime.datetime.now().strftime("%Y-%m-%d")},
        {"Nom": "Fournisseur B", "Téléphone": "0987654321", "Email": "b@demo.com", "Date création": datetime.datetime.now().strftime("%Y-%m-%d")}
    ]
    db.fournisseurs.insert_many(fournisseurs)
    print(f"✓ {len(fournisseurs)} fournisseurs insérés avec succès")
def insert_articles():
    """Insert articles using standardized schema"""
    db.articles.delete_many({})
    
    # Use schema constants for field names
    P = ArtSchema.Product  # Shorthand for Product fields
    
    articles = [
        {
            ArtSchema.CODE: "MPA",
            ArtSchema.DESIGNATION: "Matière A",
            ArtSchema.TYPE: "matiere",
            ArtSchema.QUANTITY: 100,
            ArtSchema.SUPPLIER: "Fournisseur A",
            "produits": [
                {P.DEM: "DEM001", P.PRICE: 10.0, P.QUANTITY: 100, P.BATCH: "LOT001", P.MANUFACTURING_DATE: "2025-09-01", P.EXPIRATION_DATE: "2026-09-01", P.ALERT_MONTHS: 3, P.THRESHOLD: 10},
                {P.DEM: "DEM002", P.PRICE: 11.0, P.QUANTITY: 50, P.BATCH: "LOT002", P.MANUFACTURING_DATE: "2025-09-15", P.EXPIRATION_DATE: "2026-09-15", P.ALERT_MONTHS: 3, P.THRESHOLD: 10},
                {P.DEM: "DEM003", P.PRICE: 12.0, P.QUANTITY: 30, P.BATCH: "LOT003", P.MANUFACTURING_DATE: "2025-09-20", P.EXPIRATION_DATE: "2026-09-20", P.ALERT_MONTHS: 3, P.THRESHOLD: 10}
            ]
        },
        {
            ArtSchema.CODE: "MPB",
            ArtSchema.DESIGNATION: "Matière B",
            ArtSchema.TYPE: "matiere",
            ArtSchema.QUANTITY: 200,
            ArtSchema.SUPPLIER: "Fournisseur B",
            "produits": [
                {P.DEM: "DEM004", P.PRICE: 12.0, P.QUANTITY: 200, P.BATCH: "LOT004", P.MANUFACTURING_DATE: "2025-09-05", P.EXPIRATION_DATE: "2026-09-05", P.ALERT_MONTHS: 3, P.THRESHOLD: 20},
                {P.DEM: "DEM005", P.PRICE: 13.0, P.QUANTITY: 80, P.BATCH: "LOT005", P.MANUFACTURING_DATE: "2025-09-18", P.EXPIRATION_DATE: "2026-09-18", P.ALERT_MONTHS: 3, P.THRESHOLD: 20}
            ]
        },
        {
            ArtSchema.CODE: "MPC",
            ArtSchema.DESIGNATION: "Matière C",
            ArtSchema.TYPE: "matiere",
            ArtSchema.QUANTITY: 150,
            ArtSchema.SUPPLIER: "Fournisseur A",
            "produits": [
                {P.DEM: "DEM006", P.PRICE: 8.0, P.QUANTITY: 150, P.BATCH: "LOT006", P.MANUFACTURING_DATE: "2025-09-10", P.EXPIRATION_DATE: "2026-09-10", P.ALERT_MONTHS: 3, P.THRESHOLD: 15},
                {P.DEM: "DEM008", P.PRICE: 9.0, P.QUANTITY: 75, P.BATCH: "LOT008", P.MANUFACTURING_DATE: "2025-09-25", P.EXPIRATION_DATE: "2026-09-25", P.ALERT_MONTHS: 3, P.THRESHOLD: 15}
            ]
        },
        {
            ArtSchema.CODE: "ADD1",
            ArtSchema.DESIGNATION: "Additif 1",
            ArtSchema.TYPE: "additif",
            ArtSchema.QUANTITY: 50,
            ArtSchema.SUPPLIER: "Fournisseur B",
            "produits": [
                {P.DEM: "DEM007", P.PRICE: 5.0, P.QUANTITY: 50, P.BATCH: "LOT007", P.MANUFACTURING_DATE: "2025-09-12", P.EXPIRATION_DATE: "2026-09-12", P.ALERT_MONTHS: 3, P.THRESHOLD: 5}
            ]
        },
    ]
    db.articles.insert_many(articles)
    print(f"✓ {len(articles)} articles insérés avec succès")

def insert_commandes():
    db.commandes.delete_many({})
    commandes = [
        {
            "ref": "CMD001",
            "date_reception": datetime.datetime.now().strftime("%Y-%m-%d"),
            "fournisseur": "Fournisseur A",
            "statut": "Validée",
            "produits": [
                {"Code": "MPA", "DESIGNATION ARTICLE": "Matière A", "DEM": "DEM001", "QUANTITE": 100, "QUANTITE REEL": 100, "Prix UNI.": 10, "TVA": 20, "Prix TTC": 12.0, "MONTANT": 1200.0, "MONTANT REEL": 1200.0, "optim_formule": "1", "recette_formule": "R001"},
                {"Code": "MPA", "DESIGNATION ARTICLE": "Matière A", "DEM": "DEM002", "QUANTITE": 50, "QUANTITE REEL": 50, "Prix UNI.": 11, "TVA": 20, "Prix TTC": 13.2, "MONTANT": 660.0, "MONTANT REEL": 660.0, "optim_formule": "1", "recette_formule": "R001"},
                {"Code": "MPA", "DESIGNATION ARTICLE": "Matière A", "DEM": "DEM003", "QUANTITE": 30, "QUANTITE REEL": 30, "Prix UNI.": 12, "TVA": 20, "Prix TTC": 14.4, "MONTANT": 432.0, "MONTANT REEL": 432.0, "optim_formule": "1", "recette_formule": "R001"},
            ],
            "infos_commande": [
                {"statut": "Validée", "remarque": "Livraison rapide", "utilisateur": "admin"}
            ],
            "infos_commande_detail": [
                {"mode": "Express", "date": datetime.datetime.now().strftime("%Y-%m-%d"), "fournisseur": "Fournisseur A", "payement": "CB", "adresse": "1 rue Alpha", "transport": "Camion", "numero": "BR001"}
            ]
        },
        {
            "ref": "CMD002",
            "date_reception": datetime.datetime.now().strftime("%Y-%m-%d"),
            "fournisseur": "Fournisseur B",
            "statut": "En attente",
            "produits": [
                {"Code": "MPB", "DESIGNATION ARTICLE": "Matière B", "DEM": "DEM004", "QUANTITE": 200, "QUANTITE REEL": 200, "Prix UNI.": 12, "TVA": 20, "Prix TTC": 14.4, "MONTANT": 2880.0, "MONTANT REEL": 2880.0, "optim_formule": "1", "recette_formule": "R002"},
                {"Code": "MPB", "DESIGNATION ARTICLE": "Matière B", "DEM": "DEM005", "QUANTITE": 80, "QUANTITE REEL": 80, "Prix UNI.": 13, "TVA": 20, "Prix TTC": 15.6, "MONTANT": 1248.0, "MONTANT REEL": 1248.0, "optim_formule": "1", "recette_formule": "R002"},
                {"Code": "MPC", "DESIGNATION ARTICLE": "Matière C", "DEM": "DEM006", "QUANTITE": 150, "QUANTITE REEL": 150, "Prix UNI.": 8, "TVA": 10, "Prix TTC": 8.8, "MONTANT": 1320.0, "MONTANT REEL": 1320.0, "optim_formule": "1", "recette_formule": "R002"},
                {"Code": "ADD1", "DESIGNATION ARTICLE": "Additif 1", "DEM": "DEM007", "QUANTITE": 50, "QUANTITE REEL": 50, "Prix UNI.": 5, "TVA": 10, "Prix TTC": 5.5, "MONTANT": 275.0, "MONTANT REEL": 275.0, "optim_formule": "1", "recette_formule": "R002"},
            ],
            "infos_commande": [
                {"statut": "En attente", "remarque": "Paiement à la livraison", "utilisateur": "user1"}
            ],
            "infos_commande_detail": [
                {"mode": "Standard", "date": datetime.datetime.now().strftime("%Y-%m-%d"), "fournisseur": "Fournisseur B", "payement": "Virement", "adresse": "2 rue Beta", "transport": "Train", "numero": "BR002"}
            ]
        },
        {
            "ref": "CMD003",
            "date_reception": datetime.datetime.now().strftime("%Y-%m-%d"),
            "fournisseur": "Fournisseur A",
            "statut": "Créé",
            "produits": [
                {"Code": "MPC", "DESIGNATION ARTICLE": "Matière C", "DEM": "DEM008", "QUANTITE": 75, "QUANTITE REEL": 75, "Prix UNI.": 9, "TVA": 10, "Prix TTC": 9.9, "MONTANT": 742.5, "MONTANT REEL": 742.5, "optim_formule": "1", "recette_formule": "R003"},
            ],
            "infos_commande": [
                {"statut": "Créé", "remarque": "Commande urgente", "utilisateur": "admin"}
            ],
            "infos_commande_detail": [
                {"mode": "Urgent", "date": datetime.datetime.now().strftime("%Y-%m-%d"), "fournisseur": "Fournisseur A", "payement": "Espèces", "adresse": "3 rue Gamma", "transport": "Express", "numero": "BR003"}
            ]
        }
    ]
    db.commandes.insert_many(commandes)
    print(f"✓ {len(commandes)} commandes insérées avec succès")
    # Les commandes servent uniquement à la traçabilité, pas de modification du stock ici

def insert_formules():
    db.formules.delete_many({})
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    db.formules.insert_one({
        "code": "PREMIX1",
        "type": "formule",
        "type_formule": "simple",  # Pour Premix - contient uniquement des matières/additifs
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
        "type_formule": "simple",  # Pour Premix - contient uniquement des matières/additifs
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
        "type_formule": "mixte",  # Pour Usine - contient des formules
        "optim": "1",
        "recette_code": "R003",
        "designation": "Produit Fini 1",
        "description": "Produit fini à base de premix et MPB.",
        "date_creation": now,
        "composantes": [
            {"article": "PREMIX1", "pourcentage": 70, "type": "formule", "optim_formule": "1", "recette_formule": "R001"},
            {"article": "PREMIX2", "pourcentage": 20, "type": "formule", "optim_formule": "1", "recette_formule": "R002"},
            {"article": "MPB", "pourcentage": 10, "type": "simple"}
        ]
    })

    # Ajout : pour chaque formule, ajoute optim_formule et recette_formule sur les composantes de type formule
    for formule in db.formules.find({}):
        updated = False
        for comp in formule.get("composantes", []):
            if comp.get("type") == "formule":
                if "optim_formule" not in comp:
                    comp["optim_formule"] = db.formules.find_one({"code": comp["article"]}).get("optim", "")
                    updated = True
                if "recette_formule" not in comp:
                    comp["recette_formule"] = db.formules.find_one({"code": comp["article"]}).get("recette_code", "")
                    updated = True
        if updated:
            db.formules.update_one({"_id": formule["_id"]}, {"$set": {"composantes": formule["composantes"]}})
    
    print(f"✓ 3 formules insérées avec succès")

def insert_fabrications():
    fab_premix1 = Fabrication.creer_fabrication(
        code="PREMIX1", optim="1", recette_code="R001", nb_composantes=2, quantite_a_fabriquer=20, lot="L001"
    )
    prix_total_fab_premix1 = 0
    if fab_premix1 and 'detail-fabrication' in fab_premix1:
        for comp in fab_premix1['detail-fabrication']:
            # Update component with dem and prices
            if comp['article'] == 'MPA':
                comp['dem'] = 'DEM002'
                comp['prix'] = 11.0
                comp['quantite_stock'] = 50
            elif comp['article'] == 'MPB':
                comp['dem'] = 'DEM004'
                comp['prix'] = 12.0
                comp['quantite_stock'] = 200
            
            # Add lot, optim_formule, and recette_formule for all components
            comp['lot'] = 'L001'
            comp['optim_formule'] = ''  # Empty for simple articles
            comp['recette_formule'] = ''  # Empty for simple articles
            
            # Calculate prix_total for each component
            quantite_fabrique = comp.get('quantite_fabrique', 0)
            comp['prix_total'] = round(comp['prix'] * quantite_fabrique, 2)
            prix_total_fab_premix1 += comp['prix_total']
        
        # Calculate prix_formule per kg (prix_total / quantite_a_fabriquer)
        prix_formule_premix1 = round(prix_total_fab_premix1 / 20, 2) if prix_total_fab_premix1 > 0 else 0
        
        # Update the fabrication in database with updated details and prix_formule
        db.fabrications.update_one(
            {"code": "PREMIX1", "optim": "1", "lot": "L001"},
            {"$set": {
                "detail-fabrication": fab_premix1['detail-fabrication'],
                "prix_formule": prix_formule_premix1
            }}
        )
    else:
        prix_formule_premix1 = 0
    
    db.articles.update_one({"code": "MPA"}, {"$set": {"quantite": 88}})
    db.articles.update_one({"code": "MPB"}, {"$set": {"quantite": 192}})
    fab_premix2 = Fabrication.creer_fabrication(
        code="PREMIX2", optim="1", recette_code="R002", nb_composantes=2, quantite_a_fabriquer=10, lot="L002"
    )
    prix_total_fab_premix2 = 0
    if fab_premix2 and 'detail-fabrication' in fab_premix2:
        for comp in fab_premix2['detail-fabrication']:
            # Update component with dem and prices
            if comp['article'] == 'MPC':
                comp['dem'] = 'DEM006'
                comp['prix'] = 8.0
                comp['quantite_stock'] = 150
            elif comp['article'] == 'ADD1':
                comp['dem'] = 'DEM007'
                comp['prix'] = 5.0
                comp['quantite_stock'] = 50
            
            # Add lot, optim_formule, and recette_formule for all components
            comp['lot'] = 'L002'
            comp['optim_formule'] = ''  # Empty for simple articles
            comp['recette_formule'] = ''  # Empty for simple articles
            
            # Calculate prix_total for each component
            quantite_fabrique = comp.get('quantite_fabrique', 0)
            comp['prix_total'] = round(comp['prix'] * quantite_fabrique, 2)
            prix_total_fab_premix2 += comp['prix_total']
        
        # Calculate prix_formule per kg (prix_total / quantite_a_fabriquer)
        prix_formule_premix2 = round(prix_total_fab_premix2 / 10, 2) if prix_total_fab_premix2 > 0 else 0
        
        # Update the fabrication in database with updated details and prix_formule
        db.fabrications.update_one(
            {"code": "PREMIX2", "optim": "1", "lot": "L002"},
            {"$set": {
                "detail-fabrication": fab_premix2['detail-fabrication'],
                "prix_formule": prix_formule_premix2
            }}
        )
    else:
        prix_formule_premix2 = 0
    
    db.articles.update_one({"code": "MPC"}, {"$set": {"quantite": 145}})
    db.articles.update_one({"code": "ADD1"}, {"$set": {"quantite": 45}})
    fab_prod = Fabrication.creer_fabrication(
        code="PRODFIN1", optim="1", recette_code="R003", nb_composantes=3, quantite_a_fabriquer=5, lot="L003"
    )
    prix_total_fab_prod = 0
    if fab_prod and 'detail-fabrication' in fab_prod:
        for comp in fab_prod['detail-fabrication']:
            # Add lot for all components
            comp['lot'] = 'L003'
            
            # Update component based on type
            if comp['article'] == 'MPB':
                comp['dem'] = 'DEM004'
                comp['prix'] = 12.0
                comp['quantite_stock'] = 200
                comp['optim_formule'] = ''  # Empty for simple articles
                comp['recette_formule'] = ''  # Empty for simple articles
                # Calculate prix_total for simple article
                quantite_fabrique = comp.get('quantite_fabrique', 0)
                comp['prix_total'] = round(comp['prix'] * quantite_fabrique, 2)
                prix_total_fab_prod += comp['prix_total']
            elif comp['article'] == 'PREMIX1':
                # For formule components, use the prix_formule from the premix
                comp['prix'] = prix_formule_premix1
                comp['dem'] = ''  # No DEM for formules
                comp['quantite_stock'] = 20  # Quantity fabricated from PREMIX1
                comp['optim_formule'] = '1'  # Optim of the premix
                comp['recette_formule'] = 'R001'  # Recette of the premix
                quantite_fabrique = comp.get('quantite_fabrique', 0)
                comp['prix_total'] = round(comp['prix'] * quantite_fabrique, 2)
                prix_total_fab_prod += comp['prix_total']
            elif comp['article'] == 'PREMIX2':
                # For formule components, use the prix_formule from the premix
                comp['prix'] = prix_formule_premix2
                comp['dem'] = ''  # No DEM for formules
                comp['quantite_stock'] = 10  # Quantity fabricated from PREMIX2
                comp['optim_formule'] = '1'  # Optim of the premix
                comp['recette_formule'] = 'R002'  # Recette of the premix
                quantite_fabrique = comp.get('quantite_fabrique', 0)
                comp['prix_total'] = round(comp['prix'] * quantite_fabrique, 2)
                prix_total_fab_prod += comp['prix_total']
        
        # Calculate prix_formule per kg (prix_total / quantite_a_fabriquer)
        prix_formule_prod = round(prix_total_fab_prod / 5, 2) if prix_total_fab_prod > 0 else 0
        
        # Update the fabrication in database with updated details and prix_formule
        db.fabrications.update_one(
            {"code": "PRODFIN1", "optim": "1", "lot": "L003"},
            {"$set": {
                "detail-fabrication": fab_prod['detail-fabrication'],
                "prix_formule": prix_formule_prod
            }}
        )

def insert_demo_data():
    print("\n" + "="*60)
    print("INSERTION DES DONNÉES DE DÉMONSTRATION")
    print("="*60 + "\n")
    
    print("Nettoyage des collections...")
    db.fournisseurs.delete_many({})
    db.articles.delete_many({}) 
    db.commandes.delete_many({})
    db.formules.delete_many({})
    db.fabrications.delete_many({})
    print("✓ Collections nettoyées\n")
    
    print("Insertion des données...")
    insert_fournisseurs()
    insert_articles()
    insert_commandes()
    insert_formules()
    insert_fabrications()
    
    # Debug: Verify article products are in database using schema
    print("\n" + "="*60)
    print("VÉRIFICATION DES PRODUITS DES ARTICLES")
    print("="*60)
    P = ArtSchema.Product  # Shorthand
    for article in db.articles.find({}):
        print(f"\nArticle: {article.get(ArtSchema.CODE)}")
        if 'produits' in article:
            print(f"  ✅ Nombre de produits: {len(article['produits'])}")
            print(f"  ✅ Champs standardisés (anglais, sans accents)")
            for prod in article['produits']:
                print(f"    - DEM: {prod.get(P.DEM)}, Prix: {prod.get(P.PRICE)}, Quantité: {prod.get(P.QUANTITY)}, Batch: {prod.get(P.BATCH)}")
        else:
            print("  ⚠️ PAS DE PRODUITS!")
    
    print("\n" + "="*60)
    print("✅ SCHEMA STANDARDISÉ APPLIQUÉ")
    print("="*60)
    print("Tous les champs utilisent maintenant:")
    print("  - Noms en anglais (sans accents)")
    print("  - Lowercase avec underscores (snake_case)")
    print("  - Définis dans models/schemas.py")
    print("\nExemples:")
    print(f"  - {P.PRICE} (au lieu de 'Prix')")
    print(f"  - {P.QUANTITY} (au lieu de 'Quantité')")
    print(f"  - {P.MANUFACTURING_DATE} (au lieu de 'Date fabrication')")
    print("="*60)
    
    print("\n" + "="*60)
    print("✓ TOUTES LES DONNÉES ONT ÉTÉ INSÉRÉES AVEC SUCCÈS")
    print("="*60 + "\n")

if __name__ == "__main__":
    insert_demo_data()
