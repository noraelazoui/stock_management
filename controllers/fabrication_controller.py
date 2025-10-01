from models.fabrication import Fabrication
from models.formule import FormuleManager
from models.database import db
from models.schemas import FabricationSchema as Schema, FormuleSchema, get_field_value

class FabricationController:
    def __init__(self):
        self.formule_manager = FormuleManager()
    
    def creer_fabrication(self, code, optim, recette_code, nb_composantes, quantite_a_fabriquer=None, date_fabrication=None, lot=None, prix_formule=None):
        return Fabrication.creer_fabrication(code, optim, recette_code, nb_composantes, quantite_a_fabriquer, date_fabrication, lot, prix_formule)
    
    def modifier_fabrication(self, code, optim, nouvelles_donnees):
        return Fabrication.modifier_fabrication(code, optim, nouvelles_donnees)
    
    def supprimer_fabrication(self, code, optim):
        return Fabrication.supprimer_fabrication(code, optim)
    
    def get_all_fabrications(self):
        fabrications = Fabrication.get_all_fabrications()
        print("[DEBUG] Fabrications récupérées :")
        for fabrication in fabrications:
            print(fabrication)
        return fabrications
    
    def get_by_code_optim(self, code, optim):
        return Fabrication.get_by_code_optim(code, optim)
    
    def get_details_fabrication(self, code, optim):
        return Fabrication.get_details_fabrication(code, optim)
    
    def get_pourcentage_article(self, code_formule, optim_formule, code_article):
        """
        Récupère le pourcentage associé à un article dans une formule spécifique
        """
        # Récupérer la formule
        formule = db.formules.find_one({
            FormuleSchema.CODE: code_formule, 
            FormuleSchema.OPTIM: optim_formule
        })
        if not formule:
            return 0
        
        # Parcourir les composantes pour trouver l'article
        C = FormuleSchema.Component
        for comp in get_field_value(formule, [FormuleSchema.COMPONENTS, "composantes"], []):
            article_name = get_field_value(comp, [C.ARTICLE, "article"], "")
            # Vérifier si le code de l'article correspond
            if article_name.startswith(code_article):
                return float(get_field_value(comp, [C.PERCENTAGE, "pourcentage"], 0))
        
        return 0
    
    def get_composantes_formule(self, code_formule, optim_formule):
        """
        Récupère toutes les composantes d'une formule avec leurs pourcentages
        """
        formule = db.formules.find_one({
            FormuleSchema.CODE: code_formule, 
            FormuleSchema.OPTIM: optim_formule
        })
        if not formule:
            return []
            
        return get_field_value(formule, [FormuleSchema.COMPONENTS, "composantes"], [])
