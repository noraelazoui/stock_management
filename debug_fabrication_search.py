from models.database import db
import tkinter as tk
from tkinter import ttk
import traceback

def debug_valider_prix_formule(code, optim):
    """Simulation de la méthode valider_prix_formule pour déboguer"""
    try:
        print(f"\n=== SIMULATION DE VALIDATION PRIX FORMULE ===")
        print(f"Recherche de fabrication avec code='{code}', optim='{optim}'")
        
        # Essayer la recherche exacte
        fabrication = db.fabrications.find_one({"code": code, "optim": optim})
        if fabrication:
            print(f"Fabrication trouvée avec la recherche exacte")
            print(f"ID: {fabrication.get('_id')}")
            print(f"Prix formule: {fabrication.get('prix_formule')}")
            return
            
        print(f"Aucune fabrication trouvée avec la recherche exacte")
        
        # Essayer avec optim comme entier si c'est une chaîne numérique
        if isinstance(optim, str) and optim.isdigit():
            optim_int = int(optim)
            print(f"Essai avec optim comme entier: {optim_int}")
            fabrication = db.fabrications.find_one({"code": code, "optim": optim_int})
            if fabrication:
                print(f"Fabrication trouvée avec optim comme entier")
                print(f"ID: {fabrication.get('_id')}")
                print(f"Prix formule: {fabrication.get('prix_formule')}")
                return
                
        # Essayer avec optim comme chaîne si c'est un nombre
        if isinstance(optim, (int, float)):
            optim_str = str(optim)
            print(f"Essai avec optim comme chaîne: {optim_str}")
            fabrication = db.fabrications.find_one({"code": code, "optim": optim_str})
            if fabrication:
                print(f"Fabrication trouvée avec optim comme chaîne")
                print(f"ID: {fabrication.get('_id')}")
                print(f"Prix formule: {fabrication.get('prix_formule')}")
                return
                
        # Vérifier combien de fabrications existent avec ce code
        fabrications = list(db.fabrications.find({"code": code}))
        print(f"\nNombre total de fabrications avec code='{code}': {len(fabrications)}")
        
        if fabrications:
            print("\nListe des optimisations disponibles:")
            for i, fab in enumerate(fabrications):
                opt = fab.get("optim")
                print(f"  {i+1}. optim='{opt}' (type: {type(opt).__name__})")
                
        # Vérifier si la chaîne combinée existe
        combined = f"{code}-{optim}"
        print(f"\nRecherche avec code combiné: '{combined}'")
        fabrication = db.fabrications.find_one({"code": combined})
        if fabrication:
            print(f"Fabrication trouvée avec code combiné")
            print(f"ID: {fabrication.get('_id')}")
            print(f"Prix formule: {fabrication.get('prix_formule')}")
            return
            
        print(f"Aucune fabrication trouvée avec code combiné")
        
        print("\n=== FABRICATION NON TROUVÉE ===")
        
    except Exception as e:
        print(f"Erreur pendant le débogage: {e}")
        traceback.print_exc()

# Paramètres à tester
code = "mama"
optim = "1"

# Exécuter le débogage
debug_valider_prix_formule(code, optim)

# Tester avec l'ID d'une fabrication existante
print("\n\n=== TEST AVEC UN ID SPÉCIFIQUE ===")
# Trouver une fabrication existante
fabrications = list(db.fabrications.find({"code": code}))
if fabrications:
    # Prendre la première fabrication
    fabrication = fabrications[0]
    fab_id = fabrication.get("_id")
    fab_code = fabrication.get("code")
    fab_optim = fabrication.get("optim")
    
    print(f"Fabrication trouvée avec ID {fab_id}")
    print(f"Code: {fab_code}, Optim: {fab_optim}")
    
    # Tester la recherche avec ces valeurs
    print(f"\nTest de recherche avec ces valeurs exactes:")
    debug_valider_prix_formule(fab_code, fab_optim)
else:
    print("Aucune fabrication trouvée dans la base de données")
