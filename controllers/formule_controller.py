from models.formule import Formule, Composante
from models.schemas import FormuleSchema as Schema

class FormuleController:
    def lister_formules_par_type(self):
        """Retourne un dictionnaire avec les formules simples et mixtes séparées."""
        from models.formule import FormuleManager
        return {
            'simples': FormuleManager.get_simples(),
            'mixtes': FormuleManager.get_mixtes()
        }
    def ajouter_formule(self, formule):
        formule.save()

    def supprimer_formule(self, code):
        formules = Formule.get_by_code(code)
        if formules:
            for f in formules:
                f.delete()

    def get_formule(self, code):
        return Formule.get_by_code(code)

    def lister_formules(self):
        return Formule.all()
    def lister_formules(self):
        return Formule.all()
