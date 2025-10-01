import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.schemas import CommandeSchema as Schema, get_field_value

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
        # Formulaire principal - Compact layout in 2 rows
        form_frame = ttk.LabelFrame(self, text="Commande", padding=5)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        # First row - All main fields
        form_row1 = ttk.Frame(form_frame)
        form_row1.pack(fill=tk.X, padx=2, pady=2)

        ttk.Label(form_row1, text="Réf:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(0,2))
        self.ref_entry = ttk.Entry(form_row1, width=12)
        self.ref_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row1, text="Date:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        from tkcalendar import DateEntry
        self.date_reception_entry = DateEntry(form_row1, width=12, date_pattern='y-mm-dd')
        self.date_reception_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row1, text="Mode:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        self.mode_entry = ttk.Entry(form_row1, width=12)
        self.mode_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row1, text="Fournisseur:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        self.fournisseur_combo = AutocompleteCombobox(form_row1, width=15)
        self.fournisseur_combo.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row1, text="Paiement:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        self.payement_entry = ttk.Entry(form_row1, width=12)
        self.payement_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row1, text="Transport:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        self.transport_entry = ttk.Entry(form_row1, width=12)
        self.transport_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row1, text="Adresse:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        self.adresse_entry = ttk.Entry(form_row1, width=20)
        self.adresse_entry.pack(side=tk.LEFT, padx=2)

        # Second row - Additional fields and buttons
        form_row2 = ttk.Frame(form_frame)
        form_row2.pack(fill=tk.X, padx=2, pady=2)

        ttk.Label(form_row2, text="N° BR:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(0,2))
        self.numero_entry = ttk.Entry(form_row2, width=12)
        self.numero_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row2, text="Statut:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        self.statut_entry = ttk.Entry(form_row2, width=12)
        self.statut_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row2, text="Remarque:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        self.remarque_entry = ttk.Entry(form_row2, width=30)
        self.remarque_entry.pack(side=tk.LEFT, padx=2)

        ttk.Label(form_row2, text="Utilisateur:", font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT, padx=(5,2))
        self.utilisateur_entry = ttk.Entry(form_row2, width=12)
        self.utilisateur_entry.pack(side=tk.LEFT, padx=2)

        # Buttons in the same row
        ttk.Separator(form_row2, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        btn_row = form_row2  # Use same row for buttons

        self.add_btn = ttk.Button(btn_row, text="Ajouter", width=15)
        self.add_btn.pack(side=tk.LEFT, padx=2)
        self.modify_btn = ttk.Button(btn_row, text="Modifier", width=15)
        self.modify_btn.pack(side=tk.LEFT, padx=2)
        self.delete_btn = ttk.Button(btn_row, text="Supprimer", width=15)
        self.delete_btn.pack(side=tk.LEFT, padx=2)
        self.reset_btn = ttk.Button(btn_row, text="Réinitialiser", width=15)
        self.reset_btn.pack(side=tk.LEFT, padx=2)

        # Tableau des commandes - Expanded columns
        table_frame = ttk.LabelFrame(self, text="Liste des commandes", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ref", "date_reception", "mode", "fournisseur", "payement", "transport", "adresse", "numero", "statut", "remarque", "utilisateur", "detail")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        # Style pour les en-têtes plus foncés
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('TkDefaultFont', 9, 'bold'), background='#4a4a4a', foreground='white')
        
        column_headers = ["Référence", "Date réception", "Mode", "Fournisseur", "Paiement", "Transport", "Adresse", "Numéro BR", "Statut", "Remarque", "Utilisateur", "Détail"]
        for col, text in zip(columns, column_headers):
            self.tree.heading(col, text=text)
        
        # Set column widths
        self.tree.column("ref", width=100)
        self.tree.column("date_reception", width=100)
        self.tree.column("mode", width=80)
        self.tree.column("fournisseur", width=120)
        self.tree.column("payement", width=80)
        self.tree.column("transport", width=80)
        self.tree.column("adresse", width=150)
        self.tree.column("numero", width=100)
        self.tree.column("statut", width=80)
        self.tree.column("remarque", width=150)
        self.tree.column("utilisateur", width=100)
        self.tree.column("detail", width=80, anchor="center")
        
        # Scrollbars
        tree_vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        tree_hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_vsb.set, xscrollcommand=tree_hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_vsb.grid(row=0, column=1, sticky="ns")
        tree_hsb.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.tree.bind("<Double-1>", self.open_detail_tab)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

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
            from models.schemas import SupplierSchema as SSchema
            fournisseurs_db = list(db.fournisseurs.find({}, {"_id": 0}))
            fournisseur_list = []
            
            print(f"DEBUG: Fournisseurs trouvés dans MongoDB: {fournisseurs_db}")
            
            for f in fournisseurs_db:
                # Use schema with backward compatibility
                nom = get_field_value(f, SSchema.NAME, "Nom", "nom", "name", "Name", "ID", "id")
                
                if nom:
                    fournisseur_list.append(nom)
            
            self.fournisseurs = fournisseur_list
            
            # Update the main combobox if it exists
            if hasattr(self, "fournisseur_combo") and self.fournisseur_combo.winfo_exists():
                self.fournisseur_combo.set_values(self.fournisseurs)
        except Exception as e:
            self.fournisseurs = []

    def refresh_tree(self):
        """Rafraîchit l'arbre principal (appelé depuis le contrôleur)"""
        if self.controller:
            self.controller.refresh_tree()

    def on_tree_select(self, event):
        """Called when a row is selected in the tree"""
        selected = self.tree.selection()
        if not selected:
            return
        
        item = selected[0]
        values = self.tree.item(item, "values")
        
        # Fill the form fields with selected row data
        self.ref_entry.delete(0, tk.END)
        self.ref_entry.insert(0, values[0])
        
        self.date_reception_entry.set_date(values[1] if values[1] else datetime.now())
        
        self.mode_entry.delete(0, tk.END)
        self.mode_entry.insert(0, values[2])
        
        self.fournisseur_combo.set(values[3])
        
        self.payement_entry.delete(0, tk.END)
        self.payement_entry.insert(0, values[4])
        
        self.transport_entry.delete(0, tk.END)
        self.transport_entry.insert(0, values[5])
        
        self.adresse_entry.delete(0, tk.END)
        self.adresse_entry.insert(0, values[6])
        
        self.numero_entry.delete(0, tk.END)
        self.numero_entry.insert(0, values[7])
        
        self.statut_entry.delete(0, tk.END)
        self.statut_entry.insert(0, values[8])
        
        self.remarque_entry.delete(0, tk.END)
        self.remarque_entry.insert(0, values[9])
        
        self.utilisateur_entry.delete(0, tk.END)
        self.utilisateur_entry.insert(0, values[10])

    # Removed _create_info_commande_section - no longer needed as info is in main grid

    def open_detail_tab(self, event):
        """Ouvre l'onglet détail pour une commande sélectionnée"""
        selected = self.tree.selection()
        if not selected:
            return
            
        item = selected[0]
        region = self.tree.identify_column(event.x)
        # Check if clicked on "Détail" column (now column #12 with the expanded structure)
        if region != "#12":
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
            from models.schemas import ArticleSchema as ASchema
            articles_db = list(db.articles.find({}, {"_id": 0}))
            
            mp_codes = []
            add_codes = []
            code_to_designation = {}
            
            for article in articles_db:
                # Use schema constants with backward compatibility
                code = get_field_value(article, ASchema.CODE, "code", "Code").strip()
                designation = get_field_value(article, ASchema.DESIGNATION, "designation", "Designation").strip()
                type_art = get_field_value(article, ASchema.TYPE, "type", "Type").strip().lower()
                
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

        def load_product_to_form():
            """Load selected product into form fields for editing"""
            selected = product_tree.selection()
            if not selected:
                messagebox.showwarning("Sélection", "Sélectionnez une ligne à charger.")
                return
                
            item = selected[0]
            values = product_tree.item(item, "values")
            
            # Fill the form with selected product data
            for i, field in enumerate(prod_fields):
                if field in prod_form_entries:
                    entry = prod_form_entries[field]
                    if hasattr(entry, 'delete'):
                        entry.delete(0, tk.END)
                        entry.insert(0, values[i] if i < len(values) else "")
        
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

        # Bind double-click to load product into form
        product_tree.bind("<Double-1>", lambda e: load_product_to_form())
        
        # Placer les boutons à côté du champ TVA dans le formulaire produit
        # Chercher l'index du champ TVA
        tva_index = None
        for i, field in enumerate(prod_fields):
            if field == "TVA":
                tva_index = i
                break
        if tva_index is not None:
            btn_col = tva_index + 1
            ttk.Button(prod_form_frame, text="Charger", command=load_product_to_form, width=12).grid(row=1, column=btn_col, padx=1)
            ttk.Button(prod_form_frame, text="Ajouter", command=insert_product_row, width=12).grid(row=1, column=btn_col+1, padx=1)
            ttk.Button(prod_form_frame, text="Modifier", command=modify_product_row, width=12).grid(row=1, column=btn_col+2, padx=1)
            ttk.Button(prod_form_frame, text="Supprimer", command=delete_product_row, width=12).grid(row=1, column=btn_col+3, padx=1)

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