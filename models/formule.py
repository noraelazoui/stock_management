class FormuleManager:
    @staticmethod
    def get_simples():
        # Retourne les formules simples en se basant sur l'attribut type_formule
        return [f for f in Formule.all() if getattr(f, 'type_formule', 'simple') == 'simple']

    @staticmethod
    def get_mixtes():
        # Retourne les formules mixtes en se basant sur l'attribut type_formule
        return [f for f in Formule.all() if getattr(f, 'type_formule', 'simple') == 'mixte']

    @staticmethod
    def get_composants(formule_id, quantite):
        formule = next((f for f in Formule.all() if getattr(f, '_id', None) == formule_id), None)
        if not formule:
            return []
        composants = []
        for comp in formule.composantes:
            composants.append({
                "id": getattr(comp.article, 'id', None),
                "nom": getattr(comp.article, 'designation', str(comp.article)),
                "quantite": comp.pourcentage * quantite / 100,
                "pourcentage": comp.pourcentage
            })
        return composants

    @staticmethod
    def is_formule(component_code):
        """
        Check if the given component code corresponds to a formula.
        """
        formule = db.formules.find_one({"code": component_code})
        return formule is not None

import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from models.database import db

class Composante:
    def __init__(self, article, pourcentage, optim_formule=None, recette_formule=None):
        self.article = article
        self.pourcentage = pourcentage
        self.optim_formule = optim_formule
        self.recette_formule = recette_formule
    def to_dict(self):
        return {
            "article": self.article,
            "pourcentage": self.pourcentage,
            "optim_formule": self.optim_formule,
            "recette_formule": self.recette_formule
        }
    @staticmethod
    def from_dict(d):
        return Composante(
            d["article"],
            d["pourcentage"],
            d.get("optim_formule"),
            d.get("recette_formule")
        )

