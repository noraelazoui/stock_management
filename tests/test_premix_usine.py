import unittest
from models.fabrication import Fabrication
from models.database import db
import uuid

class TestPremixUsineFabrication(unittest.TestCase):
    def setUp(self):
        # Nettoyer les collections pour un test propre
        db.articles.delete_many({"code": {"$in": ["MPA", "MPB", "PREMIX1", "USINE1"]}})
        db.formules.delete_many({"code": {"$in": ["PREMIX1", "USINE1"]}})
        db.fabrications.delete_many({"code": {"$in": ["PREMIX1", "USINE1"]}})
        # Créer deux matières premières
        db.articles.insert_many([
            {"code": "MPA", "nom": "Matiere A", "prix": 10, "quantite": 100},
            {"code": "MPB", "nom": "Matiere B", "prix": 20, "quantite": 200}
        ])
        # Créer une formule Premix
        db.formules.insert_one({
            "code": "PREMIX1",
            "optim": "1",
            "composantes": [
                {"article": "MPA", "pourcentage": 60},
                {"article": "MPB", "pourcentage": 40}
            ]
        })
        # Créer une formule Usine qui utilise le Premix
        db.formules.insert_one({
            "code": "USINE1",
            "optim": "1",
            "composantes": [
                {"article": "PREMIX1", "pourcentage": 100}
            ]
        })

    def test_fabrication_premix_et_usine(self):
        # 1. Fabriquer le Premix
        fabrication_premix = Fabrication.creer_fabrication(
            code="PREMIX1",
            optim="1",
            recette_code="R001",
            nb_composantes=2,
            quantite_a_fabriquer=10,
            lot="L001"
        )
        self.assertIsNotNone(fabrication_premix)
        # Vérifier que le stock des matières premières a diminué
        mpa = db.articles.find_one({"code": "MPA"})
        mpb = db.articles.find_one({"code": "MPB"})
        self.assertLess(mpa["quantite"], 100)
        self.assertLess(mpb["quantite"], 200)
        # Ajouter le Premix comme article autonome
        db.articles.insert_one({"code": "PREMIX1", "nom": "Premix 1", "prix": 15, "quantite": 10, "lot": "L001"})
        # 2. Fabriquer le produit Usine en utilisant le Premix
        fabrication_usine = Fabrication.creer_fabrication(
            code="USINE1",
            optim="1",
            recette_code="R002",
            nb_composantes=1,
            quantite_a_fabriquer=5,
            lot="L002"
        )
        self.assertIsNotNone(fabrication_usine)
        # Vérifier que le stock du Premix a diminué
        premix = db.articles.find_one({"code": "PREMIX1"})
        self.assertLess(premix["quantite"], 10)
        # Vérifier la traçabilité dans detail-fabrication
        details_usine = fabrication_usine["detail-fabrication"]
        self.assertTrue(any(d["article"] == "PREMIX1" for d in details_usine))

    def tearDown(self):
        db.articles.delete_many({"code": {"$in": ["MPA", "MPB", "PREMIX1", "USINE1"]}})
        db.formules.delete_many({"code": {"$in": ["PREMIX1", "USINE1"]}})
        db.fabrications.delete_many({"code": {"$in": ["PREMIX1", "USINE1"]}})

if __name__ == "__main__":
    unittest.main()
