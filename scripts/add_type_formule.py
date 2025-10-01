"""
Script pour ajouter le champ 'type_formule' aux formules existantes dans MongoDB
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db

def add_type_formule_to_formules():
    """
    Ajoute le champ 'type_formule' à toutes les formules en fonction de leurs composantes:
    - 'simple' (Premix): si toutes les composantes sont de type 'matiere' ou 'additif'
    - 'mixte' (Usine): si au moins une composante est de type 'formule'
    """
    print("=== Début de la mise à jour des formules ===\n")
    
    formules = list(db.formules.find())
    print(f"Nombre de formules trouvées: {len(formules)}\n")
    
    for formule in formules:
        code = formule.get('code')
        designation = formule.get('designation', '')
        composantes = formule.get('composantes', [])
        
        # Vérifier si une composante est de type 'formule'
        has_formule_composante = any(c.get('type') == 'formule' for c in composantes)
        
        if has_formule_composante:
            type_formule = 'mixte'  # Usine
            print(f"✓ Formule '{code}' ({designation})")
            print(f"  → Type: MIXTE (Usine) - contient des formules")
        else:
            type_formule = 'simple'  # Premix
            print(f"✓ Formule '{code}' ({designation})")
            print(f"  → Type: SIMPLE (Premix) - contient uniquement des matières/additifs")
        
        # Mettre à jour la formule avec le nouveau champ
        result = db.formules.update_one(
            {"_id": formule["_id"]},
            {"$set": {"type_formule": type_formule}}
        )
        
        if result.modified_count > 0:
            print(f"  ✓ Mise à jour réussie\n")
        else:
            print(f"  ⚠ Aucune modification (peut-être déjà à jour)\n")
    
    print("=== Fin de la mise à jour ===\n")
    
    # Vérification
    print("=== Vérification des formules mises à jour ===\n")
    formules_updated = list(db.formules.find())
    for f in formules_updated:
        print(f"Code: {f.get('code')}")
        print(f"  Désignation: {f.get('designation')}")
        print(f"  Type formule: {f.get('type_formule')}")
        print()

if __name__ == "__main__":
    add_type_formule_to_formules()
