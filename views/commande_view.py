import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        # S'assurer que le combobox n'est PAS en readonly
        if 'state' in kwargs and kwargs['state'] == 'readonly':
            del kwargs['state']
        
        super().__init__(master, state='normal', **kwargs)
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace("w", self.on_text_change)
        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<Button-1>", self.on_click)
        self.bind("<<ComboboxSelected>>", self.on_select)
        self.original_values = []
        self.filtering = False

    def set_values(self, values):
        """Définit les valeurs originales pour l'autocomplétion"""
        self.original_values = list(values) if values else []
        self['values'] = self.original_values

    def on_text_change(self, *args):
        """Appelé quand le texte change - Filtre les suggestions"""
        if self.filtering:
            return
            
        current_text = self.var.get()
        if not current_text:
            self['values'] = self.original_values
            return
            
        matches = [item for item in self.original_values 
                  if current_text.lower() in item.lower()]
        
        self.filtering = True
        self['values'] = matches if matches else []
        self.filtering = False

    def on_key_release(self, event):
        """Appelé lors du relâchement d'une touche"""
        if event.keysym in ['Up', 'Down', 'Left', 'Right', 'Return', 'Tab', 
                           'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
            return

    def on_click(self, event):
        """Appelé lors d'un clic sur le combobox"""
        if not self.var.get():
            self['values'] = self.original_values

    def on_select(self, event):
        """Appelé lors de la sélection d'un élément dans la liste"""
        pass


class CommandeView(ttk.Frame):
    def set_fournisseurs(self, fournisseurs):
        self.fournisseurs = fournisseurs
    def __init__(self, parent, main_notebook=None):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.controller = None
        self.main_notebook = main_notebook
        self.fournisseurs = []
        self.create_widgets()
        if self.main_notebook:
            self.main_notebook.bind("<Button-1>", self.on_tab_click)
        else:
            self.notebook.bind("<Button-1>", self.on_tab_click)

    def create_widgets(self):
        # Formulaire principal
        form_frame = ttk.LabelFrame(self, text="Commande", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        form_row = ttk.Frame(form_frame)
        form_row.pack(fill=tk.X, padx=2, pady=2)

        ttk.Label(form_row, text="Référence :", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        self.ref_entry = ttk.Entry(form_row, width=15)
        self.ref_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row, text="Date réception :", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        from tkcalendar import DateEntry
        self.date_reception_entry = DateEntry(form_row, width=15, date_pattern='y-mm-dd')
        self.date_reception_entry.pack(side=tk.LEFT, padx=2)


        # Boutons
        self.add_btn = ttk.Button(form_row, text="Ajouter", width=15)
        self.add_btn.pack(side=tk.LEFT, padx=2)
        self.modify_btn = ttk.Button(form_row, text="Modifier", width=15)
        self.modify_btn.pack(side=tk.LEFT, padx=2)
        self.delete_btn = ttk.Button(form_row, text="Supprimer", width=15)
        self.delete_btn.pack(side=tk.LEFT, padx=2)
        self.reset_btn = ttk.Button(form_row, text="Réinitialiser", width=15)
        self.reset_btn.pack(side=tk.LEFT, padx=2)

        # Tableau des commandes
        table_frame = ttk.LabelFrame(self, text="Liste des commandes", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ref", "date_reception", "detail")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        # Style pour les en-têtes plus foncés
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('TkDefaultFont', 9, 'bold'), background='#4a4a4a', foreground='white')
        
        for col, text in zip(columns, ["Référence", "Date réception", "Détail"]):
            self.tree.heading(col, text=text)
        self.tree.column("ref", width=100)
        self.tree.column("date_reception", width=120)
        self.tree.column("detail", width=80, anchor="center")
        
        # Scrollbar verticale
        tree_vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<Double-1>", self.open_detail_tab)

        # Notebook pour onglets détail
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.notebook.bind("<Button-1>", self.on_tab_click)

        # Initialisation des fournisseurs
        self.load_initial_fournisseurs()

    def load_initial_fournisseurs(self):
        """Charge les fournisseurs depuis la base de données au démarrage"""
        try:
            from models.database import db
            fournisseurs_db = list(db.fournisseurs.find({}, {"_id": 0}))
            fournisseur_list = []
            
            print(f"DEBUG: Fournisseurs trouvés dans MongoDB: {fournisseurs_db}")
            
            for f in fournisseurs_db:
                nom = (f.get("nom", "") or f.get("Nom", "") or 
                       f.get("name", "") or f.get("Name", "") or
                       f.get("ID", "") or f.get("id", "")).strip()
                
                if nom:
                    fournisseur_list.append(nom)
            
            self.fournisseurs = fournisseur_list
        except Exception as e:
            self.fournisseurs = []

    def refresh_tree(self):
        """Rafraîchit l'arbre principal (appelé depuis le contrôleur)"""
        if self.controller:
            self.controller.refresh_tree()

    def open_detail_tab(self, event):
        """Ouvre l'onglet détail pour une commande sélectionnée"""
        selected = self.tree.selection()
        if not selected:
            return
            
        item = selected[0]
        region = self.tree.identify_column(event.x)
        if region != "#3":  # Vérifier qu'on a cliqué sur la colonne "Détail"
            return
            
        ref = self.tree.item(item, "values")[0]
        title = f"Détail {ref} ✖"

        # Fermer tout onglet détail déjà ouvert
        for tab_id in self.notebook.tabs():
            tab_text = self.notebook.tab(tab_id, "text")
            if tab_text.startswith("Détail "):
                self.notebook.forget(tab_id)
                break

        # Créer le frame détail
        detail_frame = ttk.Frame(self.notebook)
        self.notebook.add(detail_frame, text=title)
        self.notebook.select(detail_frame)

        # Créer l'interface du détail de commande
        self._create_detail_interface(detail_frame, ref)

    def _create_detail_interface(self, detail_frame, ref):
        """Crée l'interface complète de l'onglet détail"""
        
        # Titre
        titre_label = tk.Label(detail_frame, text="Bon de réception", 
                              font=("Helvetica", 12, "bold"), fg="#2a9f5d", bg="#eafbf1")
        titre_label.pack(side=tk.TOP, fill=tk.X, pady=2)

        # === SECTION INFOS COMMANDE (Mode, Date, Fournisseur, etc.) ===
        self._create_info_commande_section(detail_frame, ref)
        
        # === SECTION PRODUITS ===
        self._create_produits_section(detail_frame, ref)
        
        # === SECTION INFOS GENERALES (Statut, Remarque, Utilisateur) ===
        self._create_infos_generales_section(detail_frame, ref)

        # Charger toutes les données depuis la base
        if self.controller:
            self.controller.load_commande_details(ref, detail_frame)

        # Pré-remplir le champ référence principal
        self.ref_entry.delete(0, tk.END)
        self.ref_entry.insert(0, ref)

    def _create_info_commande_section(self, detail_frame, ref):
        """Crée la section Informations commande (detail_commande)"""
        info_frame = ttk.LabelFrame(detail_frame, text="Informations commande", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        labels = ["Mode", "Date", "Fournisseur", "Payement", "Adresse", "Transport", "Numéro"]

        # Formulaire de saisie
        entry_row_frame = ttk.Frame(info_frame)
        entry_row_frame.pack(fill=tk.X, padx=2, pady=2)
        detail_entries = {}

        for idx, label in enumerate(labels):
            label_widget = ttk.Label(entry_row_frame, text=label+" :", font=('TkDefaultFont', 9, 'bold'))
            label_widget.pack(side=tk.LEFT, padx=2)

            if label == "Fournisseur":
                entry = AutocompleteCombobox(entry_row_frame, width=15)
                entry.set_values(self.fournisseurs)
                # Ne pas sélectionner automatiquement le premier fournisseur
                entry.pack(side=tk.LEFT, padx=2)
                detail_entries[label] = entry
            elif label == "Date":
                from tkcalendar import DateEntry
                date_entry = DateEntry(entry_row_frame, width=15, date_pattern='y-mm-dd')
                date_entry.pack(side=tk.LEFT, padx=2)
                detail_entries[label] = date_entry
            else:
                entry = ttk.Entry(entry_row_frame, width=15)
                entry.pack(side=tk.LEFT, padx=2)
                detail_entries[label] = entry

            # Ajouter les boutons juste après le champ "Numéro"
            if label == "Numéro":
                ttk.Button(entry_row_frame, text="Ajouter", command=lambda: add_info_row(), width=12).pack(side=tk.LEFT, padx=5)
                ttk.Button(entry_row_frame, text="Modifier", command=lambda: modify_info_row(), width=12).pack(side=tk.LEFT, padx=5)
                ttk.Button(entry_row_frame, text="Supprimer", command=lambda: delete_info_row(), width=12).pack(side=tk.LEFT, padx=5)

        # Tableau avec scrollbar
        info_table_frame = ttk.Frame(info_frame)
        info_table_frame.pack(fill=tk.X, padx=2, pady=2)
        
        info_table = ttk.Treeview(info_table_frame, columns=labels, show="headings", height=3)
        for label in labels:
            info_table.heading(label, text=label)
            info_table.column(label, width=110, anchor="center")
            
        info_vsb = ttk.Scrollbar(info_table_frame, orient="vertical", command=info_table.yview)
        info_table.configure(yscrollcommand=info_vsb.set)
        info_table.grid(row=0, column=0, sticky="nsew")
        info_vsb.grid(row=0, column=1, sticky="ns")
        info_table_frame.grid_rowconfigure(0, weight=1)
        info_table_frame.grid_columnconfigure(0, weight=1)

        # Exposer le tableau pour le contrôleur
        detail_frame.info_commande_table = info_table

        # Définir les fonctions de gestion
        def add_info_row():
            info_row = {}
            for label in labels:
                if label == "Date":
                    date_entry = detail_entries[label]
                    date_val = date_entry.get().strip()
                    info_row[label] = date_val
                else:
                    value = detail_entries[label].get().strip()
                    info_row[label] = value
            # Ajouter dans le tableau ET dans la base via le contrôleur
            if self.controller:
                if self.controller.add_info_commande_detail(ref, info_row):
                    info_table.insert("", "end", values=list(info_row.values()))
                    # Vider les champs de saisie
                    for entry in detail_entries.values():
                        if hasattr(entry, 'delete'):
                            entry.delete(0, tk.END)

        def modify_info_row():
            selected = info_table.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Sélectionnez une ligne à modifier.")
                return
                
            item = selected[0]
            old_values = info_table.item(item, "values")
            old_row = {labels[i]: old_values[i] for i in range(len(labels))}
            
            new_row = {}
            for label in labels:
                value = detail_entries[label].get().strip()
                new_row[label] = value
            
            # Modifier dans la base via le contrôleur
            if self.controller:
                if self.controller.modify_info_commande_detail(ref, old_row, new_row):
                    info_table.item(item, values=list(new_row.values()))
                    # Vider les champs de saisie
                    for entry in detail_entries.values():
                        if hasattr(entry, 'delete'):
                            entry.delete(0, tk.END)

        def delete_info_row():
            selected = info_table.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Sélectionnez une ligne à supprimer.")
                return
                
            if messagebox.askyesno("Confirmation", "Supprimer cette ligne ?"):
                for item in selected:
                    old_values = info_table.item(item, "values")
                    old_row = {labels[i]: old_values[i] for i in range(len(labels))}
                    
                    # Supprimer de la base via le contrôleur
                    if self.controller:
                        if self.controller.delete_info_commande_detail(ref, old_row):
                            info_table.delete(item)

    # ...existing code...

    def _create_produits_section(self, detail_frame, ref):
        """Crée la section Produits"""
        prod_fields = [
            "Code", "DESIGNATION ARTICLE", "DEM", "QUANTITE", "QUANTITE REEL",
            "Prix UNI.", "TVA", "Prix TTC", "MONTANT", "MONTANT REEL"
        ]

        # Charger les articles depuis MongoDB
        try:
            from models.database import db
            articles_db = list(db.articles.find({}, {"_id": 0, "code": 1, "designation": 1, "type": 1}))
            
            mp_codes = []
            add_codes = []
            code_to_designation = {}
            
            for article in articles_db:
                code = article.get("code", "").strip()
                designation = article.get("designation", "").strip()
                type_art = article.get("type", "").strip().lower()
                
                if not code:
                    continue
                    
                code_to_designation[code] = designation
                
                type_normalized = type_art.replace("é", "e").replace("è", "e").replace(" ", "")
                
                if "matiere" in type_normalized and "premiere" in type_normalized:
                    mp_codes.append(code)
                elif "additif" in type_normalized:
                    add_codes.append(code)
            
            article_codes = []
            if mp_codes:
                article_codes.append("--- Matières premières ---")
                article_codes.extend(mp_codes)
            if add_codes:
                article_codes.append("--- Additifs ---")
                article_codes.extend(add_codes)
            if not article_codes:
                article_codes = ["Aucun article"]
                
        except Exception as e:
            print(f"Erreur lors du chargement des articles : {e}")
            article_codes = ["Erreur chargement"]
            code_to_designation = {}

        # Formulaire produit
        prod_form_frame = ttk.LabelFrame(detail_frame, text="Ajouter / Modifier produit", padding=5)
        prod_form_frame.pack(fill=tk.X, padx=5, pady=5)

        # Validation pour n'accepter que des chiffres (float) pour les champs numériques
        def validate_float(P):
            if P == "":
                return True
            try:
                float(P)
                return True
            except ValueError:
                return False
        vcmd_float = (prod_form_frame.register(validate_float), '%P')

        prod_form_entries = {}
        for i, field in enumerate(prod_fields):
            if field in ["MONTANT", "Prix TTC", "MONTANT REEL"]:
                continue  # Ces champs sont calculés automatiquement

            ttk.Label(prod_form_frame, text=field+" :", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=i, sticky="w", padx=2)

            if field == "Code":
                entry = ttk.Combobox(prod_form_frame, values=article_codes, state="normal", width=15)

                def update_designation(event=None, entry=entry):
                    display_code = entry.get()
                    if display_code.startswith("---"):
                        des_entry = prod_form_entries.get("DESIGNATION ARTICLE")
                        if des_entry:
                            des_entry.delete(0, tk.END)
                        return
                    designation = code_to_designation.get(display_code, "")
                    des_entry = prod_form_entries.get("DESIGNATION ARTICLE")
                    if des_entry:
                        des_entry.delete(0, tk.END)
                        des_entry.insert(0, designation)

                entry.bind("<<ComboboxSelected>>", update_designation)
                entry.bind("<KeyRelease>", update_designation)
            elif field in ["QUANTITE", "QUANTITE REEL", "Prix UNI.", "TVA"]:
                entry = ttk.Entry(prod_form_frame, width=15, validate="key", validatecommand=vcmd_float)
            else:
                entry = ttk.Entry(prod_form_frame, width=15)
            entry.grid(row=1, column=i, padx=2)
            prod_form_entries[field] = entry

        # Tableau produits
        product_frame = ttk.LabelFrame(detail_frame, text="Produits", padding=10)
        product_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=15)

    # ...existing code...
        product_tree_frame = ttk.Frame(product_frame)
        product_tree_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        product_tree = ttk.Treeview(product_tree_frame, columns=prod_fields, show="headings", height=10)
        for col in prod_fields:
            product_tree.heading(col, text=col)
            product_tree.column(col, width=110, anchor="center")

        vsb = ttk.Scrollbar(product_tree_frame, orient="vertical", command=product_tree.yview)
        hsb = ttk.Scrollbar(product_tree_frame, orient="horizontal", command=product_tree.xview)
        product_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        product_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        product_tree_frame.grid_rowconfigure(0, weight=1)
        product_tree_frame.grid_columnconfigure(0, weight=1)

        # Exposer le tableau pour le contrôleur
        detail_frame.product_tree = product_tree

        # Fonctions de gestion des produits
        def calculate_amounts():
            """Calcule Prix TTC, MONTANT et MONTANT REEL"""
            try:
                prix_uni = float(prod_form_entries["Prix UNI."].get() or 0)
                tva = float(prod_form_entries["TVA"].get() or 0)
                quantite = float(prod_form_entries["QUANTITE"].get() or 0)
                quantite_reel = float(prod_form_entries["QUANTITE REEL"].get() or 0)
                
                prix_ttc = prix_uni * (1 + tva / 100)
                montant = prix_ttc * quantite
                montant_reel = prix_ttc * quantite_reel
                
                return prix_ttc, montant, montant_reel
            except ValueError:
                return 0.0, 0.0, 0.0

        def insert_product_row():
            product_row = {}
            prix_ttc, montant, montant_reel = calculate_amounts()
            
            for field in prod_fields:
                if field == "Prix TTC":
                    product_row[field] = f"{prix_ttc:.2f}"
                elif field == "MONTANT":
                    product_row[field] = f"{montant:.2f}"
                elif field == "MONTANT REEL":
                    product_row[field] = f"{montant_reel:.2f}"
                elif field in prod_form_entries:
                    product_row[field] = prod_form_entries[field].get()
                else:
                    product_row[field] = ""

            # Ajouter via le contrôleur
            if self.controller:
                if self.controller.add_product_row(ref, product_row):
                    values = [product_row[field] for field in prod_fields]
                    product_tree.insert("", "end", values=values)
                    # Vider les champs
                    for entry in prod_form_entries.values():
                        if hasattr(entry, 'delete'):
                            entry.delete(0, tk.END)

        def modify_product_row():
            selected = product_tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Sélectionnez une ligne à modifier.")
                return
                
            item = selected[0]
            old_values = product_tree.item(item, "values")
            old_row = {prod_fields[i]: old_values[i] for i in range(len(prod_fields))}
            
            new_row = {}
            prix_ttc, montant, montant_reel = calculate_amounts()
            
            for field in prod_fields:
                if field == "Prix TTC":
                    new_row[field] = f"{prix_ttc:.2f}"
                elif field == "MONTANT":
                    new_row[field] = f"{montant:.2f}"
                elif field == "MONTANT REEL":
                    new_row[field] = f"{montant_reel:.2f}"
                elif field in prod_form_entries:
                    new_row[field] = prod_form_entries[field].get()
                else:
                    new_row[field] = ""

            # Modifier via le contrôleur
            if self.controller:
                if self.controller.modify_product_row(ref, old_row, new_row):
                    values = [new_row[field] for field in prod_fields]
                    product_tree.item(item, values=values)
                    # Vider les champs
                    for entry in prod_form_entries.values():
                        if hasattr(entry, 'delete'):
                            entry.delete(0, tk.END)

        def delete_product_row():
            selected = product_tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Sélectionnez une ligne à supprimer.")
                return
                
            if messagebox.askyesno("Confirmation", f"Supprimer {len(selected)} ligne(s) ?"):
                for item in selected:
                    old_values = product_tree.item(item, "values")
                    old_row = {prod_fields[i]: old_values[i] for i in range(len(prod_fields))}
                    
                    # Supprimer via le contrôleur
                    if self.controller:
                        if self.controller.delete_product_row(ref, old_row):
                            product_tree.delete(item)

        # Placer les boutons à côté du champ TVA dans le formulaire produit
        # Chercher l'index du champ TVA
        tva_index = None
        for i, field in enumerate(prod_fields):
            if field == "TVA":
                tva_index = i
                break
        if tva_index is not None:
            btn_col = tva_index + 1
            ttk.Button(prod_form_frame, text="Ajouter ligne", command=insert_product_row, width=13).grid(row=1, column=btn_col, padx=1)
            ttk.Button(prod_form_frame, text="Modifier ligne", command=modify_product_row, width=13).grid(row=1, column=btn_col+1, padx=1)
            ttk.Button(prod_form_frame, text="Supprimer ligne", command=delete_product_row, width=13).grid(row=1, column=btn_col+2, padx=1)

    def _create_infos_generales_section(self, detail_frame, ref):
        """Crée la section Infos générales commande (infos_commande)"""
        infos_commande_frame = ttk.LabelFrame(detail_frame, text="Infos générales commande", padding=10)
        infos_commande_frame.pack(fill=tk.X, padx=10, pady=5)
        
        infos_labels = ["Statut", "Remarque", "Utilisateur"]
        infos_entries = {}
        
        # Formulaire de saisie
        infos_row_frame = ttk.Frame(infos_commande_frame)
        infos_row_frame.pack(fill=tk.X, padx=2, pady=2)
        
        for label in infos_labels:
            label_widget = ttk.Label(infos_row_frame, text=label+" :", font=('TkDefaultFont', 9, 'bold'))
            label_widget.pack(side=tk.LEFT, padx=2)
            entry = ttk.Entry(infos_row_frame, width=15)
            entry.pack(side=tk.LEFT, padx=2)
            infos_entries[label] = entry

        # Boutons
        infos_btn_frame = ttk.Frame(infos_commande_frame)
        infos_btn_frame.pack(fill=tk.X, pady=5)
        
        # Tableau avec scrollbar
        infos_table_frame = ttk.Frame(infos_commande_frame)
        infos_table_frame.pack(fill=tk.X, padx=2, pady=2)
        
        infos_table = ttk.Treeview(infos_table_frame, columns=infos_labels, show="headings", height=3)
        for label in infos_labels:
            infos_table.heading(label, text=label)
            infos_table.column(label, width=110, anchor="center")
            
        infos_vsb = ttk.Scrollbar(infos_table_frame, orient="vertical", command=infos_table.yview)
        infos_table.configure(yscrollcommand=infos_vsb.set)
        infos_table.grid(row=0, column=0, sticky="nsew")
        infos_vsb.grid(row=0, column=1, sticky="ns")
        infos_table_frame.grid_rowconfigure(0, weight=1)
        infos_table_frame.grid_columnconfigure(0, weight=1)

        # Exposer le tableau pour le contrôleur
        detail_frame.infos_generales_table = infos_table

        # Fonctions de gestion
        def add_infos_commande_row():
            infos_row = {}
            for label in infos_labels:
                value = infos_entries[label].get().strip()
                infos_row[label] = value
                
            # Ajouter via le contrôleur
            if self.controller:
                if self.controller.add_infos_commande(ref, infos_row):
                    infos_table.insert("", "end", values=list(infos_row.values()))
                    # Vider les champs
                    for entry in infos_entries.values():
                        if hasattr(entry, 'delete'):
                            entry.delete(0, tk.END)

        def modify_infos_commande_row():
            selected = infos_table.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Sélectionnez une ligne à modifier.")
                return
                
            item = selected[0]
            old_values = infos_table.item(item, "values")
            old_row = {infos_labels[i]: old_values[i] for i in range(len(infos_labels))}
            
            new_row = {}
            for label in infos_labels:
                value = infos_entries[label].get().strip()
                new_row[label] = value
            
            # Modifier via le contrôleur
            if self.controller:
                if self.controller.modify_infos_commande(ref, old_row, new_row):
                    infos_table.item(item, values=list(new_row.values()))
                    # Vider les champs
                    for entry in infos_entries.values():
                        if hasattr(entry, 'delete'):
                            entry.delete(0, tk.END)

        def delete_infos_commande_row():
            selected = infos_table.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Sélectionnez une ligne à supprimer.")
                return
                
            if messagebox.askyesno("Confirmation", "Supprimer cette ligne ?"):
                for item in selected:
                    old_values = infos_table.item(item, "values")
                    old_row = {infos_labels[i]: old_values[i] for i in range(len(infos_labels))}
                    
                    # Supprimer via le contrôleur
                    if self.controller:
                        if self.controller.delete_infos_commande(ref, old_row):
                            infos_table.delete(item)

        # Associer les boutons
        ttk.Button(infos_btn_frame, text="Ajouter", command=add_infos_commande_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(infos_btn_frame, text="Modifier", command=modify_infos_commande_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(infos_btn_frame, text="Supprimer", command=delete_infos_commande_row).pack(side=tk.LEFT, padx=5)

    # === MÉTHODES UTILITAIRES ===
    def update_fournisseurs(self):
        """Récupère et met à jour la liste des fournisseurs depuis la base de données"""
        try:
            if hasattr(self, "controller") and hasattr(self.controller, "model"):
                fournisseurs_db = self.controller.model.get_fournisseurs()
                self.fournisseurs = [f for f in fournisseurs_db if f and f.strip()]
            else:
                self.load_initial_fournisseurs()
                return
                
            self._update_all_fournisseur_combobox()
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour des fournisseurs : {e}")

    def _update_all_fournisseur_combobox(self):
        """Met à jour tous les Combobox fournisseurs"""
        # Combobox principal
        if hasattr(self, "fournisseur_combo") and self.fournisseur_combo.winfo_exists():
            self.fournisseur_combo.set_values(self.fournisseurs)
            if self.fournisseurs and not self.fournisseur_combo.get():
                self.fournisseur_combo.set(self.fournisseurs[0])

        # Combobox dans les onglets détail
        for tab_id in self.notebook.tabs():
            try:
                frame = self.nametowidget(tab_id)
                self._update_fournisseur_combobox_in_frame(frame)
            except Exception as e:
                print(f"Erreur lors de la mise à jour du combobox dans l'onglet : {e}")

    def _update_fournisseur_combobox_in_frame(self, frame):
        """Met à jour récursivement les combobox fournisseurs dans un frame"""
        for child in frame.winfo_children():
            if isinstance(child, ttk.LabelFrame) and child.cget("text") == "Informations commande":
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Frame):
                        for widget in subchild.winfo_children():
                            if isinstance(widget, AutocompleteCombobox):
                                widget.set_values(self.fournisseurs)
                                if self.fournisseurs and not widget.get():
                                    widget.set(self.fournisseurs[0])
            elif hasattr(child, 'winfo_children'):
                self._update_fournisseur_combobox_in_frame(child)

    def on_tab_click(self, event):
        """Gère la fermeture des onglets avec le bouton X"""
        notebook = self.main_notebook if self.main_notebook else self.notebook
        x, y = event.x, event.y
        element = notebook.identify(x, y)
        
        if "label" in element:
            index = notebook.index(f"@{x},{y}")
            text = notebook.tab(index, "text")
            
            if "✖" in text:
                bbox = notebook.bbox(index)
                if bbox:
                    label_x, label_y, label_w, label_h = bbox
                    import tkinter.font
                    font = tkinter.font.nametofont("TkDefaultFont")
                    txt = text.replace("✖", "").strip()
                    txt_width = font.measure(txt)
                    
                    # Vérifier si le clic est sur la zone X
                    if x > label_x + txt_width:
                        if messagebox.askyesno("Fermeture", "Voulez-vous vraiment fermer cet onglet ?"):
                            notebook.forget(index)