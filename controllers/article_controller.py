from models.article import ArticleModel
from models.schemas import ArticleSchema as Schema
from views.article_view import ArticleView
from tkinter import messagebox
import tkinter as tk

class ArticleController:
    def get_article_by_code_and_unit(self, code, unit):
        # Cherche l'article avec le code et l'unité
        articles = self.model.collection.find({Schema.CODE: code, Schema.UNIT: unit})
        for art in articles:
            return {k: v for k, v in art.items() if k != "_id"}
        return None
    def __init__(self, root):
        self.model = ArticleModel()
        self.view = ArticleView(root, self)
        self.view.refresh_table(self.model.articles)

    def add_article(self):
        art = {
            Schema.CODE: self.view.code_entry.get(),
            Schema.DESIGNATION: self.view.designation_entry.get(),
            Schema.TYPE: self.view.type_combo.get()
        }
        if not art[Schema.CODE] or not art[Schema.DESIGNATION]:
            messagebox.showwarning("Champs manquants","Veuillez remplir tous les champs.")
            return
        if self.model.add_article(art):
            self.view.refresh_table(self.model.articles)
            # Synchronisation avec GestionApp
            if hasattr(self.view, 'on_add_article'):
                self.view.on_add_article(art)
            # Reset des champs du formulaire après ajout
            self.view.code_entry.delete(0, tk.END)
            self.view.designation_entry.delete(0, tk.END)
            self.view.type_combo.current(0)
            # Reset des champs de détail si ils existent
            if hasattr(self.view, 'prix_entry'):
                self.view.prix_entry.delete(0, tk.END)
            if hasattr(self.view, 'qte_entry'):
                self.view.qte_entry.delete(0, tk.END)
            if hasattr(self.view, 'dem_entry'):
                self.view.dem_entry.delete(0, tk.END)
            if hasattr(self.view, 'batch_entry'):
                self.view.batch_entry.delete(0, tk.END)
            if hasattr(self.view, 'fab_entry'):
                self.view.fab_entry.delete(0, tk.END)
            if hasattr(self.view, 'exp_entry'):
                self.view.exp_entry.delete(0, tk.END)
            if hasattr(self.view, 'mois_entry'):
                self.view.mois_entry.delete(0, tk.END)
            if hasattr(self.view, 'alerte_entry'):
                self.view.alerte_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Doublon","Code déjà existant.")

    def modify_article(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection","Sélectionnez un article à modifier.")
            return
        old_code = self.view.tree.item(selected[0])["values"][0]
        new_data = {
            "code": self.view.code_entry.get(),
            "designation": self.view.designation_entry.get(),
            "type": self.view.type_combo.get()
        }
        self.model.modify_article(old_code, new_data)
        self.view.refresh_table(self.model.articles)

    def delete_article(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez un ou plusieurs articles à supprimer.")
            return
        # Supprimer tous les articles sélectionnés
        for item in selected:
            art_code = self.view.tree.item(item)["values"][0]
            self.model.delete_article(art_code)
        self.view.refresh_table(self.model.articles)

    def on_tree_click(self, event):
        region = self.view.tree.identify("region", event.x, event.y)
        col = self.view.tree.identify_column(event.x)
        if region == "cell" and col == "#4":  # Colonne Détail
            row_id = self.view.tree.identify_row(event.y)
            if not row_id:
                return
            art_code = self.view.tree.item(row_id)["values"][0]
            if not art_code:
                return
            art = self.model.get_article(art_code)
            if art:
                self.view.show_detail_form(art)

