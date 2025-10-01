from models.database import db
from bson import ObjectId
import json
from datetime import datetime

# Classe pour permettre la sérialisation des ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, o)

def log_message(message, level="INFO"):
    """Affiche un message formaté avec l'heure"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def fix_fabrication_details(fabrication):
    """
    Vérifie et met à jour les détails d'une fabrication si nécessaire.
    
    Args:
        fabrication: Document de fabrication à vérifier
        
    Returns:
        tuple: (True/False pour indiquer si une mise à jour a été effectuée,
                nombre de détails ajoutés)
    """
    # Si les détails existent déjà, pas besoin de mettre à jour
    existing_details = fabrication.get("detail-fabrication", {}).get("article", [])
    if existing_details:
        log_message(f"La fabrication {fabrication['code']}-{fabrication['optim']} (ID: {fabrication['_id']}) a déjà {len(existing_details)} détails.")
        return False, len(existing_details)
    
    log_message(f"La fabrication {fabrication['code']}-{fabrication['optim']} (ID: {fabrication['_id']}) n'a pas de détails. Tentative de correction...")
    
    # Récupérer la formule correspondante avec différentes tentatives de type
    code = fabrication["code"]
    optim = fabrication["optim"]
    formule = None
    
    # Essayer avec les valeurs telles quelles
    formule = db.formules.find_one({"code": code, "optim": optim})
    
    # Essayer avec différentes conversions de type pour optim
    if not formule and isinstance(optim, str):
        try:
            numeric_optim = int(optim)
            formule = db.formules.find_one({"code": code, "optim": numeric_optim})
            if formule:
                log_message(f"Formule trouvée avec optim converti en entier: {code}-{numeric_optim}")
        except ValueError:
            pass
    
    if not formule and isinstance(optim, (int, float)):
        formule = db.formules.find_one({"code": code, "optim": str(optim)})
        if formule:
            log_message(f"Formule trouvée avec optim converti en string: {code}-{str(optim)}")
    
    if not formule:
        log_message(f"Aucune formule trouvée pour {code}-{optim}. Impossible de corriger.", level="ERROR")
        return False, 0
    
    # Calculer les détails de fabrication
    details = []
    composantes = formule.get("composantes", [])
    log_message(f"Formule trouvée avec {len(composantes)} composantes.")
    
    try:
        quantite_a_fabriquer = float(fabrication.get("quantite_a_fabriquer", 0))
    except (ValueError, TypeError):
        log_message(f"Erreur de conversion de la quantité à fabriquer: {fabrication.get('quantite_a_fabriquer')}", level="ERROR")
        quantite_a_fabriquer = 0
    
    for comp in composantes:
        article_name = comp.get("article", "")
        article_code = article_name.split(" - ")[0] if " - " in article_name else article_name
        article = db.articles.find_one({"code": article_code})
        
        if article:
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
                log_message(f"Détail ajouté pour l'article {article_code}.")
            except (ValueError, TypeError) as e:
                log_message(f"Erreur lors du calcul des détails pour {article_code}: {e}", level="ERROR")
        else:
            log_message(f"Article non trouvé: {article_code}", level="WARNING")
    
    if not details:
        log_message(f"Aucun détail n'a pu être calculé pour {code}-{optim}.", level="WARNING")
        return False, 0
    
    # Mettre à jour la fabrication avec les détails calculés
    try:
        result = db.fabrications.update_one(
            {"_id": fabrication["_id"]},
            {"$set": {"detail-fabrication": {"article": details}}}
        )
        
        if result.modified_count > 0:
            log_message(f"Fabrication {code}-{optim} mise à jour avec {len(details)} détails.", level="SUCCESS")
            return True, len(details)
        else:
            log_message(f"Aucune modification pour {code}-{optim}. Même contenu ou erreur.", level="WARNING")
            return False, 0
    except Exception as e:
        log_message(f"Erreur lors de la mise à jour de {code}-{optim}: {e}", level="ERROR")
        return False, 0

def main():
    log_message("Début de la vérification et correction des fabrications.")
    
    # Récupérer toutes les fabrications
    fabrications = list(db.fabrications.find())
    log_message(f"Nombre total de fabrications: {len(fabrications)}")
    
    # Statistiques
    total_fabrications = len(fabrications)
    updated_count = 0
    already_ok_count = 0
    failed_count = 0
    total_details_added = 0
    
    # Traiter chaque fabrication
    for fabrication in fabrications:
        try:
            updated, details_count = fix_fabrication_details(fabrication)
            
            if updated:
                updated_count += 1
                total_details_added += details_count
            elif details_count > 0:
                already_ok_count += 1
            else:
                failed_count += 1
        except Exception as e:
            log_message(f"Erreur lors du traitement de la fabrication {fabrication.get('_id')}: {e}", level="ERROR")
            failed_count += 1
    
    # Afficher le résumé
    log_message("=== RÉSUMÉ DE L'OPÉRATION ===")
    log_message(f"Total des fabrications traitées: {total_fabrications}")
    log_message(f"Fabrications déjà correctes: {already_ok_count}")
    log_message(f"Fabrications mises à jour: {updated_count}")
    log_message(f"Fabrications non corrigées: {failed_count}")
    log_message(f"Total des détails ajoutés: {total_details_added}")
    log_message("Fin de l'opération.")

if __name__ == "__main__":
    main()
