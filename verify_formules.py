from models.database import db
from models.formule import Formule

def verify_formule_types():
    print("\n=== Vérification des types de formules dans MongoDB ===")
    
    # Récupérer toutes les formules
    formules = list(db.formules.find({}))
    
    print(f"\nNombre total de formules: {len(formules)}")
    
    for f in formules:
        print(f"\nFormule: {f.get('code')} (Type: {f.get('type_formule')})")
        print("Composantes:")
        for comp in f.get('composantes', []):
            has_formule = comp.get('optim_formule') is not None or comp.get('recette_formule') is not None
            comp_type = "Formule" if has_formule else "Article"
            print(f"  - Type: {comp_type}")
            if has_formule:
                print(f"    Optim: {comp.get('optim_formule')}")
                print(f"    Recette: {comp.get('recette_formule')}")
            else:
                print(f"    Article: {comp.get('article')}")

        # Vérifier si le type est correct
        should_be_mixte = any(
            comp.get('optim_formule') is not None or comp.get('recette_formule') is not None
            for comp in f.get('composantes', [])
        )
        correct_type = "mixte" if should_be_mixte else "simple"
        current_type = f.get('type_formule')
        
        if current_type != correct_type:
            print(f"ERREUR: Le type devrait être {correct_type}, mais est {current_type}")
            
            # Corriger le type
            print("Correction du type...")
            db.formules.update_one(
                {"_id": f["_id"]},
                {"$set": {"type_formule": correct_type}}
            )
            print(f"Type corrigé à {correct_type}")

if __name__ == "__main__":
    verify_formule_types()
