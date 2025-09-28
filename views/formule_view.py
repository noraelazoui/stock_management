import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.formule import Formule, Composante
from controllers.formule_controller import FormuleController


class FormuleView(ttk.Frame):
    def __init__(self, parent, articles=None):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        
        # Initialisation des attributs
        self.controller = FormuleController()
        self.articles = articles if articles else []
        self.current_formule = None
        self.selected_composante_index = None
        self.copie_mode = False
        
        # Variables Tkinter
        self.code_var = tk.StringVar(value="")
        self.recette_code_var = tk.StringVar(value=self.generate_recette_code())
        self.detail_type_var = tk.StringVar(value="article")
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.date_mode = tk.BooleanVar(value=True)
        
        # Création de l'interface
        self.create_widgets()

    def generate_code(self):
        """Génère un code unique pour la formule"""
        from models.formule import Formule
        codes = [f.code for f in Formule.all()]
        i = 1
        while True:
            code = f"F{i:03d}"
            if code not in codes:
                return code
            i += 1

    def generate_recette_code(self):
        """Génère un code unique pour la recette"""
        from models.formule import Formule
        recettes = [getattr(f, "recette_code", None) for f in Formule.all() if hasattr(f, "recette_code")]
        i = 1
        while True:
            code = f"R{i:03d}"
            if code not in recettes:
                return code
            i += 1

    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        self.create_form_frame()
        self.create_table_frame()
        self.create_detail_notebook()
        self.refresh_table()

    def create_form_frame(self):
        """Crée le formulaire de saisie des formules"""
        form_frame = ttk.LabelFrame(self, text="Nouvelle formule", padding=15)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Configuration des colonnes
        for i in range(13):
            form_frame.columnconfigure(i, weight=1)

        # Champs du formulaire
        self.create_form_fields(form_frame)

    def create_form_fields(self, parent):
        """Crée les champs du formulaire"""
        row = 0
        # Code
        code_frame = ttk.Frame(parent)
        ttk.Label(code_frame, text="Code :").pack(side=tk.LEFT)
        self.code_entry = ttk.Entry(code_frame, textvariable=self.code_var, width=15)
        self.code_entry.pack(side=tk.LEFT)
        code_frame.grid(row=row, column=0, sticky="w")

        # Recette
        recette_frame = ttk.Frame(parent)
        ttk.Label(recette_frame, text="Recette :").pack(side=tk.LEFT)
        self.recette_code_entry = ttk.Entry(recette_frame, textvariable=self.recette_code_var, width=15, state="readonly")
        self.recette_code_entry.pack(side=tk.LEFT)
        recette_frame.grid(row=row, column=1, sticky="w")

        # Optim
        optim_frame = ttk.Frame(parent)
        ttk.Label(optim_frame, text="Optim :").pack(side=tk.LEFT)
        self.optim_entry = ttk.Entry(optim_frame, width=15)
        self.optim_entry.pack(side=tk.LEFT)
        optim_frame.grid(row=row, column=2, sticky="w")

        # Désignation
        designation_frame = ttk.Frame(parent)
        ttk.Label(designation_frame, text="Désignation :").pack(side=tk.LEFT)
        self.designation_entry = ttk.Entry(designation_frame, width=15)
        self.designation_entry.pack(side=tk.LEFT)
        designation_frame.grid(row=row, column=3, sticky="w")

        # Description
        desc_frame = ttk.Frame(parent)
        ttk.Label(desc_frame, text="Description :").pack(side=tk.LEFT)
        self.desc_entry = ttk.Entry(desc_frame, width=15)
        self.desc_entry.pack(side=tk.LEFT)
        desc_frame.grid(row=row, column=4, sticky="w")

        # Date création
        from tkcalendar import DateEntry
        date_frame = ttk.Frame(parent)
        ttk.Label(date_frame, text="Date création :").pack(side=tk.LEFT)
        self.date_entry = DateEntry(date_frame, textvariable=self.date_var, width=15, date_pattern='y-mm-dd')
        self.date_entry.pack(side=tk.LEFT)
        # Boutons à côté du champ date
        ttk.Button(date_frame, text="Ajouter", command=self.ajouter_formule, width=10).pack(side=tk.LEFT)
        ttk.Button(date_frame, text="Modifier", command=self.modifier_formule, width=10).pack(side=tk.LEFT)
        ttk.Button(date_frame, text="Copier", command=self.copier_formule, width=10).pack(side=tk.LEFT)
        ttk.Button(date_frame, text="Supprimer", command=self.supprimer_formule, width=10).pack(side=tk.LEFT)
        date_frame.grid(row=row, column=5, sticky="w")

    def create_table_frame(self):
        """Crée le tableau des formules"""
        table_frame = ttk.LabelFrame(self, text="Formules", padding=15)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Création du tableau
        self.create_formule_table(table_frame)
        
        # Boutons d'action
        self.create_table_buttons(table_frame)

    def create_formule_table(self, parent):
        """Crée le tableau des formules avec scrollbars"""
        columns = ("code", "optim", "designation", "description", "date", "type", "nb_composantes", "detail", "generer_recette")
        
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.formule_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="extended")
        
        # Configuration des colonnes
        headers = ["Code", "Optim", "Désignation", "Description", "Date création", "Type", "Nb composantes", "Détail", "Générer recette"]
        widths = [80, 100, 180, 200, 140, 80, 120, 80, 120]
        
        for col, txt, w in zip(columns, headers, widths):
            self.formule_tree.heading(col, text=txt)
            self.formule_tree.column(col, width=w, anchor="center")
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.formule_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.formule_tree.xview)
        self.formule_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Placement
        self.formule_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Events
        self.formule_tree.bind("<Button-1>", self.on_detail_click)

    def create_table_buttons(self, parent):
        """Crée les boutons du tableau"""
        # Les boutons sont maintenant à côté du champ Date création

    def create_detail_notebook(self):
        """Crée le notebook pour les détails des formules"""
        self.detail_notebook = ttk.Notebook(self)
        self.detail_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ==================== MÉTHODES DE GESTION DES FORMULES ====================

    def toggle_date_mode(self):
        """Bascule entre mode automatique et manuel pour la date"""
        if self.date_mode.get():
            self.date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M"))
            self.date_entry.config(state="readonly")
        else:
            self.date_entry.config(state="normal")

    def ajouter_formule(self):
        """Ajoute une nouvelle formule"""
        if not self.validate_formule_form():
            return
            
        code = self.code_var.get()
        optim = self.optim_entry.get().strip()
        designation = self.designation_entry.get().strip()
        description = self.desc_entry.get().strip()
        date = self.date_var.get().strip()
        recette_code = self.recette_code_var.get()
        quantity = 0  # À adapter si champ quantité

        # Récupérer les valeurs du formulaire
        code = self.code_var.get()
        optim = self.optim_entry.get()
        designation = self.designation_entry.get()
        description = self.desc_entry.get()
        date_creation = self.date_var.get()
        recette_code = self.recette_code_var.get()
        quantity = 0  # À adapter si champ quantité

        # Récupérer les composantes saisies (exemple: depuis un tableau ou une liste)
        composantes = []
        if hasattr(self, 'composante_list'):
            for c in self.composante_list:
                composantes.append(c)
        # Sinon, à adapter selon votre logique d'UI

        # Créer la formule
        # Détermine le type de formule en fonction du type sélectionné (Premix/Usine)
        type_formule = "simple"  # Par défaut, toutes les formules sont simples
        formule = Formule(
            code=code,
            optim=optim,
            designation=designation,
            description=description,
            date_creation=date_creation,
            composantes=composantes,
            quantity=quantity,
            recette_code=recette_code,
            type_formule=type_formule
        )
        self.controller.ajouter_formule(formule)
        self.refresh_table()
        self.reset_formule_form()  # Réinitialise le formulaire après ajout
        messagebox.showinfo("Succès", "Formule enregistrée avec ses composantes.")

    def modifier_formule(self):
        """Modifie la formule sélectionnée"""
        selected = self.formule_tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une formule à modifier.")
            return
            
        formule = self.get_selected_formule(selected[0])
        if not formule:
            return
            
        self.populate_form_with_formule(formule)
        self.controller.supprimer_formule(formule.code)
        self.refresh_table()
        
        messagebox.showinfo("Succès", "Formule modifiée. Cliquez sur Ajouter pour enregistrer les modifications.")

    def copier_formule(self):
        """Copie la formule sélectionnée"""
        selected = self.formule_tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une formule à copier.")
            return
            
        formule = self.get_selected_formule(selected[0])
        if not formule:
            return
            
        self.populate_form_for_copy(formule)
        self.copie_mode = True
        
        messagebox.showinfo("Succès", "Formule copiée avec ses composantes. Cliquez sur Ajouter pour enregistrer la nouvelle formule.")

    def supprimer_formule(self):
        """Supprime les formules sélectionnées"""
        selected = self.formule_tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une ou plusieurs formules à supprimer.")
            return
            
        if not messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer les formules sélectionnées ?"):
            return
            
        codes_to_delete = []
        for item_id in selected:
            values = self.formule_tree.item(item_id, "values")
            codes_to_delete.append(values[0])
            
        for code in codes_to_delete:
            self.controller.supprimer_formule(code)
            
        self.refresh_table()
        messagebox.showinfo("Succès", "Formules supprimées avec succès !")

    # ==================== MÉTHODES DE GESTION DES COMPOSANTES ====================

    def on_detail_click(self, event):
        """Gère le clic sur la colonne détail"""
        if not self.is_detail_column_clicked(event):
            return
            
        item_id = self.formule_tree.identify_row(event.y)
        if not item_id:
            return
            
        values = self.formule_tree.item(item_id, "values")
        code, optim = values[0], values[1]
        
        formule = self.find_formule_by_code_optim(code, optim)
        if formule:
            # Sélectionne le bouton radio 'article' par défaut
            if hasattr(self, 'radio_article'):
                self.detail_type_var.set('article')
                self.radio_article.invoke()
            self.refresh_detail_tab(formule)

    def refresh_detail_tab(self, formule):
        """Rafraîchit l'onglet de détail pour une formule"""
        # Supprimer tous les onglets existants
        for tab_id in self.detail_notebook.tabs():
            self.detail_notebook.forget(tab_id)
            
        if not formule:
            return
            
        self.current_formule = formule
        self.selected_composante_index = None
        
        # Créer le nouvel onglet
        tab = ttk.Frame(self.detail_notebook)
        self.detail_notebook.add(tab, text=f"Composantes {formule.code}")
        
        self.create_composante_form(tab, formule)
        self.create_composante_table(tab)
        self.create_total_frame(tab, formule)
        
        self.refresh_compo_table()
        self.update_optim_formule_combo()  # NOUVEAU : Remplir le combo optim formule
        self.detail_notebook.select(tab)

    def create_composante_form(self, parent, formule):
        """Crée le formulaire des composantes"""
        form_compo_frame = ttk.LabelFrame(parent, text="Ajouter/Modifier une composante", padding=10)
        form_compo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.create_optim_recette_fields(form_compo_frame, formule)
        self.create_type_selection_fields(form_compo_frame)
        self.create_composante_input_fields(form_compo_frame)
        self.create_pourcentage_info(form_compo_frame)
    # Les boutons de composante sont créés dans create_form_fields, donc on ne les recrée pas ici

    def create_optim_recette_fields(self, parent, formule):
        """Crée les champs optim et recette"""
        # Optim
        ttk.Label(parent, text="Optim :").grid(row=0, column=0, padx=5, pady=5)
        self.compo_optim_var = tk.StringVar()
        
        formules_same_code = self.controller.get_formule(formule.code)
        optim_values = list({f.optim for f in formules_same_code if f.optim})
        
        self.compo_optim_combo = ttk.Combobox(parent, textvariable=self.compo_optim_var, 
                                             values=optim_values, state="readonly", width=15)
        self.compo_optim_combo.grid(row=0, column=1, padx=5, pady=5)
        
        if formule.optim:
            self.compo_optim_combo.set(formule.optim)
        elif optim_values:
            self.compo_optim_combo.set(optim_values[0])

        # Recette liée
        ttk.Label(parent, text="Recette liée :").grid(row=0, column=2, padx=5, pady=5)
        self.compo_recette_var = tk.StringVar(value=getattr(formule, "recette_code", ""))
        self.compo_recette_entry = ttk.Entry(parent, textvariable=self.compo_recette_var, 
                                           state="readonly", width=15)
        self.compo_recette_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Synchronisation optim-recette
        self.compo_optim_combo.bind("<<ComboboxSelected>>", 
                                   lambda e: self.update_recette_for_optim(formules_same_code))

    def create_type_selection_fields(self, parent):
        """Crée les boutons radio pour le type (Article/Formule)"""
        # Regroupement des radio-boutons dans un Frame
        radio_frame = ttk.Frame(parent)
        self.radio_article = ttk.Radiobutton(radio_frame, text="Article", variable=self.detail_type_var, 
                                            value="article", command=self.on_detail_type_change)
        self.radio_formule = ttk.Radiobutton(radio_frame, text="Formule", variable=self.detail_type_var, 
                                            value="formule", command=self.on_detail_type_change)
        self.radio_article.pack(side=tk.LEFT, padx=0)
        self.radio_formule.pack(side=tk.LEFT, padx=0)
        radio_frame.grid(row=0, column=4, columnspan=2, padx=0, pady=5, sticky="w")

    def create_composante_input_fields(self, parent):
        """Crée les champs de saisie des composantes"""
        # Label article/formule
        self.compo_type_label = ttk.Label(parent, text="Article :")
        self.compo_type_label.grid(row=1, column=0, padx=5, pady=(15,5))

        # Combobox article
        self.compo_article_var = tk.StringVar()
        self.compo_article_combo = ttk.Combobox(parent, textvariable=self.compo_article_var, state="normal", width=15)
        self.compo_article_combo.grid(row=1, column=1, padx=5, pady=(15,5))
        self.update_article_combo_values()

        # Combobox formule
        self.compo_formule_var = tk.StringVar()
        self.compo_formule_combo = ttk.Combobox(parent, textvariable=self.compo_formule_var, state="readonly", width=15)
        self.update_formule_combo_values()
        # Ajoute le binding pour mettre à jour les optim quand la formule change
        self.compo_formule_combo.bind("<<ComboboxSelected>>", lambda e: self.update_optim_formule_combo_for_selected_formule())

        # NOUVEAU : Optim Formule (pour les composantes)
        self.compo_optim_formule_label = ttk.Label(parent, text="Optim Formule :")
        self.compo_optim_formule_label.grid(row=1, column=2, padx=5, pady=(15,5))
        self.compo_optim_formule_var = tk.StringVar()
        self.compo_optim_formule_combo = ttk.Combobox(parent, textvariable=self.compo_optim_formule_var, state="readonly", width=15)
        self.compo_optim_formule_combo.grid(row=1, column=3, padx=5, pady=(15,5))
        self.compo_optim_formule_combo.bind("<<ComboboxSelected>>", self.update_recette_formule_for_composante)

        # NOUVEAU : Recette Formule (affichage automatique)
        self.compo_recette_formule_label = ttk.Label(parent, text="Recette Formule :")
        self.compo_recette_formule_label.grid(row=1, column=4, padx=5, pady=(15,5))
        self.compo_recette_formule_var = tk.StringVar()
        self.compo_recette_formule_entry = ttk.Entry(parent, textvariable=self.compo_recette_formule_var, state="readonly", width=15)
        self.compo_recette_formule_entry.grid(row=1, column=5, padx=5, pady=(15,5))


        # Validation pour n'accepter que des chiffres (float) pour le pourcentage
        def validate_float(P):
            if P == "":
                return True
            try:
                float(P)
                return True
            except ValueError:
                return False
        vcmd_float = (parent.register(validate_float), '%P')

        ttk.Label(parent, text="Pourcentage :").grid(row=1, column=6, padx=5, pady=(15,5))
        self.compo_pourcentage_entry = ttk.Entry(parent, width=15, validate="key", validatecommand=vcmd_float)
        self.compo_pourcentage_entry.grid(row=1, column=7, padx=5, pady=(15,5))
        self.compo_pourcentage_entry.bind('<KeyRelease>', self.update_pourcentage_info)

        # Boutons de gestion des composantes à côté du champ pourcentage
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=1, column=8, padx=5, pady=(15,5), sticky="w")
        buttons = [
            ("Ajouter composante", self.ajouter_composante),
            ("Modifier composante", self.modifier_composante),
            ("Copier composante", self.copier_composante),
            ("Supprimer composante", self.supprimer_composante),
            ("Annuler", self.annuler_composante)
        ]
        for text, command in buttons:
            ttk.Button(btn_frame, text=text, command=command, width=15).pack(side=tk.LEFT, padx=2)

    def on_detail_type_change(self):
        """Gère le changement de type de composante (Article/Formule)"""
        # Masquer tous les combos
        self.hide_all_combos()
        
        # Mettre à jour le label
        if self.detail_type_var.get() == "formule":
            self.compo_type_label.config(text="Formule :")
            self.update_formule_combo_values()
            self.compo_formule_combo.grid(row=1, column=1, padx=5, pady=(15,5))
            self.update_optim_formule_combo_for_selected_formule()
        else:
            self.compo_type_label.config(text="Article :")
            self.update_article_combo_values()
            if hasattr(self, 'compo_article_combo'):
                self.compo_article_combo.grid(row=1, column=1, padx=5, pady=(15,5))
            self.compo_optim_formule_combo['values'] = []
            self.compo_optim_formule_var.set("")

    def update_optim_formule_combo_for_selected_formule(self):
        """Met à jour le combobox des optim selon la formule sélectionnée dans le combobox formule, uniquement pour les formules validées"""
        formule_selected = self.compo_formule_var.get()
        if not formule_selected or formule_selected == "Rechercher" or formule_selected.startswith('---'):
            self.compo_optim_formule_combo['values'] = []
            self.compo_optim_formule_var.set("")
            return

        # Extraire le code de la formule si au format "code - designation"
        formule_code = formule_selected.split(" - ")[0] if " - " in formule_selected else formule_selected

        # Récupérer tous les optims pour ce code de formule (tous, pas seulement validés)
        from models.formule import Formule
        all_formules = Formule.all()
        optim_values = sorted({f.optim for f in all_formules if f.code == formule_code and f.optim})
        self.compo_optim_formule_combo['values'] = optim_values
        if optim_values:
            self.compo_optim_formule_var.set(optim_values[0])
        else:
            self.compo_optim_formule_var.set("")

    # Les boutons sont maintenant créés dans create_form_fields à côté du champ pourcentage

    def create_composante_table(self, parent):
        """Crée le tableau des composantes"""
        table_compo_frame = ttk.LabelFrame(parent, text="Composantes de la formule", padding=10)
        table_compo_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("article", "pourcentage", "optim_formule", "recette_formule")
        headers = ["Article", "%", "Optim formule", "Recette formule"]
        widths = [180, 80, 100, 120]
        
        tree_frame = ttk.Frame(table_compo_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.compo_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        for col, txt, w in zip(columns, headers, widths):
            self.compo_tree.heading(col, text=txt)
            self.compo_tree.column(col, width=w, anchor="center" if col != "article" else "w")
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.compo_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.compo_tree.xview)
        self.compo_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.compo_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.compo_tree.bind("<<TreeviewSelect>>", self.on_composante_select)
        
        
    def create_total_frame(self, parent, formule):
        """Crée le cadre d'affichage du total"""
        total_frame = ttk.Frame(parent)
        total_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(total_frame, text=f"Nombre de composantes : {len(formule.composantes)}").pack(side=tk.LEFT)
        
        # Calculer le total pour déterminer la couleur
        total = formule.total_pourcentage()
        nb_composantes = len(formule.composantes)
        
        # Déterminer la couleur
        color = "black"
        if nb_composantes > 0:
            if abs(total - 100) < 0.01:
                color = "green"
            else:
                color = "red"
        
        self.total_label = ttk.Label(total_frame, text=f"Total: {total:.4f}%", foreground=color)
        self.total_label.pack(side=tk.RIGHT)

    def create_pourcentage_info(self, parent):
        """Crée l'affichage des informations de pourcentage"""
        self.pourcentage_info_var = tk.StringVar(value="Pourcentage saisi : 0.0000 | Somme : 0.0000")
        self.pourcentage_info_label = ttk.Label(parent, textvariable=self.pourcentage_info_var, foreground="blue")
        self.pourcentage_info_label.grid(row=4, column=0, columnspan=8, sticky="w", padx=5, pady=2)

    # ==================== MÉTHODES DE GESTION DU TYPE DE COMPOSANTE ====================

    def on_detail_type_change(self):
        """Gère le changement de type de composante (Article/Formule)"""
        # Masquer tous les combos
        self.hide_all_combos()

        # Always clear pourcentage and recette fields when switching type
        if hasattr(self, 'compo_pourcentage_entry'):
            self.compo_pourcentage_entry.delete(0, tk.END)
        if hasattr(self, 'compo_recette_formule_var'):
            self.compo_recette_formule_var.set("")
        if hasattr(self, 'compo_optim_formule_var'):
            self.compo_optim_formule_var.set("")

        # Hide/show Recette and Optim fields and labels depending on type
        if self.detail_type_var.get() == "formule":
            self.compo_type_label.config(text="Formule :")
            self.update_formule_combo_values()
            self.compo_formule_combo.grid(row=1, column=1, padx=5, pady=(15,5))
            self.update_optim_formule_combo_for_selected_formule()
            # Show Optim/Recette widgets and labels
            if hasattr(self, 'compo_optim_formule_label'):
                self.compo_optim_formule_label.grid(row=1, column=2, padx=5, pady=(15,5))
            if hasattr(self, 'compo_optim_formule_combo'):
                self.compo_optim_formule_combo.grid(row=1, column=3, padx=5, pady=(15,5))
            if hasattr(self, 'compo_recette_formule_label'):
                self.compo_recette_formule_label.grid(row=1, column=4, padx=5, pady=5)
            if hasattr(self, 'compo_recette_formule_entry'):
                self.compo_recette_formule_entry.grid(row=1, column=5, padx=5, pady=5)
        else:
            self.compo_type_label.config(text="Article :")
            self.update_article_combo_values()
            self.compo_article_combo.grid(row=1, column=1, padx=5, pady=(15,5))
            # Hide Optim/Recette widgets and labels for article
            if hasattr(self, 'compo_optim_formule_label'):
                self.compo_optim_formule_label.grid_remove()
            if hasattr(self, 'compo_optim_formule_combo'):
                self.compo_optim_formule_combo.grid_remove()
            if hasattr(self, 'compo_recette_formule_label'):
                self.compo_recette_formule_label.grid_remove()
            if hasattr(self, 'compo_recette_formule_entry'):
                self.compo_recette_formule_entry.grid_remove()

    def hide_all_combos(self):
        """Masque tous les comboboxes de sélection"""
        try:
            self.compo_article_combo.grid_remove()
        except (AttributeError, tk.TclError):
            pass
        try:
            self.compo_formule_combo.grid_remove()
        except (AttributeError, tk.TclError):
            pass

    def update_article_combo_values(self):
        """Met à jour le combobox articles avec groupes simulés et recherche dynamique"""
        if hasattr(self, 'compo_article_combo'):
            from models.database import db
            # Aggregate all DEM/product lines for all articles from commandes
            all_commandes = list(db.commandes.find({}))
            seen = set()
            values = []
            for cmd in all_commandes:
                for prod in cmd.get('produits', []):
                    code = prod.get('code', '')
                    if code and code not in seen:
                        values.append(code)
                        seen.add(code)
            values.sort()
            self.compo_article_combo['values'] = values
            self.compo_article_combo.set("")
            # Recherche dynamique
            def on_keyrelease(event):
                typed = self.compo_article_combo.get().lower()
                filtered = [v for v in values if typed in v.lower()]
                self.compo_article_combo['values'] = filtered if typed else values
                if filtered:
                    self.compo_article_combo.event_generate('<Down>')
            self.compo_article_combo.bind('<KeyRelease>', on_keyrelease)

    def update_formule_combo_values(self):
        """Met à jour le combobox formules pour permettre la recherche et la saisie libre, avec organisation par type et titres non sélectionnables."""
        if hasattr(self, 'compo_formule_combo'):
            # Utilise le controller pour séparer les formules
            types_dict = self.controller.lister_formules_par_type()
            
            # Formules simples avec leur désignation et type réel
            simples = types_dict['simples']
            simples_formatted = [f"{f.code} - {f.designation} [{f.type_formule.capitalize()}]" for f in simples if f.valider()]
            
            # Formules mixtes avec leur désignation et type réel également
            mixtes = types_dict['mixtes']
            mixtes_formatted = [f"{f.code} - {f.designation} [{f.type_formule.capitalize()}]" for f in mixtes if f.valider()]
            
            # Organisation sans titres
            values_with_titles = ['Rechercher']
            
            # Ajoute les formules simples
            if simples_formatted:
                values_with_titles.extend(simples_formatted)
                
            # Ajoute les formules mixtes
            if mixtes_formatted:
                values_with_titles.extend(mixtes_formatted)
                
            # Permettre la saisie libre
            self.compo_formule_combo.config(state="normal")
            self.compo_formule_combo['values'] = values_with_titles
            self.compo_formule_combo.set(values_with_titles[0] if values_with_titles else "")
            # Empêcher la sélection des titres et mettre à jour le combo optim
            def on_select(event):
                value = self.compo_formule_combo.get()
                if value == 'Rechercher':
                    self.compo_formule_combo.set("")
                else:
                    # Extraire le code de la formule (avant le " - " s'il existe)
                    formule_code = value.split(" - ")[0] if " - " in value else value
                    
                    # Mettre à jour les options liées à la formule sélectionnée
                    self.update_optim_formule_combo_for_selected_formule()
                    
                    # Met à jour la recette liée automatiquement si on trouve la formule
                    from models.formule import Formule
                    formules = [f for f in Formule.all() if f.code == formule_code]
                    if formules:
                        recette = formules[0].recette_code if hasattr(formules[0], 'recette_code') else ""
                        if hasattr(self, 'compo_recette_formule_var'):
                            self.compo_recette_formule_var.set(recette)
            self.compo_formule_combo.bind('<<ComboboxSelected>>', on_select)
            
            # Ajouter une fonctionnalité de recherche pendant la saisie
            def on_keyrelease(event):
                # Obtenir la valeur saisie
                value = event.widget.get()
                
                # Si la valeur est vide, remettre toutes les options
                if not value or value == "Rechercher":
                    self.compo_formule_combo['values'] = values_with_titles
                else:
                    # Sinon, filtrer les options qui contiennent la valeur saisie (ignorer la casse)
                    filtered = [item for item in values_with_titles if value.lower() in item.lower()]
                    if filtered:
                        event.widget['values'] = filtered
                        # Montrer la liste déroulante
                        self.compo_formule_combo.event_generate('<Down>')
            
            self.compo_formule_combo.bind('<KeyRelease>', on_keyrelease)
            
    def update_optim_formule_combo(self):
        """Met à jour les valeurs du combobox optim formule"""
        if not hasattr(self, 'compo_optim_formule_combo') or not self.current_formule:
            return
        
        # Récupère tous les optims pour toutes les formules (pas seulement la courante)
        from models.formule import Formule
        all_formules = Formule.all()
        optims = list({f.optim for f in all_formules if f.optim})
        
        self.compo_optim_formule_combo['values'] = optims

    def update_recette_formule_for_composante(self, event=None):
        """Met à jour la recette formule selon l'optim sélectionné pour les composantes"""
        if not hasattr(self, 'compo_optim_formule_var') or not hasattr(self, 'compo_recette_formule_var'):
            return
            
        selected_optim = self.compo_optim_formule_var.get()
        recette = ""

        # Récupérer le code de la formule sélectionnée
        formule_selected = self.compo_formule_var.get() if hasattr(self, 'compo_formule_var') else ""
        formule_code = formule_selected.split(" - ")[0] if " - " in formule_selected else formule_selected

        # Cherche la recette correspondant à la formule ET à l'optim
        from models.formule import Formule
        all_formules = Formule.all()
        for f in all_formules:
            if f.code == formule_code and f.optim == selected_optim:
                recette = getattr(f, "recette_code", "")
                break

        self.compo_recette_formule_var.set(recette)

    # ==================== MÉTHODES DE GESTION DES COMPOSANTES ====================

    def ajouter_composante(self):
        """Ajoute une composante à la formule courante"""
        if not self.current_formule:
            return
            
        composante_data = self.get_composante_from_form()
        if not composante_data:
            return
            
        designation, pourcentage, unite, optim_formule, recette_formule = composante_data
        
        if not self.validate_composante(designation, pourcentage):
            return
            
        # Créer la composante avec les nouvelles données
        composante = Composante(designation, pourcentage, unite)
        composante.optim_formule = optim_formule  # NOUVEAU
        composante.recette_formule = recette_formule  # NOUVEAU
        
        self.current_formule.ajouter_composante(composante)
        self.current_formule.save()
        
        self.reset_composante_form()
        self.refresh_compo_table()
        self.refresh_table()
        self.calculer_total()
        
        messagebox.showinfo("Ajout", "Composante ajoutée à la formule et enregistrée dans la base de données.")

    def modifier_composante(self):
        """Modifie la composante sélectionnée"""
        if not self.current_formule or self.selected_composante_index is None:
            messagebox.showwarning("Sélection", "Sélectionnez une composante à modifier.")
            return
            
        composante_data = self.get_composante_from_form()
        if not composante_data:
            return
            
        designation, pourcentage, unite, optim_formule, recette_formule = composante_data
        
        if not self.validate_composante_modification(designation, pourcentage):
            return
            
        # Créer la composante avec les nouvelles données
        composante = Composante(designation, pourcentage, unite)
        composante.optim_formule = optim_formule  # NOUVEAU
        composante.recette_formule = recette_formule  # NOUVEAU
        
        self.current_formule.composantes[self.selected_composante_index] = composante
        self.current_formule.save()
        
        self.reset_composante_form()
        self.selected_composante_index = None
        self.refresh_compo_table()
        self.refresh_table()
        self.calculer_total()
        
        messagebox.showinfo("Modification", "Composante modifiée et enregistrée dans la base de données.")

    def copier_composante(self):
        """Copie la composante sélectionnée dans le formulaire"""
        if not self.current_formule or self.selected_composante_index is None:
            messagebox.showwarning("Sélection", "Sélectionnez une composante à copier.")
            return
            
        comp = self.current_formule.composantes[self.selected_composante_index]
        
        # Remplir le formulaire avec les données de la composante
        article = next((a for a in self.articles if a["code"] == comp.article or a["designation"] == comp.article), None)
        
        # Détermine le type selon la composante
        from models.formule import Formule
        formule_comp = next((f for f in Formule.all() if f.code == comp.article), None)
        
        if formule_comp:
            # C'est une formule
            self.detail_type_var.set("formule")
            self.compo_formule_combo.set(comp.article)
        elif article:
            # C'est un article
            self.detail_type_var.set("article")
            self.compo_article_combo.set(f"{article['code']} - {article['designation']}")
        else:
            # Article non trouvé, affiche tel quel
            self.detail_type_var.set("article")
            self.compo_article_combo.set(comp.article)
        
        self.on_detail_type_change()
            
        # Copier le pourcentage
        self.compo_pourcentage_entry.delete(0, tk.END)
        self.compo_pourcentage_entry.insert(0, comp.pourcentage)
        
        # Copier optim et recette formule si disponibles
        if hasattr(comp, 'optim_formule') and comp.optim_formule:
            self.compo_optim_formule_combo.set(comp.optim_formule)
            # Déclencher la mise à jour de la recette
            self.update_recette_formule_for_composante()
        
        messagebox.showinfo("Copie", "Composante copiée dans le formulaire. Modifiez les valeurs et cliquez sur Ajouter.")

    def supprimer_composante(self):
        """Supprime la composante sélectionnée"""
        if not self.current_formule or self.selected_composante_index is None:
            messagebox.showwarning("Sélection", "Sélectionnez une composante à supprimer.")
            return
            
        if not messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette composante?"):
            return
            
        self.current_formule.supprimer_composante(self.selected_composante_index)
        self.current_formule.save()
        
        self.reset_composante_form()
        self.selected_composante_index = None
        self.refresh_compo_table()
        self.refresh_table()
        self.calculer_total()
        
        messagebox.showinfo("Suppression", "Composante supprimée et enregistrée dans la base de données.")

    def annuler_composante(self):
        """Annule la saisie/modification de composante"""
        self.reset_composante_form()
        self.selected_composante_index = None

    def valider_formule(self):
        """Valide la formule (total = 100%)"""
        if not self.current_formule:
            return
            
        total = self.current_formule.total_pourcentage()
        if abs(total - 100) > 0.01:
            messagebox.showwarning("Erreur", f"Le total doit être exactement 100%. Total actuel: {total}%")
            return
            
        messagebox.showinfo("Succès", "Formule validée avec succès!")
        self.refresh_table()

    # ==================== MÉTHODES DE SÉLECTION ET EVENTS ====================

    def on_composante_select(self, event):
        """Gère la sélection d'une composante dans le tableau"""
        selected = self.compo_tree.selection()
        if not selected:
            self.selected_composante_index = None
            return
            
        item = selected[0]
        values = self.compo_tree.item(item, "values")
        
        # Récupérer toutes les valeurs du tableau
        article_code = values[0]
        pourcentage = values[1]
        optim_formule = values[2] if len(values) > 2 else ""
        recette_formule = values[3] if len(values) > 3 else ""
        
        # Déterminer le type (article ou formule) selon le code
        article = next((a for a in self.articles if a["code"] == article_code), None)
        
        if article:
            # C'est un article
            self.detail_type_var.set("article")
            self.compo_article_combo.set(f"{article['code']} - {article['designation']}")
        else:
            # Vérifier si c'est une formule
            from models.formule import Formule
            formule = next((f for f in Formule.all() if f.code == article_code), None)
            if formule:
                self.detail_type_var.set("formule")
                # Afficher le code et la désignation de la formule
                formule_display = f"{formule.code} - {formule.designation}" if formule.designation else formule.code
                self.compo_formule_combo.set(formule_display)
            else:
                # Code non trouvé, traiter comme article
                self.detail_type_var.set("article")
                self.compo_article_combo.set(article_code)
        
        self.on_detail_type_change()
        
        # Remplir les autres champs
        self.compo_pourcentage_entry.delete(0, tk.END)
        self.compo_pourcentage_entry.insert(0, pourcentage)
        
        # Remplir optim formule et recette formule
        if hasattr(self, 'compo_optim_formule_combo') and optim_formule:
            self.compo_optim_formule_combo.set(optim_formule)
        if hasattr(self, 'compo_recette_formule_var') and recette_formule:
            self.compo_recette_formule_var.set(recette_formule)
        print(f"Optim formule sélectionné : {optim_formule}")
        print(f"Recette formule sélectionnée : {recette_formule}")
       
        # Trouver l'index de la composante
        for i, comp in enumerate(self.current_formule.composantes):
            if comp.article == article_code and str(comp.pourcentage) == str(pourcentage):
                self.selected_composante_index = i
                break

    # ==================== MÉTHODES DE RAFRAÎCHISSEMENT ====================

    def refresh_table(self):
        """Rafraîchit le tableau des formules"""
        self.formule_tree.delete(*self.formule_tree.get_children())
        
        # Configuration des tags de couleur
        self.formule_tree.tag_configure('rouge', background='#FFB6C1')  # Rouge clair pour pourcentage < 100
        self.formule_tree.tag_configure('vert', background='#90EE90')   # Vert clair pour pourcentage = 100
        self.formule_tree.tag_configure('blanc', background='white')    # Blanc pour aucune composante
        
        from models.formule import Formule
        for f in Formule.all():
            nb_composantes = len(getattr(f, 'composantes', []))
            recette_code = getattr(f, 'recette_code', '')
            # Déterminer le type de formule
            type_formule = "simple"
            
            # Déterminer la couleur en fonction des composantes
            tag = 'with_composantes' if nb_composantes > 0 else 'no_composantes'
            for comp in getattr(f, 'composantes', []):
                # Si la composante n'a pas d'attribut 'article', c'est une formule (mixte)
                if not hasattr(comp, 'article') or comp.article is None:
                    type_formule = "mixte"
                    break
                # Si la composante a une recette_formule non vide, c'est aussi une formule (mixte)
                if hasattr(comp, 'recette_formule') and comp.recette_formule:
                    type_formule = "mixte"
                    break
                    
            # Déterminer la couleur en fonction du pourcentage total
            tag = self.get_formule_color_tag(f, nb_composantes)
                
            # Insérer la ligne avec la couleur appropriée
            item = self.formule_tree.insert('', 'end', values=(
                f.code,
                f.optim,
                f.designation,
                f.description,
                f.date_creation,
                type_formule,
                nb_composantes,
                "Détail",
                recette_code
            ), tags=(tag,))

    def refresh_compo_table(self):
        """Rafraîchit le tableau des composantes"""
        if not self.current_formule:
            return
            
        # Configuration des tags de couleur
        if hasattr(self, 'compo_tree'):
            self.compo_tree.tag_configure('rouge', background='#FFB6C1')  # Rouge clair pour pourcentage < 100
            self.compo_tree.tag_configure('vert', background='#90EE90')   # Vert clair pour pourcentage = 100
            self.compo_tree.tag_configure('blanc', background='white')    # Blanc pour aucune composante
        
        for i in self.compo_tree.get_children():
            self.compo_tree.delete(i)
            
        for comp in self.current_formule.composantes:
            # NOUVEAU : Afficher les vraies valeurs dans les colonnes
            optim_formule = getattr(comp, 'optim_formule', '')
            recette_formule = getattr(comp, 'recette_formule', '')
            
            # Calculer le total pour déterminer la couleur
            total = self.current_formule.total_pourcentage()
            nb_composantes = len(self.current_formule.composantes)
            
            # Déterminer le tag de couleur
            if nb_composantes == 0:
                tag = 'blanc'
            elif abs(total - 100) < 0.01:
                tag = 'vert'
            else:
                tag = 'rouge'
            
            self.compo_tree.insert("", "end", values=(
                comp.article,           # Code article OU code formule
                comp.pourcentage,       # Pourcentage
                optim_formule,         # Optim formule sélectionné
                recette_formule        # Recette formule correspondante
            ), tags=(tag,))
            
        self.calculer_total()

    def calculer_total(self):
        """Calcule et met à jour l'affichage du total des pourcentages"""
        if not self.current_formule:
            return
            
        total = self.current_formule.total_pourcentage()
        nb_composantes = len(self.current_formule.composantes)
        
        # Mettre à jour le label total avec la couleur appropriée
        if hasattr(self, 'total_label'):
            self.total_label.config(text=f"Total: {total:.4f}%")
            
            # Appliquer la couleur au label selon le pourcentage
            if nb_composantes == 0:
                self.total_label.config(foreground="black")
            elif abs(total - 100) < 0.01:
                self.total_label.config(foreground="green")
            else:
                self.total_label.config(foreground="red")
        
        # Mettre à jour le bouton valider
        if hasattr(self, 'valider_btn'):
            if abs(total - 100) < 0.01:
                self.valider_btn.config(state=tk.NORMAL, text="Valider (Total: 100%)")
            else:
                self.valider_btn.config(state=tk.DISABLED, text=f"Valider (Total: {total:.4f}%)")

    def update_pourcentage_info(self, event=None):
        """Met à jour l'affichage des informations de pourcentage"""
        try:
            val = float(self.compo_pourcentage_entry.get())
            val_str = f"{val:.4f}"
        except (ValueError, tk.TclError):
            val = 0.0
            val_str = "0.0000"
        
        total = sum([float(f"{c.pourcentage:.4f}") for c in self.current_formule.composantes]) if self.current_formule else 0
        total_with_input = total + val if val > 0 else total
        total_str = f"{total_with_input:.4f}"
        
        self.pourcentage_info_var.set(f"Pourcentage saisi : {val_str} | Somme : {total_str}")
        
        # Changer la couleur selon le total
        if total_with_input > 100:
            self.pourcentage_info_label.config(foreground="red")
        else:
            self.pourcentage_info_label.config(foreground="blue")

    def update_recette_for_optim(self, formules_same_code):
        """Met à jour la recette selon l'optim sélectionné"""
        selected_optim = self.compo_optim_var.get()
        recette = ""
        
        for f in formules_same_code:
            if f.optim == selected_optim:
                recette = getattr(f, "recette_code", "")
                break
                
        self.compo_recette_var.set(recette)

    # ==================== MÉTHODES UTILITAIRES ====================

    def validate_formule_form(self):
        """Valide les champs du formulaire de formule"""
        optim = self.optim_entry.get().strip()
        designation = self.designation_entry.get().strip()
        description = self.desc_entry.get().strip()
        
        if not optim or not designation or not description:
            messagebox.showwarning("Champs manquants", "Remplissez tous les champs.")
            return False
        return True

    def check_optim_exists(self, code, optim):
        """Vérifie si l'optim existe déjà pour ce code"""
        existing_formules = self.controller.get_formule(code)
        return any(f.optim == optim for f in existing_formules)

    def get_composantes_for_new_formule(self):
        """Récupère les composantes pour une nouvelle formule (mode copie)"""
        if (hasattr(self, 'copie_mode') and self.copie_mode and 
            self.current_formule and isinstance(self.current_formule, Formule)):
            return [Composante(c.article, c.pourcentage, c.unite) for c in self.current_formule.composantes]
        return []

    def get_selected_formule(self, item_id):
        """Récupère la formule sélectionnée"""
        values = self.formule_tree.item(item_id, "values")
        code = values[0]
        formules = self.controller.get_formule(code)
        
        if not formules or len(formules) == 0:
            messagebox.showerror("Erreur", "Formule introuvable.")
            return None
        return formules[0]

    def populate_form_with_formule(self, formule):
        """Remplit le formulaire avec les données d'une formule"""
        self.code_var.set(formule.code)
        self.optim_entry.delete(0, tk.END)
        self.optim_entry.insert(0, formule.optim)
        self.designation_entry.delete(0, tk.END)
        self.designation_entry.insert(0, formule.designation)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, formule.description)
        self.date_var.set(formule.date_creation)

    def populate_form_for_copy(self, formule):
        """Remplit le formulaire pour copier une formule"""
        self.code_var.set(self.generate_code())
        self.optim_entry.delete(0, tk.END)
        self.optim_entry.insert(0, formule.optim)
        self.designation_entry.delete(0, tk.END)
        self.designation_entry.insert(0, formule.designation)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, formule.description)
        self.date_var.set(datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        # Copier les composantes
        if hasattr(formule, 'composantes'):
            self.current_formule = Formule(
                self.code_var.get(),
                formule.optim,
                formule.designation,
                formule.description,
                self.date_var.get(),
                [Composante(c.article, c.pourcentage, c.unite) for c in formule.composantes]
            )

    def reset_formule_form(self):
        """Remet à zéro le formulaire de formule"""
        self.code_var.set(self.generate_code())
        self.recette_code_var.set(self.generate_recette_code())
        self.optim_entry.delete(0, tk.END)
        self.designation_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.current_formule = None
        self.copie_mode = False

    def reset_composante_form(self):
        """Remet à zéro le formulaire de composante"""
        if hasattr(self, 'compo_article_combo'):
            self.compo_article_combo.set("")
        if hasattr(self, 'compo_formule_combo'):
            self.compo_formule_combo.set("")
        if hasattr(self, 'compo_pourcentage_entry'):
            self.compo_pourcentage_entry.delete(0, tk.END)
        if hasattr(self, 'compo_optim_formule_combo'):
            self.compo_optim_formule_combo.set("")
        if hasattr(self, 'compo_recette_formule_var'):
            self.compo_recette_formule_var.set("")

    def get_composante_from_form(self):
        """Récupère les données de composante depuis le formulaire"""
        if self.detail_type_var.get() == "formule":
            designation_full = self.compo_formule_var.get()
            # Extraire le code de la formule si au format "code - designation"
            designation = designation_full.split(" - ")[0] if " - " in designation_full else designation_full
            unite = "-"  # Les formules n'ont pas d'unité
        else:
            designation_full = self.compo_article_combo.get()
            if not designation_full:
                return None
            
            code = designation_full.split(' - ')[0] if ' - ' in designation_full else designation_full
            article = next((a for a in self.articles if a["code"] == code), None)
            
            if article:
                designation = article["code"]  # MODIFIÉ : On stocke le CODE, pas la désignation
                unite = article["unite"]
            else:
                designation = designation_full
                unite = "-"
        
        pourcentage_str = self.compo_pourcentage_entry.get().strip()
        if not designation or not pourcentage_str:
            messagebox.showwarning("Champs manquants", "Sélectionnez un élément et entrez un pourcentage.")
            return None
            
        try:
            pourcentage = float(pourcentage_str)
        except ValueError:
            messagebox.showwarning("Format", "Le pourcentage doit être un nombre.")
            return None
        
        # NOUVEAU : Récupérer optim formule et recette formule
        optim_formule = ""
        recette_formule = ""
        if hasattr(self, 'compo_optim_formule_var'):
            optim_formule = self.compo_optim_formule_var.get()
        if hasattr(self, 'compo_recette_formule_var'):
            recette_formule = self.compo_recette_formule_var.get()
            
        return designation, pourcentage, unite, optim_formule, recette_formule

    def validate_composante(self, designation, pourcentage):
        """Valide les données d'une composante"""
        if pourcentage <= 0 or pourcentage > 100:
            messagebox.showwarning("Valeur", "Le pourcentage doit être entre 1 et 100.")
            return False
            
        total_actuel = self.current_formule.total_pourcentage()
        if total_actuel + pourcentage > 100:
            messagebox.showwarning("Erreur", f"Le total ne peut pas dépasser 100%. Total actuel: {total_actuel}%")
            return False
            
        return True

    def validate_composante_modification(self, designation, pourcentage):
        """Valide les données lors de la modification d'une composante"""
        if pourcentage <= 0 or pourcentage > 100:
            messagebox.showwarning("Valeur", "Le pourcentage doit être entre 1 et 100.")
            return False
            
        total_actuel = self.current_formule.total_pourcentage()
        ancien_pourcentage = self.current_formule.composantes[self.selected_composante_index].pourcentage
        
        if total_actuel - ancien_pourcentage + pourcentage > 100:
            messagebox.showwarning("Erreur", "Le total ne peut pas dépasser 100%.")
            return False
            
        return True

    def get_formule_color_tag(self, formule, nb_composantes):
        """Détermine la couleur d'affichage d'une formule selon son état"""
        if nb_composantes == 0:
            return 'blanc'
        
        total = formule.total_pourcentage() if nb_composantes > 0 else None
        if total is not None and abs(total - 100) < 0.01:
            return 'vert'
        else:
            return 'rouge'

    def is_detail_column_clicked(self, event):
        """Vérifie si le clic est sur la colonne détail"""
        region = self.formule_tree.identify("region", event.x, event.y)
        if region != "cell":
            return False
        col = self.formule_tree.identify_column(event.x)
        return col == "#8"  # Colonne détail (après ajout de la colonne 'type')

    def find_formule_by_code_optim(self, code, optim):
        """Trouve une formule par code et optim"""
        formules = self.controller.lister_formules()
        return next((f for f in formules if f.code == code and f.optim == optim), None)

    # ==================== MÉTHODES PUBLIQUES ====================

    def update_articles(self, articles):
        """Met à jour la liste des articles"""
        self.articles = articles
        
        # Mettre à jour les comboboxes d'articles dans tous les onglets
        self.update_article_combo_values()
        
        # Mettre à jour les onglets de détail ouverts
        for tab_id in self.detail_notebook.tabs():
            tab = self.detail_notebook.nametowidget(tab_id)
            self.update_tab_article_combo(tab, articles)

    def update_tab_article_combo(self, tab, articles):
        """Met à jour le combobox d'articles dans un onglet spécifique"""
        for child in tab.winfo_children():
            if isinstance(child, ttk.LabelFrame) and 'Ajouter/Modifier une composante' in child.cget('text'):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Combobox) and hasattr(widget, 'set'):
                        # Vérifier si c'est le combobox d'articles
                        try:
                            current_values = widget['values']
                            if current_values and ' - ' in str(current_values[0]):
                                widget['values'] = [f"{a['code']} - {a.get('designation', '')}" for a in articles]
                                widget.set("")
                        except (tk.TclError, IndexError):
                            pass