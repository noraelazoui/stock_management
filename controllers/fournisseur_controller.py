from models.schemas import SupplierSchema as Schema

class FournisseurController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self
        # Lier les boutons aux fonctions
        self.view.add_btn.config(command=self.add_fournisseur)
        self.view.modify_btn.config(command=self.modify_fournisseur)
        self.view.delete_btn.config(command=self.delete_fournisseur)
        self.view.reset_btn.config(command=self.view.reset_form)

    def add_fournisseur(self):
        data = self.view.get_form_data()
        success, msg = self.model.add(data)
        if success:
            self.view.add_to_tree(data)
            self.view.reset_form()
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
            self.view.update_tree(fournisseur_nom, new_data)
            self.view.reset_form()
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
            self.view.delete_from_tree(fournisseur_nom)
            self.view.reset_form()
        else:
            self.view.show_message(msg)
