from models.database import db
from pprint import pprint

# Afficher le nombre total de formules
formules = list(db.formules.find())
print(f"\nNombre total de formules dans la base: {len(formules)}")

# Vérifier si la formule avec code "mama" et optim "1" existe
print("\n=== RECHERCHE FORMULE SPÉCIFIQUE ===")
print("Recherche formule avec code='mama', optim='1'")

# Essayer différentes variantes du champ optim
formule_str = db.formules.find_one({"code": "mama", "optim": "1"})
formule_int = db.formules.find_one({"code": "mama", "optim": 1})
print(f"Formule trouvée avec optim='1' (string): {formule_str is not None}")
print(f"Formule trouvée avec optim=1 (int): {formule_int is not None}")

# Afficher la formule trouvée, si elle existe
formule = formule_str or formule_int
if formule:
    print("\n=== DÉTAILS DE LA FORMULE ===")
    print(f"Code: {formule.get('code')}")
    print(f"Optim: {formule.get('optim')} (type: {type(formule.get('optim')).__name__})")
    
    # Vérifier les composantes
    composantes = formule.get('composantes', [])
    print(f"Nombre de composantes: {len(composantes)}")
    
    # Afficher chaque composante
    for i, comp in enumerate(composantes, 1):
        print(f"\nComposante {i}:")
        article_name = comp.get("article", "")
        print(f"- Article: {article_name}")
        article_code = article_name.split(" - ")[0] if " - " in article_name else article_name
        print(f"- Code article extrait: {article_code}")
        print(f"- Pourcentage: {comp.get('pourcentage', 0)}")
        
        # Vérifier si l'article existe
        article = db.articles.find_one({"code": article_code})
        print(f"- Article trouvé dans la base: {article is not None}")
        if article:
            print(f"- Détails de l'article: nom={article.get('nom', '')}, prix={article.get('prix', 0)}")
else:
    print("\n=== FORMULE NON TROUVÉE ===")
    print("La formule avec code 'mama' et optim '1' n'existe pas dans la base.")
    
    # Liste toutes les formules disponibles pour aider à comprendre quelles formules existent
    print("\n=== LISTE DES FORMULES DISPONIBLES ===")
    for i, f in enumerate(formules, 1):
        print(f"{i}. code='{f.get('code')}', optim='{f.get('optim')}' (type: {type(f.get('optim')).__name__})")
