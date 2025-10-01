import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from models.database import db
from models.fabrication import Fabrication

def insert_fabrications():
    """Insert fabrications only - assumes articles, formules already exist"""
    print("\n" + "="*60)
    print("TEST: INSERTION DES FABRICATIONS UNIQUEMENT")
    print("="*60 + "\n")
    
    # Clean only fabrications
    print("Nettoyage de la collection fabrications...")
    db.fabrications.delete_many({})
    print("✓ Collection fabrications nettoyée\n")
    
    print("Insertion des fabrications...\n")
    
    # Fabrication PREMIX1
    print("1. Création de la fabrication PREMIX1...")
    fab_premix1 = Fabrication.creer_fabrication(
        code="PREMIX1", optim="1", recette_code="R001", nb_composantes=2, quantite_a_fabriquer=20, lot="L001"
    )
    
    prix_total_fab_premix1 = fab_premix1.get('prix_formule', 0) if fab_premix1 else 0
    if fab_premix1 and 'detail-fabrication' in fab_premix1:
        # Update detail-fabrication with DEM codes and prices from commandes
        for comp in fab_premix1['detail-fabrication']:
            article_code = comp.get('article', '')
            if article_code == 'MPA':
                comp['dem'] = 'DEM002'
                comp['prix'] = 11
                comp['prix_total'] = round(comp['prix'] * comp['quantite_fabrique'], 2)
            elif article_code == 'MPB':
                comp['dem'] = 'DEM004'
                comp['prix'] = 12
                comp['prix_total'] = round(comp['prix'] * comp['quantite_fabrique'], 2)
        
        # Recalculate prix_formule based on updated prix_total
        total_prix = sum(comp.get('prix_total', 0) for comp in fab_premix1['detail-fabrication'])
        fab_premix1['prix_formule'] = round(total_prix / fab_premix1['quantite_a_fabriquer'], 4)
        prix_total_fab_premix1 = fab_premix1['prix_formule']
        
        # Update fabrication in database
        db.fabrications.update_one(
            {"_id": fab_premix1['_id']},
            {"$set": {
                "detail-fabrication": fab_premix1['detail-fabrication'],
                "prix_formule": fab_premix1['prix_formule']
            }}
        )
        
        print(f"   ✓ PREMIX1 créé - Prix formule: {prix_total_fab_premix1}")
        print(f"   Nombre de composantes: {len(fab_premix1['detail-fabrication'])}")
        print(f"   DEM codes ajoutés pour les composantes simples")
    
    
    # Fabrication PREMIX2
    print("\n2. Création de la fabrication PREMIX2...")
    fab_premix2 = Fabrication.creer_fabrication(
        code="PREMIX2", optim="1", recette_code="R002", nb_composantes=2, quantite_a_fabriquer=10, lot="L002"
    )
    
    prix_total_fab_premix2 = fab_premix2.get('prix_formule', 0) if fab_premix2 else 0
    if fab_premix2 and 'detail-fabrication' in fab_premix2:
        # Update detail-fabrication with DEM codes and prices from commandes
        for comp in fab_premix2['detail-fabrication']:
            article_code = comp.get('article', '')
            if article_code == 'MPC':
                comp['dem'] = 'DEM006'
                comp['prix'] = 8
                comp['prix_total'] = round(comp['prix'] * comp['quantite_fabrique'], 2)
            elif article_code == 'ADD1':
                comp['dem'] = 'DEM007'
                comp['prix'] = 5
                comp['prix_total'] = round(comp['prix'] * comp['quantite_fabrique'], 2)
        
        # Recalculate prix_formule
        total_prix = sum(comp.get('prix_total', 0) for comp in fab_premix2['detail-fabrication'])
        fab_premix2['prix_formule'] = round(total_prix / fab_premix2['quantite_a_fabriquer'], 4)
        
        # Update fabrication in database
        db.fabrications.update_one(
            {"_id": fab_premix2['_id']},
            {"$set": {
                "detail-fabrication": fab_premix2['detail-fabrication'],
                "prix_formule": fab_premix2['prix_formule']
            }}
        )
        
        print(f"   ✓ PREMIX2 créé - Prix formule: {fab_premix2['prix_formule']}")
        print(f"   Nombre de composantes: {len(fab_premix2['detail-fabrication'])}")
        print(f"   DEM codes ajoutés pour les composantes simples")
    
    # Fabrication PRODFIN1 (formule mixte with premixes and simple articles)
    print("\n3. Création de la fabrication PRODFIN1 (formule mixte)...")
    fab_prod = Fabrication.creer_fabrication(
        code="PRODFIN1", optim="1", recette_code="R003", nb_composantes=3, quantite_a_fabriquer=5, lot="L003"
    )
    
    prix_total_fab_prod = fab_prod.get('prix_formule', 0) if fab_prod else 0
    if fab_prod and 'detail-fabrication' in fab_prod:
        # Update detail-fabrication with proper fields
        for comp in fab_prod['detail-fabrication']:
            article_code = comp.get('article', '')
            
            # For formule components (premixes), add recette_formule and lot
            if article_code == 'PREMIX1':
                comp['recette_formule'] = 'R001'
                comp['lot'] = 'L001'
                comp['optim'] = '1'
                # Recalculate prix based on actual prix_formule
                comp['prix'] = fab_premix1['prix_formule']
                comp['prix_total'] = round(comp['prix'] * comp['quantite_fabrique'], 2)
            elif article_code == 'PREMIX2':
                comp['recette_formule'] = 'R002'
                comp['lot'] = 'L002'
                comp['optim'] = '1'
                # Recalculate prix based on actual prix_formule
                comp['prix'] = fab_premix2['prix_formule']
                comp['prix_total'] = round(comp['prix'] * comp['quantite_fabrique'], 2)
            # For simple article components, add DEM
            elif article_code == 'MPB':
                comp['dem'] = 'DEM004'
                comp['prix'] = 12
                comp['prix_total'] = round(comp['prix'] * comp['quantite_fabrique'], 2)
        
        # Recalculate prix_formule
        total_prix = sum(comp.get('prix_total', 0) for comp in fab_prod['detail-fabrication'])
        fab_prod['prix_formule'] = round(total_prix / fab_prod['quantite_a_fabriquer'], 4)
        
        # Update fabrication in database
        db.fabrications.update_one(
            {"_id": fab_prod['_id']},
            {"$set": {
                "detail-fabrication": fab_prod['detail-fabrication'],
                "prix_formule": fab_prod['prix_formule']
            }}
        )
        
        print(f"   ✓ PRODFIN1 créé - Prix formule: {fab_prod['prix_formule']}")
        print(f"   Nombre de composantes: {len(fab_prod['detail-fabrication'])}")
        print(f"   DEM codes ajoutés pour composantes simples")
        print(f"   recette_formule et lot ajoutés pour composantes formules (premixes)")
    
    print("\n" + "="*60)
    print("VÉRIFICATION DES FABRICATIONS DANS LA BASE DE DONNÉES")
    print("="*60 + "\n")
    
    # Verify fabrications in database
    fabrications_count = db.fabrications.count_documents({})
    print(f"Nombre total de fabrications: {fabrications_count}")
    
    if fabrications_count > 0:
        print("\nDétails des fabrications:")
        for fab in db.fabrications.find({}):
            print(f"\n{'='*50}")
            print(f"  Code: {fab.get('code', 'N/A')}")
            print(f"  Lot: {fab.get('lot', 'N/A')}")
            print(f"  Optim: {fab.get('optim', 'N/A')}")
            print(f"  Recette: {fab.get('recette_code', 'N/A')}")
            print(f"  Quantité à fabriquer: {fab.get('quantite_a_fabriquer', 'N/A')}")
            print(f"  Prix formule: {fab.get('prix_formule', 'N/A')}")
            print(f"  Nombre de composantes: {len(fab.get('detail-fabrication', []))}")
            print(f"\n  Composantes:")
            for i, comp in enumerate(fab.get('detail-fabrication', []), 1):
                print(f"    {i}. Article: {comp.get('article', 'N/A')}")
                print(f"       - DEM: {comp.get('dem', 'N/A')}")
                print(f"       - Prix: {comp.get('prix', 'N/A')}")
                print(f"       - Quantité fabriquée: {comp.get('quantite_fabrique', 'N/A')}")
                print(f"       - Prix total: {comp.get('prix_total', 'N/A')}")
                if 'recette_formule' in comp:
                    print(f"       - Recette formule: {comp.get('recette_formule', 'N/A')}")
                if 'lot' in comp and comp.get('lot'):
                    print(f"       - Lot: {comp.get('lot', 'N/A')}")
                if 'optim' in comp:
                    print(f"       - Optim: {comp.get('optim', 'N/A')}")
    else:
        print("\n⚠️  AUCUNE FABRICATION TROUVÉE DANS LA BASE!")
    
    print("\n" + "="*60)
    print("✓ TEST TERMINÉ")
    print("="*60 + "\n")
    print("Maintenant, ouvrez l'application et vérifiez l'onglet Fabrication.")
    print("Les fabrications devraient apparaître dans fabrication_view.py\n")

if __name__ == "__main__":
    insert_fabrications()
