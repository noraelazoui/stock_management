from models.database import db

# Rechercher avec différents formats d'optim
fab_string = list(db.fabrications.find({"code": "mama", "optim": "1"}))
fab_int = list(db.fabrications.find({"code": "mama", "optim": 1}))

print(f"Fabrications avec optim='1' (chaîne): {len(fab_string)}")
print(f"Fabrications avec optim=1 (entier): {len(fab_int)}")

# Afficher quelques détails sur ces fabrications
if fab_string:
    print("\nExemples de fabrications avec optim='1':")
    for i, fab in enumerate(fab_string[:3]):  # Limiter à 3 pour la lisibilité
        print(f"Fabrication {i+1}:")
        print(f"  ID: {fab.get('_id')}")
        print(f"  Code: {fab.get('code')} (type: {type(fab.get('code')).__name__})")
        print(f"  Optim: {fab.get('optim')} (type: {type(fab.get('optim')).__name__})")
        print(f"  Prix formule: {fab.get('prix_formule')} (type: {type(fab.get('prix_formule')).__name__})")

# Vérifier aussi avec un format "mama-1"
combined_search = list(db.fabrications.find({"code": "mama-1"}))
print(f"\nFabrications avec code='mama-1': {len(combined_search)}")

# Rechercher avec la clé "_id" si disponible
if fab_string:
    first_id = fab_string[0].get("_id")
    by_id = db.fabrications.find_one({"_id": first_id})
    print(f"\nRecherche par ID {first_id}: {'Trouvé' if by_id else 'Non trouvé'}")
