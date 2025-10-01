import unittest
from models.formule import Formule, Composante
from controllers.formule_controller import FormuleController

class TestFormuleCRUD(unittest.TestCase):
    def setUp(self):
        self.controller = FormuleController()
        self.formule = Formule(
            code="F001",
            optim="Optim1",
            designation="Formule Test",
            description="Description test",
            date_creation="2025-08-26 10:00",
            composantes=[Composante("Article1", 60, "kg"), Composante("Article2", 40, "kg")]
        )

    def test_add_formule(self):
        self.controller.ajouter_formule(self.formule)
        self.assertEqual(len(self.controller.formules), 1)
        self.assertEqual(self.controller.formules[0].code, "F001")

    def test_get_formule(self):
        self.controller.ajouter_formule(self.formule)
        f = self.controller.get_formule("F001")
        self.assertIsNotNone(f)
        self.assertEqual(f.optim, "Optim1")

    def test_list_formules(self):
        self.controller.ajouter_formule(self.formule)
        formules = self.controller.lister_formules()
        self.assertEqual(len(formules), 1)
        self.assertEqual(formules[0].designation, "Formule Test")

    def test_delete_formule(self):
        self.controller.ajouter_formule(self.formule)
        self.controller.supprimer_formule("F001")
        self.assertEqual(len(self.controller.formules), 0)
        self.assertIsNone(self.controller.get_formule("F001"))

    def test_composantes(self):
        self.controller.ajouter_formule(self.formule)
        f = self.controller.get_formule("F001")
        self.assertEqual(len(f.composantes), 2)
        f.ajouter_composante(Composante("Article3", 10, "kg"))
        self.assertEqual(len(f.composantes), 3)
        f.supprimer_composante(0)
        self.assertEqual(len(f.composantes), 2)
        self.assertTrue(f.valider() is False)  # total != 100

if __name__ == "__main__":
    unittest.main()
