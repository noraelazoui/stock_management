from pymongo import MongoClient
from datetime import datetime

# Connexion à la base MongoDB avec gestion d'erreur
try:
    client = MongoClient('mongodb://localhost:27017/')
    # Test de connexion
    client.admin.command('ismaster')
    db = client['stock_manager']
    print("Connexion MongoDB établie avec succès.")
except Exception as e:
    print(f"Erreur de connexion à MongoDB : {e}")
    exit(1)

# Création des collections si elles n'existent pas
collections_requises = ["articles", "commandes", "fournisseurs", "fabrications", "formules"]
for collection_name in collections_requises:
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        print(f"Collection '{collection_name}' créée.")

def enregistrer_formule_mongodb(code, optim, designation, description, date_creation, composantes, quantity=0, recette_code=None, type_formule="simple"):
    """
    Enregistre une formule complète avec composantes dans MongoDB.
    
    Args:
        code (str): Code de la formule
        optim (str): Code d'optimisation
        designation (str): Désignation de la formule
        description (str): Description de la formule
        date_creation (datetime): Date de création
        composantes (list): Liste des composantes
        quantity (int): Quantité (défaut: 0)
        recette_code (str): Code de recette (optionnel)
        type_formule (str): Type de la formule ('mixte' ou 'simple', défaut: 'simple')
    """
    try:
        # Validation des paramètres obligatoires
        if not all([code, optim, designation, composantes]):
            raise ValueError("Les paramètres code, optim, designation et composantes sont obligatoires")
        
        if not isinstance(composantes, list):
            raise ValueError("Les composantes doivent être une liste")
        
        # Validation de la date
        if isinstance(date_creation, str):
            try:
                date_creation = datetime.strptime(date_creation, "%Y-%m-%d")
            except ValueError:
                date_creation = datetime.now()
        elif not isinstance(date_creation, datetime):
            date_creation = datetime.now()
        
        # Création du document formule
        formule_doc = {
            "code": code,
            "optim": optim,
            "designation": designation,
            "description": description,
            "date_creation": date_creation,
            "composantes": composantes,
            "quantity": quantity,
            "recette_code": recette_code,
            "type_formule": type_formule,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Enregistrement avec upsert pour éviter les doublons
        result = db.formules.replace_one(
            {"code": code, "optim": optim}, 
            formule_doc, 
            upsert=True
        )
        
        if result.upserted_id:
            print(f"Formule '{code}' créée avec {len(composantes)} composantes dans MongoDB.")
        else:
            print(f"Formule '{code}' mise à jour avec {len(composantes)} composantes dans MongoDB.")
            
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la formule '{code}': {e}")
        return False

def verifier_formule_mongodb(code, optim=None):
    """
    Affiche la formule et ses composantes enregistrées dans MongoDB pour vérification.
    
    Args:
        code (str): Code de la formule
        optim (str): Code d'optimisation (optionnel)
    """
    try:
        # Construction de la requête
        query = {"code": code}
        if optim:
            query["optim"] = optim
        doc = db.formules.find_one(query)
        if not doc:
            print(f"Aucune formule trouvée pour code='{code}'" + (f" et optim='{optim}'" if optim else ""))
            return False
        print(f"\n=== Formule trouvée ===")
        print(f"Code: {doc['code']}")
        print(f"Optim: {doc.get('optim', 'N/A')}")
        print(f"Désignation: {doc.get('designation', 'N/A')}")
        print(f"Description: {doc.get('description', 'N/A')}")
        print(f"Type de formule: {doc.get('type_formule', 'N/A')}")
        print(f"Date création: {doc.get('date_creation', 'N/A')}")
        print(f"Quantité: {doc.get('quantity', 0)}")
        print(f"Code recette: {doc.get('recette_code', 'N/A')}")
        composantes = doc.get("composantes", [])
        print(f"\nComposantes ({len(composantes)}):")
        if composantes:
            for i, c in enumerate(composantes, 1):
                article = c.get('article', 'N/A')
                pourcentage = c.get('pourcentage', 0)
                print(f"  {i}. Article: {article}, Pourcentage: {pourcentage}%")
        else:
            print("  Aucune composante trouvée")
        return True
    except Exception as e:
        print(f"Erreur lors de la vérification de la formule '{code}': {e}")
        return False

def enregistrer_article_mongodb(code, designation, type_article, produits=None):
    """
    Enregistre un article dans MongoDB avec la structure simplifiée demandée.
    
    Structure: article (code/type/designation/produit(prix,quantite,dem,batch,date_fabrication,date_expiration,alerte,seuil))
    
    Args:
        code (str): Code de l'article
        designation (str): Désignation de l'article  
        type_article (str): Type de l'article
        produits (list): Liste des produits avec leurs détails complets
            Chaque produit doit avoir la structure:
            {
                "produit": "nom_du_produit",
                "prix": float,
                "quantite": int,
                "dem": str,  # demande
                "batch": str,  # numéro de lot
                "date_fabrication": datetime ou str,
                "date_expiration": datetime ou str,
                "alerte": bool,
                "seuil": int
            }
    """
    try:
        # Validation des paramètres obligatoires
        if not all([code, designation, type_article]):
            raise ValueError("Les paramètres code, designation et type_article sont obligatoires")
        
        # Traitement des produits
        produits_final = []
        if produits:
            for produit_info in produits:
                if not isinstance(produit_info, dict):
                    print(f"Attention: Produit ignoré (format invalide): {produit_info}")
                    continue
                
                # Conversion des dates si nécessaire
                date_fab = produit_info.get('date_fabrication')
                date_exp = produit_info.get('date_expiration')
                
                if isinstance(date_fab, str):
                    try:
                        date_fab = datetime.strptime(date_fab, "%Y-%m-%d")
                    except ValueError:
                        date_fab = None
                        
                if isinstance(date_exp, str):
                    try:
                        date_exp = datetime.strptime(date_exp, "%Y-%m-%d")
                    except ValueError:
                        date_exp = None
                
                # Construction du produit
                produit = {
                    "produit": produit_info.get('produit', ''),
                    "prix": float(produit_info.get('prix', 0.0)),
                    "quantite": int(produit_info.get('quantite', 0)),
                    "dem": produit_info.get('dem', ''),
                    "batch": produit_info.get('batch', ''),
                    "date_fabrication": date_fab,
                    "date_expiration": date_exp,
                    "alerte": bool(produit_info.get('alerte', False)),
                    "seuil": int(produit_info.get('seuil', 0))
                }
                produits_final.append(produit)
        
        # Construction du document article selon la structure demandée (SANS "detail")
        article = {
            "code": code,
            "type": type_article,
            "designation": designation,
            "produit": produits_final
        }
        
        # Enregistrement avec upsert
        result = db.articles.replace_one({"code": code}, article, upsert=True)
        
        if result.upserted_id:
            print(f"Article '{code}' enregistré dans MongoDB avec {len(produits_final)} produits.")
        else:
            print(f"Article '{code}' mis à jour dans MongoDB avec {len(produits_final)} produits.")
            
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'article '{code}': {e}")
        return False

def verifier_article_mongodb(code):
    """
    Affiche l'article et ses détails enregistrés dans MongoDB pour vérification.
    
    Args:
        code (str): Code de l'article
    """
    try:
        doc = db.articles.find_one({"code": code})
        
        if not doc:
            print(f"Aucun article trouvé pour code='{code}'")
            return False
        
        print(f"\n=== Article trouvé ===")
        print(f"Code: {doc['code']}")
        print(f"Type: {doc.get('type', 'N/A')}")
        print(f"Désignation: {doc.get('designation', 'N/A')}")
        
        # Affichage des produits
        produits = doc.get("produit", [])
        if produits:
            print(f"\nProduits ({len(produits)}):")
            for i, prod in enumerate(produits, 1):
                print(f"  {i}. Produit: {prod.get('produit', 'N/A')}")
                print(f"     - Prix: {prod.get('prix', 0)} €")
                print(f"     - Quantité: {prod.get('quantite', 0)}")
                print(f"     - Demande: {prod.get('dem', 'N/A')}")
                print(f"     - Batch: {prod.get('batch', 'N/A')}")
                print(f"     - Date fabrication: {prod.get('date_fabrication', 'N/A')}")
                print(f"     - Date expiration: {prod.get('date_expiration', 'N/A')}")
                print(f"     - Alerte: {'Oui' if prod.get('alerte', False) else 'Non'}")
                print(f"     - Seuil: {prod.get('seuil', 0)}")
                print()
        else:
            print("\nAucun produit trouvé")
            
        return True
        
    except Exception as e:
        print(f"Erreur lors de la vérification de l'article '{code}': {e}")
        return False

def fermer_connexion_mongodb():
    """
    Ferme proprement la connexion MongoDB.
    """
    try:
        client.close()
        print("Connexion MongoDB fermée.")
    except Exception as e:
        print(f"Erreur lors de la fermeture de la connexion: {e}")

# Fonctions utilitaires supplémentaires

def lister_formules():
    """
    Liste toutes les formules dans la base de données.
    """
    try:
        formules = list(db.formules.find({}, {"code": 1, "optim": 1, "designation": 1}))
        if formules:
            print(f"\n=== Liste des formules ({len(formules)}) ===")
            for f in formules:
                print(f"- {f['code']} ({f.get('optim', 'N/A')}) : {f.get('designation', 'N/A')}")
        else:
            print("Aucune formule trouvée dans la base de données.")
    except Exception as e:
        print(f"Erreur lors de la récupération des formules: {e}")

def lister_articles():
    """
    Liste tous les articles dans la base de données.
    """
    try:
        articles = list(db.articles.find({}, {"code": 1, "designation": 1, "type": 1}))
        if articles:
            print(f"\n=== Liste des articles ({len(articles)}) ===")
            for a in articles:
                print(f"- {a['code']} : {a.get('designation', 'N/A')} ({a.get('type', 'N/A')})")
        else:
            print("Aucun article trouvé dans la base de données.")
    except Exception as e:
        print(f"Erreur lors de la récupération des articles: {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Test d'enregistrement d'un article avec la nouvelle structure
    produits_details = [
        {
            "produit": "Produit A",
            "prix": 25.50,
            "quantite": 100,
            "dem": "Commande urgent",
            "batch": "LOT2024001",
            "date_fabrication": "2024-01-15",
            "date_expiration": "2024-12-31",
            "alerte": False,
            "seuil": 10
        },
        {
            "produit": "Produit B", 
            "prix": 45.80,
            "quantite": 50,
            "dem": "Stock normal",
            "batch": "LOT2024002",
            "date_fabrication": "2024-02-01",
            "date_expiration": "2025-01-31",
            "alerte": True,
            "seuil": 5
        }
    ]
    
    
    
   
    # Test d'enregistrement d'une formule
    composantes_test = [
        {"article": "ART001", "pourcentage": 50},
        {"article": "ART002", "pourcentage": 30},
        {"article": "ART003", "pourcentage": 20}
    ]
    
    
    # Fermeture de la connexion
    # fermer_connexion_mongodb()