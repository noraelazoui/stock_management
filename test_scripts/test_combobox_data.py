"""
Script de test pour vérifier que les formules sont correctement récupérées
pour les combobox Premix et Usine
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from models.database import db

print("=" * 70)
print("TEST DE RÉCUPÉRATION DES FORMULES POUR LES COMBOBOX")
print("=" * 70)

# Test 1: Vérifier les formules de type "simple" (Premix)
print("\n1. Test Radio Button 'Premix' (type_formule: 'simple')")
print("-" * 70)
formules_premix = list(db.formules.find({"type_formule": "simple"}))
codes_premix = [f.get('code') for f in formules_premix if f.get('code')]
print(f"Nombre de formules trouvées: {len(formules_premix)}")
print(f"Codes pour le combobox: {codes_premix}")
for f in formules_premix:
    print(f"  - {f.get('code')}: {f.get('designation')}")
    composantes = f.get('composantes', [])
    print(f"    Composantes: {[(c.get('article'), c.get('type')) for c in composantes]}")

# Test 2: Vérifier les formules de type "mixte" (Usine)
print("\n2. Test Radio Button 'Usine' (type_formule: 'mixte')")
print("-" * 70)
formules_usine = list(db.formules.find({"type_formule": "mixte"}))
codes_usine = [f.get('code') for f in formules_usine if f.get('code')]
print(f"Nombre de formules trouvées: {len(formules_usine)}")
print(f"Codes pour le combobox: {codes_usine}")
for f in formules_usine:
    print(f"  - {f.get('code')}: {f.get('designation')}")
    composantes = f.get('composantes', [])
    print(f"    Composantes: {[(c.get('article'), c.get('type')) for c in composantes]}")

# Test 3: Simuler la sélection d'un code et récupération des optims
print("\n3. Test Sélection d'un Code (PREMIX1)")
print("-" * 70)
selected_code = "PREMIX1"
formule_type = "simple"
selected_formule = db.formules.find_one({
    "code": selected_code,
    "type_formule": formule_type
})
print(f"Code sélectionné: {selected_code}")
print(f"Type de formule recherché: {formule_type}")
print(f"Formule trouvée: {'OUI' if selected_formule else 'NON'}")

if selected_formule:
    print(f"  Désignation: {selected_formule.get('designation')}")
    print(f"  Recette: {selected_formule.get('recette_code')}")
    print(f"  Optim: {selected_formule.get('optim')}")
    
    # Récupérer toutes les optimisations pour ce code
    formules_meme_code = list(db.formules.find({"code": selected_code}))
    optimisations = [str(f.get('optim', '')) for f in formules_meme_code if f.get('optim')]
    print(f"  Optimisations disponibles: {optimisations}")

# Test 4: Simuler la sélection d'un code Usine
print("\n4. Test Sélection d'un Code (PRODFIN1)")
print("-" * 70)
selected_code = "PRODFIN1"
formule_type = "mixte"
selected_formule = db.formules.find_one({
    "code": selected_code,
    "type_formule": formule_type
})
print(f"Code sélectionné: {selected_code}")
print(f"Type de formule recherché: {formule_type}")
print(f"Formule trouvée: {'OUI' if selected_formule else 'NON'}")

if selected_formule:
    print(f"  Désignation: {selected_formule.get('designation')}")
    print(f"  Recette: {selected_formule.get('recette_code')}")
    print(f"  Optim: {selected_formule.get('optim')}")
    
    # Récupérer toutes les optimisations pour ce code
    formules_meme_code = list(db.formules.find({"code": selected_code}))
    optimisations = [str(f.get('optim', '')) for f in formules_meme_code if f.get('optim')]
    print(f"  Optimisations disponibles: {optimisations}")

print("\n" + "=" * 70)
print("RÉSUMÉ DES TESTS")
print("=" * 70)
print(f"✓ Premix (simple): {len(codes_premix)} formule(s) - {codes_premix}")
print(f"✓ Usine (mixte): {len(codes_usine)} formule(s) - {codes_usine}")
print("\nLes combobox devraient maintenant afficher ces codes correctement!")
print("=" * 70)