class Formule:
    def __init__(self, code, optim, designation, description, date_creation, composantes=None, quantity=0, _id=None, recette_code=None, type_formule=None):
        self.code = code
        self.optim = optim
        self.designation = designation
        self.description = description
        self.date_creation = date_creation
        self.composantes = composantes if composantes else []
        self.quantity = quantity
        self._id = _id
        self.recette_code = recette_code
        self.type_formule = type_formule  # Sera déterminé lors de la sauvegarde en fonction des composantes

    def to_dict(self):
        return {
            "code": self.code,
            "optim": self.optim,
            "designation": self.designation,
            "description": self.description,
            "date_creation": self.date_creation,
            "composantes": [c.to_dict() for c in self.composantes],
            "quantity": self.quantity,
            "recette_code": self.recette_code,
            "type_formule": self.type_formule
        }

    @staticmethod
    def from_dict(d):
        composantes = [Composante.from_dict(c) for c in d.get("composantes", [])]
        return Formule(
            d["code"],
            d.get("optim", ""),
            d.get("designation", ""),
            d.get("description", ""),
            d.get("date_creation", ""),
            composantes,
            d.get("quantity", 0),
            d.get("_id"),
            d.get("recette_code", None),
            d.get("type_formule", "simple")
        )

    def total_pourcentage(self):
        return sum(c.pourcentage for c in self.composantes)

    def ajouter_composante(self, composante):
        self.composantes.append(composante)

    def supprimer_composante(self, index):
        if 0 <= index < len(self.composantes):
            del self.composantes[index]
            self.save()

    def valider(self):
        return abs(self.total_pourcentage() - 100) < 0.01

    def save(self):
        # Nettoie le dictionnaire pour éviter les champs None ou vides
        data = self.to_dict()
        data = {k: v for k, v in data.items() if v is not None and v != ""}
        if "composantes" not in data or not isinstance(data["composantes"], list):
            data["composantes"] = []

        print("\n[DEBUG] === VÉRIFICATION DU TYPE DE FORMULE ===")
        print(f"Code de la formule: {self.code}")
        
        # Analyser chaque composante en détail
        has_formule_component = False
        for i, composante in enumerate(self.composantes, 1):
            print(f"\nAnalyse composante {i}:")
            
            # Vérifier si c'est une formule
            is_formule = bool(composante.optim_formule or composante.recette_formule)
            
            print(f"- Type: {'Formule' if is_formule else 'Article'}")
            print(f"- Optim formule: {composante.optim_formule}")
            print(f"- Recette formule: {composante.recette_formule}")
            print(f"- Article: {composante.article}")
            
            if is_formule:
                has_formule_component = True
                print("=> Cette composante est une formule !")
                break
        
        # Déterminer le type final
        determined_type = 'mixte' if has_formule_component else 'simple'
        data['type_formule'] = determined_type
        
        print(f"\nRÉSULTAT:")
        print(f"- Contient des formules: {has_formule_component}")
        print(f"- Type déterminé: {determined_type}")
        print("=====================================\n")
        
        # Si au moins une composante est une formule, alors c'est une formule mixte
        data['type_formule'] = 'mixte' if has_formule_component else 'simple'
        print(f"[DEBUG] Détermination du type: {'mixte' if has_formule_component else 'simple'} "
              f"(contient des formules: {has_formule_component})")

        if not data["composantes"]:
            print("[AVERTISSEMENT] La formule n'a aucune composante enregistrée !")
        else:
            print(f"[DEBUG] {len(data['composantes'])} composantes à enregistrer.")

        # DEBUG : Affiche les valeurs avant sauvegarde
        print("[DEBUG] Sauvegarde Formule:")
        print(f"  code={self.code}")
        print(f"  optim={self.optim}")
        print(f"  recette_code={self.recette_code}")
        print(f"  type_formule={data['type_formule']}")
        print(f"  data={data}")

        # Remplace la formule existante avec le même code et optim, ou insère si elle n'existe pas
        result = db.formules.replace_one({"code": self.code, "optim": self.optim}, data, upsert=True)
        print(f"Formule enregistrée dans MongoDB : code={self.code}, optim={self.optim}, type={data['type_formule']}")

    def delete(self):
        db.formules.delete_one({"code": self.code})

    @staticmethod
    def get_by_code(code):
        # Retourne toutes les formules ayant le même code
        docs = db.formules.find({"code": code})
        formules = []
        
        for doc in docs:
            formule = Formule.from_dict(doc)
            # Vérifier si le type est correct basé sur les composantes
            has_formule = any(
                comp.optim_formule is not None or comp.recette_formule is not None
                for comp in formule.composantes
            )
            correct_type = 'mixte' if has_formule else 'simple'
            
            if formule.type_formule != correct_type:
                print(f"\n[ATTENTION] Formule {code}: Type incorrect détecté")
                print(f"Type actuel: {formule.type_formule}")
                print(f"Type correct: {correct_type}")
                formule.type_formule = correct_type
                
            formules.append(formule)
        
        return formules

    @staticmethod
    def all():
        return [Formule.from_dict(d) for d in db.formules.find({"code": {"$exists": True}})]

    @staticmethod
    def get_by_code_optim(code, optim):
        # Debug: Afficher toutes les formules pour voir ce qui est disponible
        print("\nDébut recherche formule ===")
        print(f"Recherche formule avec code='{code}' et optim='{optim}' (type: {type(optim)})")
        
        # Afficher toutes les formules disponibles
        all_formules = list(db.formules.find())
        print("\nFormules disponibles dans la base:")
        for f in all_formules:
            print(f"- code: '{f.get('code')}', optim: '{f.get('optim')}', type: {type(f.get('optim'))}")
        
        # Essayer différents types pour optim
        # D'abord essayer avec la valeur telle quelle
        doc = db.formules.find_one({"code": code, "optim": optim})
        
        if not doc and isinstance(optim, str):
            # Si optim est une chaîne et qu'on n'a rien trouvé, essayer de le convertir en nombre
            try:
                numeric_optim = int(optim)
                doc = db.formules.find_one({"code": code, "optim": numeric_optim})
                print(f"Tentative avec optim numérique: {numeric_optim}")
            except ValueError:
                pass
        
        if not doc and isinstance(optim, (int, float)):
            # Si optim est un nombre et qu'on n'a rien trouvé, essayer avec une chaîne
            doc = db.formules.find_one({"code": code, "optim": str(optim)})
            print(f"Tentative avec optim string: {str(optim)}")
        
        print(f"\nRésultat de la recherche: {doc}")
        print("=== Fin recherche formule\n")
        
        if doc:
            return Formule.from_dict(doc)
        return None
