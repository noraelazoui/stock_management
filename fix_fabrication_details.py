from models.database import db
from bson import ObjectId
import json
from datetime import datetime
import sys

# Classe pour permettre la sérialisation des ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, o)

def log(message):
    """Affiche un message horodaté"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def find_formule_with_type_conversion(code, optim):
    """
    Recherche une formule avec différentes conversions de type pour optim
    """
    # Essayer avec les valeurs d'origine
    formule = db.formules.find_one({"code": code, "optim": optim})
    if formule:
        log(f"Formule trouvée directement avec code={code}, optim={optim}")
        return formule
    
    # Essayer avec optim converti en entier si c'est une chaîne
    if isinstance(optim, str):
        try:
            numeric_optim = int(optim)
            formule = db.formules.find_one({"code": code, "optim": numeric_optim})
            if formule:
                log(f"Formule trouvée avec optim converti en entier: {numeric_optim}")
                return formule
        except ValueError:
            pass
    
    # Essayer avec optim converti en chaîne si c'est un nombre
    if isinstance(optim, (int, float)):
        formule = db.formules.find_one({"code": code, "optim": str(optim)})
        if formule:
            log(f"Formule trouvée avec optim converti en chaîne: {str(optim)}")
            return formule
    
    # Recherche moins stricte sur le code (insensible à la casse)
    formules = list(db.formules.find({"optim": optim}))
    for f in formules:
        if f.get("code", "").lower() == code.lower():
            log(f"Formule trouvée avec recherche insensible à la casse")
            return f
    
    log(f"Aucune formule trouvée pour code={code}, optim={optim}")
    return None

def get_article_details(article_code):
    """
    Récupère les détails d'un article avec différentes stratégies de recherche
    """
    # Recherche directe
    article = db.articles.find_one({"code": article_code})
    if article:
        return article
    
    # Recherche insensible à la casse
    articles = list(db.articles.find())
    for a in articles:
        if a.get("code", "").lower() == article_code.lower():
            return a
    
    # Recherche par inclusion
    for a in articles:
        if article_code.lower() in a.get("code", "").lower():
            return a
    
    return None

def calculate_fabrication_details(formule, fabrication):
    """
    Calcule les détails d'une fabrication à partir d'une formule
    """
    details = []
    
    try:
        composantes = formule.get("composantes", [])
        log(f"Nombre de composantes dans la formule: {len(composantes)}")
        
        # Convertir quantité à fabriquer en nombre flottant
        try:
            quantite_a_fabriquer = float(fabrication.get("quantite_a_fabriquer", 0))
        except (ValueError, TypeError):
            log(f"Erreur de conversion pour quantite_a_fabriquer: {fabrication.get('quantite_a_fabriquer')}")
            quantite_a_fabriquer = 0
        
        # Traiter chaque composante
        for comp in composantes:
            article_name = comp.get("article", "")
            article_code = article_name.split(" - ")[0] if " - " in article_name else article_name
            
            log(f"Recherche de l'article: {article_code}")
            article = get_article_details(article_code)
            
            if article:
                log(f"Article trouvé: {article.get('code')}")
                try:
                    pourcentage = float(comp.get("pourcentage", 0))
                    quantite_fabrique = (pourcentage * quantite_a_fabriquer) / 100
                    prix = float(article.get("prix", 0))
                    
                    detail = {
                        "article": comp.get("article", ""),
                        "dem": article.get("dem", ""),
                        "quantite_stock": article.get("quantite", 0),
                        "prix": prix,
                        "pourcentage": pourcentage,
                        "quantite_fabrique": quantite_fabrique,
                        "prix_total": (prix * pourcentage * quantite_a_fabriquer) / 100
                    }
                    details.append(detail)
                    log(f"Détail ajouté pour {article_code}")
                except (ValueError, TypeError) as e:
                    log(f"Erreur lors du calcul des détails pour {article_code}: {e}")
            else:
                log(f"Article non trouvé: {article_code}")
    
    except Exception as e:
        log(f"Erreur générale: {e}")
    
    return details

def fix_fabrication(fabrication_id=None, code=None, optim=None):
    """
    Corrige les détails d'une fabrication spécifique
    """
    # Récupérer la fabrication par ID ou code/optim
    fabrication = None
    if fabrication_id:
        fabrication = db.fabrications.find_one({"_id": ObjectId(fabrication_id)})
        if fabrication:
            log(f"Fabrication trouvée par ID: {fabrication_id}")
    elif code and optim:
        fabrication = db.fabrications.find_one({"code": code, "optim": optim})
        if fabrication:
            log(f"Fabrication trouvée par code/optim: {code}/{optim}")
    
    if not fabrication:
        log("Fabrication non trouvée")
        return False
    
    # Vérifier si les détails existent déjà
    existing_details = fabrication.get("detail-fabrication", {}).get("article", [])
    if existing_details:
        log(f"La fabrication a déjà {len(existing_details)} détails")
        return True
    
    # Trouver la formule correspondante
    code = fabrication.get("code")
    optim = fabrication.get("optim")
    formule = find_formule_with_type_conversion(code, optim)
    
    if not formule:
        log(f"Aucune formule trouvée pour code={code}, optim={optim}")
        return False
    
    # Calculer les détails
    details = calculate_fabrication_details(formule, fabrication)
    if not details:
        log("Aucun détail n'a pu être calculé")
        return False
    
    # Mettre à jour la fabrication
    result = db.fabrications.update_one(
        {"_id": fabrication["_id"]},
        {"$set": {"detail-fabrication": {"article": details}}}
    )
    
    if result.modified_count > 0:
        log(f"Fabrication mise à jour avec {len(details)} détails")
        
        # Vérifier le résultat
        updated = db.fabrications.find_one({"_id": fabrication["_id"]})
        new_details = updated.get("detail-fabrication", {}).get("article", [])
        log(f"Après mise à jour: {len(new_details)} détails")
        
        return True
    else:
        log("Aucune modification n'a été effectuée")
        return False

def fix_all_fabrications():
    """
    Corrige toutes les fabrications qui ont des détails vides
    """
    # Récupérer toutes les fabrications
    fabrications = list(db.fabrications.find())
    log(f"Nombre total de fabrications: {len(fabrications)}")
    
    # Filtrer celles qui ont des détails vides
    fabrications_vides = [f for f in fabrications if not f.get("detail-fabrication", {}).get("article")]
    log(f"Fabrications avec détails vides: {len(fabrications_vides)}")
    
    # Statistiques
    total = len(fabrications_vides)
    succes = 0
    echec = 0
    
    # Traiter chaque fabrication
    for i, fab in enumerate(fabrications_vides):
        fab_id = fab.get("_id")
        code = fab.get("code")
        optim = fab.get("optim")
        
        log(f"\nTraitement de la fabrication {i+1}/{total}: {code}-{optim} (ID: {fab_id})")
        
        if fix_fabrication(fabrication_id=str(fab_id)):
            succes += 1
        else:
            echec += 1
    
    # Afficher le récapitulatif
    log("\n=== RÉCAPITULATIF ===")
    log(f"Total des fabrications traitées: {total}")
    log(f"Corrections réussies: {succes}")
    log(f"Corrections échouées: {echec}")
    
    return succes, echec

# Programme principal
if __name__ == "__main__":
    log("=== CORRECTION DES FABRICATIONS AVEC DÉTAILS VIDES ===")
    
    # Vérifier les arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            # Corriger toutes les fabrications
            log("Mode: correction de toutes les fabrications")
            fix_all_fabrications()
        elif len(sys.argv) > 2:
            # Corriger une fabrication spécifique par code/optim
            code = sys.argv[1]
            optim = sys.argv[2]
            log(f"Mode: correction de la fabrication spécifique {code}-{optim}")
            fix_fabrication(code=code, optim=optim)
        else:
            # Corriger une fabrication spécifique par ID
            fabrication_id = sys.argv[1]
            log(f"Mode: correction de la fabrication avec ID {fabrication_id}")
            fix_fabrication(fabrication_id=fabrication_id)
    else:
        # Par défaut, corriger la fabrication spécifique "mama-1"
        log("Mode: correction de la fabrication 'mama-1' (par défaut)")
        fix_fabrication(code="mama", optim="1")
    
    log("=== TRAITEMENT TERMINÉ ===")
