from models.formule import Formule, Composante
from models.database import db

# Exemple d'ajout d'une formule complète avec composantes
if __name__ == "__main__":
    # Création de composantes
    comp1 = Composante(article="A001", pourcentage=60, unite="kg")
    comp2 = Composante(article="A002", pourcentage=40, unite="kg")

    # Création de la formule
    formule = Formule(
        code="F001",
        optim="OPT1",
        designation="Formule Test",
        description="Formule avec deux composants",
        date_creation="2025-08-31",
        composantes=[comp1, comp2],
        quantity=100,
        recette_code=None
    )

    # Sauvegarde dans MongoDB
    formule.save()
    print("Formule complète enregistrée avec composantes dans MongoDB.")

    # Vérification
    print("Documents formules dans la base :")
    for doc in db.formules.find({"code": "F001"}):
        print(doc)
