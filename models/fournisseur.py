from models.database import db

class FournisseurModel:
    def __init__(self):
        self.collection = db.fournisseurs

    @property
    def fournisseurs(self):
        return list(self.collection.find({}, {"_id": 0}))

    def add(self, fournisseur):
        # Vérifier doublon Nom
        if self.collection.find_one({"Nom": fournisseur["Nom"]}):
            return False, "Nom déjà existant"
        self.collection.insert_one(fournisseur)
        return True, "Fournisseur ajouté"

    def update(self, fournisseur_nom, new_data):
        result = self.collection.update_one({"Nom": fournisseur_nom}, {"$set": new_data})
        if result.matched_count:
            return True, "Fournisseur modifié"
        return False, "Fournisseur non trouvé"

    def delete(self, fournisseur_nom):
        result = self.collection.delete_one({"Nom": fournisseur_nom})
        if result.deleted_count:
            return True, "Fournisseur supprimé"
        return False, "Fournisseur non trouvé"
