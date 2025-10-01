import unittest
from models.database import db
from models.fabrication import Fabrication
import uuid

class TestLogiqueMetierMultiProduits(unittest.TestCase):
    def setUp(self):
        # Nettoyage collections
        db.articles.delete_many({"code": {"$in": ["MPA", "MPB", "MPC", "ADD1", "PREMIX1", "PREMIX2", "PRODFIN1"]}})
        db.formules.delete_many({"code": {"$in": ["PREMIX1", "PREMIX2", "PRODFIN1"]}})
        db.fabrications.delete_many({"code": {"$in": ["PREMIX1", "PREMIX2", "PRODFIN1"]}})
        # Création des produits
        db.articles.insert_many([
            {"code": "MPA", "nom": "Matière A", "type": "matiere", "quantite": 0},
            {"code": "MPB", "nom": "Matière B", "type": "matiere", "quantite": 0},
            {"code": "MPC", "nom": "Matière C", "type": "matiere", "quantite": 0},
            {"code": "ADD1", "nom": "Additif 1", "type": "additif", "quantite": 0},
        ])
        # Commandes (remplissage stock)
        db.articles.update_one({"code": "MPA"}, {"$set": {"quantite": 100}})
        db.articles.update_one({"code": "MPB"}, {"$set": {"quantite": 200}})
        db.articles.update_one({"code": "MPC"}, {"$set": {"quantite": 150}})
        db.articles.update_one({"code": "ADD1"}, {"$set": {"quantite": 50}})
        # Formules
        db.formules.insert_one({
            "code": "PREMIX1", "optim": "1",
            "composantes": [
                {"article": "MPA", "pourcentage": 60},
                {"article": "MPB", "pourcentage": 40}
            ]
        })
        db.formules.insert_one({
            "code": "PREMIX2", "optim": "1",
            "composantes": [
                {"article": "MPC", "pourcentage": 50},
                {"article": "ADD1", "pourcentage": 50}
            ]
        })
        db.formules.insert_one({
            "code": "PRODFIN1", "optim": "1",
            "composantes": [
                {"article": "PREMIX1", "pourcentage": 70},
                {"article": "PREMIX2", "pourcentage": 20},
                {"article": "MPB", "pourcentage": 10}
            ]
        })

    def test_fabrication_multi_etapes(self):
        # Fabriquer PREMIX1 (20)
        fab_premix1 = Fabrication.creer_fabrication(
            code="PREMIX1", optim="1", recette_code="R001", nb_composantes=2, quantite_a_fabriquer=20, lot="L001"
        )
        self.assertIsNotNone(fab_premix1)
        mpa = db.articles.find_one({"code": "MPA"})
        mpb = db.articles.find_one({"code": "MPB"})
        self.assertEqual(mpa["quantite"], 88)
        self.assertEqual(mpb["quantite"], 192)
        # Fabriquer PREMIX2 (10)
        fab_premix2 = Fabrication.creer_fabrication(
            code="PREMIX2", optim="1", recette_code="R002", nb_composantes=2, quantite_a_fabriquer=10, lot="L002"
        )
        self.assertIsNotNone(fab_premix2)
        mpc = db.articles.find_one({"code": "MPC"})
        add1 = db.articles.find_one({"code": "ADD1"})
        self.assertEqual(mpc["quantite"], 145)
        self.assertEqual(add1["quantite"], 45)
        # Ajouter PREMIX1 et PREMIX2 comme articles autonomes
        db.articles.insert_one({"code": "PREMIX1", "nom": "Premix 1", "type": "intermediaire", "quantite": 20, "lot": "L001"})
        db.articles.insert_one({"code": "PREMIX2", "nom": "Premix 2", "type": "intermediaire", "quantite": 10, "lot": "L002"})
        # Fabriquer PRODFIN1 (5)
        fab_prod = Fabrication.creer_fabrication(
            code="PRODFIN1", optim="1", recette_code="R003", nb_composantes=3, quantite_a_fabriquer=5, lot="L003"
        )
        self.assertIsNotNone(fab_prod)
        premix1 = db.articles.find_one({"code": "PREMIX1"})
        premix2 = db.articles.find_one({"code": "PREMIX2"})
        mpb = db.articles.find_one({"code": "MPB"})
        self.assertAlmostEqual(premix1["quantite"], 16.5)
        self.assertAlmostEqual(premix2["quantite"], 9)
        self.assertAlmostEqual(mpb["quantite"], 191.5)
        # Vérification traçabilité
        details_prod = fab_prod["detail-fabrication"]
        self.assertTrue(any(d["article"] == "PREMIX1" for d in details_prod))
        self.assertTrue(any(d["article"] == "PREMIX2" for d in details_prod))
        self.assertTrue(any(d["article"] == "MPB" for d in details_prod))

    # def tearDown(self):
    #     db.articles.delete_many({"code": {"$in": ["MPA", "MPB", "MPC", "ADD1", "PREMIX1", "PREMIX2", "PRODFIN1"]}})
    #     db.formules.delete_many({"code": {"$in": ["PREMIX1", "PREMIX2", "PRODFIN1"]}})
    #     db.fabrications.delete_many({"code": {"$in": ["PREMIX1", "PREMIX2", "PRODFIN1"]}})

if __name__ == "__main__":
    unittest.main()
