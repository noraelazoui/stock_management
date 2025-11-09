from models.schemas import SupplierSchema as Schema

class FournisseurController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self
        self.view.fournisseur_model = self.model
        self.view.refresh_tree()

    def add_fournisseur(self):
        data = self.view.get_form_data()
        success, msg = self.model.add(data)
        if success:
            self.view.refresh_tree()
            self.view.reset_form()
            self.view.show_message("Fournisseur ajouté")
        else:
            self.view.show_message(msg)

    def modify_fournisseur(self):
        selected = self.view.get_selected_tree()
        if not selected:
            self.view.show_message("Sélectionnez un fournisseur à modifier")
            return
        fournisseur_nom = selected.get(Schema.NAME, selected.get('Nom'))
        new_data = self.view.get_form_data()
        success, msg = self.model.update(fournisseur_nom, new_data)
        if success:
            self.view.refresh_tree()
            self.view.reset_form()
            self.view.show_message("Fournisseur modifié")
        else:
            self.view.show_message(msg)

    def delete_fournisseur(self):
        selected = self.view.get_selected_tree()
        if not selected:
            self.view.show_message("Sélectionnez un fournisseur à supprimer")
            return
        fournisseur_nom = selected.get(Schema.NAME, selected.get('Nom'))
        success, msg = self.model.delete(fournisseur_nom)
        if success:
            self.view.refresh_tree()
            self.view.reset_form()
            self.view.show_message("Fournisseur supprimé")
        else:
            self.view.show_message(msg)
