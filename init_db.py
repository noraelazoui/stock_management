from datetime import datetime
from models.database import db

def initialize_test_data():
    try:
        print("Vérification de la connexion MongoDB...")
        # Test de la connexion
        db.command("ping")
        print("Connexion MongoDB OK!")

        # Supprimer les anciennes données de test
        print("\nSuppression des anciennes formules...")
        db.formules.delete_many({})
        
        # Créer des formules de test
        formules_test = [
            {
                "code": "FORM001",
                "optim": "OPT1",
                "designation": "Formule Simple 1",
                "description": "Première formule simple de test",
                "date_creation": datetime.now(),
                "composantes": [{"article": "ART001", "pourcentage": 100}],
                "type_formule": "simple",
                "quantity": 0
            },
            {
                "code": "FORM002",
                "optim": "OPT2",
                "designation": "Formule Simple 2",
                "description": "Deuxième formule simple de test",
                "date_creation": datetime.now(),
                "composantes": [{"article": "ART002", "pourcentage": 100}],
                "type_formule": "simple",
                "quantity": 0
            },
            {
                "code": "FORM003",
                "optim": "OPT3",
                "designation": "Formule Mixte",
                "description": "Formule mixte de test",
                "date_creation": datetime.now(),
                "composantes": [
                    {"article": "ART003", "pourcentage": 60},
                    {"article": "ART004", "pourcentage": 40}
                ],
                "type_formule": "mixte",
                "quantity": 0
            }
        ]

        print("\nInsertion des formules de test...")
        for formule in formules_test:
            db.formules.insert_one(formule)
        
        # Vérifier les formules insérées
        print("\nVérification des formules dans la base de données:")
        
        print("\nToutes les formules:")
        all_formules = list(db.formules.find({}, {'code': 1, 'type_formule': 1, '_id': 0}))
        print(all_formules)
        
        print("\nFormules simples uniquement:")
        simple_formules = list(db.formules.find({'type_formule': 'simple'}, {'code': 1, 'type_formule': 1, '_id': 0}))
        print(simple_formules)
        
        print("\nInitialisation terminée avec succès!")
        
    except Exception as e:
        print(f"Erreur lors de l'initialisation: {e}")

if __name__ == "__main__":
    initialize_test_data()
