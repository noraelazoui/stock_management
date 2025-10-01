import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class FournisseurView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        from models.fournisseur import FournisseurModel
        self.fournisseur_model = FournisseurModel()
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.controller = None
        self.create_widgets()

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Fournisseur", padding=15)
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        # Tous les champs sur la même ligne avec width=15
        labels = ["Nom", "Téléphone", "Email", "Date création"]
        self.entries = {}
        # Validation pour int
        def validate_int(P):
            if P == "":
                return True
            return P.isdigit()
        vcmd_int = (form_frame.register(validate_int), '%P')

        for i, lbl in enumerate(labels):
            ttk.Label(form_frame, text=lbl+":").grid(row=0, column=i*2, sticky="w", pady=3)
            if lbl == "Date création":
                from tkcalendar import DateEntry
                self.date_create_var = tk.StringVar()
                entry = DateEntry(form_frame, textvariable=self.date_create_var, width=15, date_pattern='y-mm-dd')
            elif lbl == "Téléphone":
                entry = ttk.Entry(form_frame, width=15, validate="key", validatecommand=vcmd_int)
            else:
                entry = ttk.Entry(form_frame, width=15)
            entry.grid(row=0, column=i*2+1, sticky="w", pady=3)
            self.entries[lbl] = entry

        # Boutons à côté du champ Date création
        col_btn = len(labels) * 2  # Place les boutons juste après le dernier champ
        self.add_btn = ttk.Button(form_frame, text="Ajouter", width=15)
        self.add_btn.grid(row=0, column=col_btn, padx=2)
        self.modify_btn = ttk.Button(form_frame, text="Modifier", width=15)
        self.modify_btn.grid(row=0, column=col_btn+1, padx=2)
        self.delete_btn = ttk.Button(form_frame, text="Supprimer", width=15)
        self.delete_btn.grid(row=0, column=col_btn+2, padx=2)
        self.reset_btn = ttk.Button(form_frame, text="Réinitialiser", width=15)
        self.reset_btn.grid(row=0, column=col_btn+3, padx=2)

        table_frame = ttk.LabelFrame(self, text="Liste des fournisseurs", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        columns = ("Nom", "Téléphone", "Email", "Date création")

        # Scrollbars pour le tableau fournisseurs
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.refresh_tree()  # Affiche les fournisseurs dès l'ouverture de l'onglet

    # --- Fonctions pour le Controller ---
    def get_form_data(self):
        data = {lbl: self.entries[lbl].get().strip() for lbl in self.entries}
        # Date création
        date_input = self.date_create_var.get().strip()
        if date_input.lower() == "auto" or date_input == "":
            date_input = datetime.today().strftime("%Y-%m-%d")
        data['Date création'] = date_input
        return data

    def add_to_tree(self, data):
        # Ajoute le fournisseur au début du DataGrid (première ligne)
        self.tree.insert("", 0, values=(
            data.get("Nom", ""),
            data.get("Téléphone", ""),
            data.get("Email", ""),
            data.get("Date création", "")
        ))
        if hasattr(self, 'on_add_fournisseur'):
            self.on_add_fournisseur(data.get("Nom", ""))

    def get_selected_tree(self):
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0], "values")
        keys = ["Nom", "Téléphone", "Email", "Date création"]
        return dict(zip(keys, values))

    def update_tree(self, fournisseur_nom, new_data):
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[0] == fournisseur_nom:
                self.tree.item(item, values=(
                    new_data["Nom"], new_data["Téléphone"], new_data["Email"], new_data["Date création"]
                ))
                break

    def delete_from_tree(self, fournisseur_nom):
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[0] == fournisseur_nom:
                self.tree.delete(item)
                break

    def reset_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.date_create_var.set("Auto")

    def show_message(self, msg):
        messagebox.showinfo("Info", msg)

    def refresh_tree(self):
        # Efface le DataGrid
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Ajoute chaque fournisseur au début du DataGrid (première ligne), uniquement si au moins un champ est rempli
        for fournisseur in self.fournisseur_model.fournisseurs:
            if any(fournisseur.get(key, "").strip() for key in ["Nom", "Téléphone", "Email", "Date création"]):
                self.tree.insert("", 0, values=(
                    fournisseur.get("Nom", ""),
                    fournisseur.get("Téléphone", ""),
                    fournisseur.get("Email", ""),
                    fournisseur.get("Date création", "")
                ))
