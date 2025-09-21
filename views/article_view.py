import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class ArticleView(ttk.Frame):
    def __init__(self, parent, controller):
        style = ttk.Style()
        style.theme_use('clam')
       

        super().__init__(parent)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.detail_frame = None
        self.field_width = 20
        self.detail_products = []  # Initialiser ici
        self.linked_product_tree = None  # Initialiser ici
        self.create_widgets()

    def create_widgets(self):
        # ---- Formulaire principal ----
        form_frame = ttk.LabelFrame(self, text="Ajouter / Modifier un article", padding=10)
        form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    # Ne pas donner de poids à la colonne pour éviter l'espace

    # Style personnalisé pour les labels
           
        ttk.Label(form_frame, text="Code :", style="TLabel").grid(row=0, column=0, sticky="w", padx=(0,0))
        self.code_entry = ttk.Entry(form_frame, width=15, style="Custom.TEntry")
        self.code_entry.grid(row=0, column=1, sticky="w", padx=(0,0))

        ttk.Label(form_frame, text="Désignation :", style="TLabel").grid(row=0, column=2, sticky="w", padx=(0,0))
        self.designation_entry = ttk.Entry(form_frame, width=15, style="Custom.TEntry")
        self.designation_entry.grid(row=0, column=3, sticky="w", padx=(0,0))

        ttk.Label(form_frame, text="Type :", style="TLabel").grid(row=0, column=4, sticky="w")
        self.type_combo = ttk.Combobox(
            form_frame,
            values=["additif", "matiere premiere"],
            state="readonly",
            width=15
        )
        self.type_combo.grid(row=0, column=5, sticky="w")
        self.type_combo.current(0)

        # Boutons sur la même ligne
        self.add_btn = ttk.Button(form_frame, text="Ajouter", command=self.controller.add_article, width=15)
        self.add_btn.grid(row=0, column=6, padx=5)
        self.modify_btn = ttk.Button(form_frame, text="Modifier", command=self.controller.modify_article, width=15)
        self.modify_btn.grid(row=0, column=7, padx=5)
        self.delete_btn = ttk.Button(form_frame, text="Supprimer", command=self.controller.delete_article, width=15)
        self.delete_btn.grid(row=0, column=8, padx=5)

        # ---- Tableau principal ----
        table_frame = ttk.LabelFrame(self, text="Liste des articles", padding=10)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Scrollbars pour le tableau articles
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        labels = ["Code", "Désignation", "Type", "Détail"]
        self.tree = ttk.Treeview(tree_frame, columns=("code","designation","type","detail"), show="headings", height=10)
        for col, label in zip(("code","designation","type","detail"), labels):
            self.tree.heading(col, text=label)
            self.tree.column(col, anchor="center")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Double-clic sur une ligne pour afficher le détail
        self.tree.bind("<Double-1>", self.controller.on_tree_click)

    def refresh_table(self, articles):
        self.tree.delete(*self.tree.get_children())
        for art in articles:
            # Vérifie si l'article a des détails (prix, quantité ou DEM)
            has_details = any(art.get(field) for field in ["prix", "quantite", "dem"])
            
            # Insère la ligne avec la couleur appropriée
            item = self.tree.insert("", "end", values=(art["code"], art["designation"], art["type"], "Détail"))
            
            # Configure la couleur de la ligne
            if has_details:
                self.tree.tag_configure("with_details", background="#90EE90")  # Vert clair
                self.tree.item(item, tags=("with_details",))
            else:
                self.tree.tag_configure("no_details", background="#FFB6C1")  # Rouge clair
                self.tree.item(item, tags=("no_details",))

    def show_detail_form(self, article):
        if self.detail_frame:
            self.detail_frame.destroy()

        self.detail_frame = ttk.LabelFrame(self, text=f"Détail de {article['code']}", padding=10)
        self.detail_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.detail_frame.columnconfigure(0, weight=1)
        self.detail_frame.columnconfigure(1, weight=2)

        # Frame pour les champs du détail (1/3)
        champs_frame = ttk.Frame(self.detail_frame)
        champs_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))

        # Validation pour n'accepter que des chiffres
        def validate_float(P):
            if P == "":
                return True
            try:
                float(P)
                return True
            except ValueError:
                return False

        def validate_int(P):
            if P == "":
                return True
            return P.isdigit()

        vcmd_float = (self.register(validate_float), '%P')
        vcmd_int = (self.register(validate_int), '%P')

        # Champs du détail (1/3)
        ttk.Label(champs_frame, text="Prix :", style="TLabel").grid(row=0, column=0, sticky="w")
        prix_entry = ttk.Entry(champs_frame, style="Custom.TEntry", width=15, validate="key", validatecommand=vcmd_float)
        prix_entry.insert(0, article.get("prix", ""))
        prix_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(champs_frame, text="Quantité :", style="TLabel").grid(row=1, column=0, sticky="w")
        qte_entry = ttk.Entry(champs_frame, style="Custom.TEntry", width=15, validate="key", validatecommand=vcmd_float)
        qte_entry.insert(0, article.get("quantite", ""))
        qte_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(champs_frame, text="DEM :", style="TLabel").grid(row=2, column=0, sticky="w")
        dem_entry = ttk.Entry(champs_frame, style="Custom.TEntry", width=15)
        dem_entry.insert(0, article.get("dem", ""))
        dem_entry.grid(row=2, column=1, sticky="w")

        ttk.Label(champs_frame, text="Batch :", style="TLabel").grid(row=3, column=0, sticky="w")
        batch_entry = ttk.Entry(champs_frame, style="Custom.TEntry", width=15)
        batch_entry.insert(0, article.get("batch", ""))
        batch_entry.grid(row=3, column=1, sticky="w")

        from tkcalendar import DateEntry
        ttk.Label(champs_frame, text="Date fabrication (JJ/MM/AAAA) :", style="TLabel").grid(row=4, column=0, sticky="w")
        fab_entry = DateEntry(champs_frame, width=15, date_pattern="dd/MM/yyyy")
        today_str = datetime.now().strftime("%d/%m/%Y")
        fab_value = article.get("date_fab") or today_str
        try:
            fab_entry.set_date(fab_value)
        except Exception:
            fab_entry.set_date(today_str)
        fab_entry.grid(row=4, column=1, sticky="w")

        ttk.Label(champs_frame, text="Date expiration (JJ/MM/AAAA) :", style="TLabel").grid(row=5, column=0, sticky="w")
        exp_entry = DateEntry(champs_frame, width=15, date_pattern="dd/MM/yyyy")
        exp_value = article.get("date_exp") or today_str
        try:
            exp_entry.set_date(exp_value)
        except Exception:
            exp_entry.set_date(today_str)
        exp_entry.grid(row=5, column=1, sticky="w")

        ttk.Label(champs_frame, text="Alerte expiration (mois) :", style="TLabel").grid(row=6, column=0, sticky="w")
        mois_entry = ttk.Entry(champs_frame, style="Custom.TEntry", width=15, validate="key", validatecommand=vcmd_float)
        mois_entry.insert(0, "3")  # par défaut 3 mois
        mois_entry.grid(row=6, column=1, sticky="w")

        ttk.Label(champs_frame, text="Seuil alerte quantité :", style="TLabel").grid(row=7, column=0, sticky="w")
        alerte_entry = ttk.Entry(champs_frame, width=15, style="Custom.TEntry", validate="key", validatecommand=vcmd_float)
        alerte_entry.insert(0, "10")  # seuil par défaut
        alerte_entry.grid(row=7, column=1, sticky="w")

        btns = ttk.Frame(champs_frame)
        btns.grid(row=8, column=0, columnspan=2, pady=10)
        cancel_btn = ttk.Button(btns, text="Annuler", command=self.detail_frame.destroy, width=15)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        # Frame pour le tableau des produits liés (2/3)
        linked_table_frame = ttk.LabelFrame(self.detail_frame, text="Produits liés à l'article", padding=10)
        linked_table_frame.grid(row=0, column=1, sticky="nsew", pady=20)
        columns = ("Prix", "Quantité", "DEM", "Batch", "Date fabrication", "Date expiration", "Alerte", "Seuil")
        self.linked_product_tree = ttk.Treeview(linked_table_frame, columns=columns, show="headings", height=6)
        for col in columns:
            self.linked_product_tree.heading(col, text=col)
            self.linked_product_tree.column(col, width=100, anchor="center")
        vsb = ttk.Scrollbar(linked_table_frame, orient="vertical", command=self.linked_product_tree.yview)
        hsb = ttk.Scrollbar(linked_table_frame, orient="horizontal", command=self.linked_product_tree.xview)
        self.linked_product_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.linked_product_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        linked_table_frame.grid_rowconfigure(0, weight=1)
        linked_table_frame.grid_columnconfigure(0, weight=1)

        # Liste locale des produits du formulaire
        self.detail_products = article.get("produits", []) if article.get("produits") else []
        self.linked_product_tree.delete(*self.linked_product_tree.get_children())
        for prod in self.detail_products:
            self.linked_product_tree.insert("", "end", values=(
                prod.get("Prix", ""),
                prod.get("Quantité", ""),
                prod.get("DEM", ""),
                prod.get("Batch", ""),
                prod.get("Date fabrication", ""),
                prod.get("Date expiration", ""),
                prod.get("Alerte", ""),
                prod.get("Seuil", "")
            ))

        # Fonctions pour gérer les produits liés
        def add_product():
            try:
                dem_value = dem_entry.get()
                # Vérifier si le DEM existe déjà dans la liste
                if any(prod.get("DEM") == dem_value for prod in self.detail_products):
                    messagebox.showwarning("Attention", "Ce DEM existe déjà pour cet article.")
                    return

                prod = {
                    "Prix": prix_entry.get(),
                    "Quantité": qte_entry.get(),
                    "DEM": dem_value,
                    "Batch": batch_entry.get(),
                    "Date fabrication": fab_entry.get(),
                    "Date expiration": exp_entry.get(),
                    "Alerte": mois_entry.get(),
                    "Seuil": alerte_entry.get()
                }
                self.detail_products.append(prod)
                self.linked_product_tree.insert("", "end", values=tuple(prod.values()))
                
                # Mise à jour dans la base de données
                from models.article import ArticleModel
                ArticleModel().modify_article(article["code"], {**article, "produits": self.detail_products})
                
                # Reset des champs du formulaire de détail après ajout
                self.clear_form_fields(prix_entry, qte_entry, dem_entry, batch_entry, 
                                     fab_entry, exp_entry, mois_entry, alerte_entry)
                messagebox.showinfo("Succès", "Produit ajouté avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit : {str(e)}")

        def delete_selected_product():
            try:
                selected = self.linked_product_tree.selection()
                if not selected:
                    messagebox.showwarning("Attention", "Veuillez sélectionner un ou plusieurs produits à supprimer")
                    return

                # Récupérer les index des lignes sélectionnées, triés en ordre décroissant
                idxs = sorted([self.linked_product_tree.index(item) for item in selected], reverse=True)
                # Supprimer les lignes du Treeview
                for item in selected:
                    self.linked_product_tree.delete(item)
                # Supprimer les produits correspondants dans la liste
                for idx in idxs:
                    if idx < len(self.detail_products):
                        del self.detail_products[idx]

                # Mise à jour dans la base de données
                from models.article import ArticleModel
                ArticleModel().modify_article(article["code"], {**article, "produits": self.detail_products})

                # Reset des champs du formulaire de détail après suppression
                self.clear_form_fields(prix_entry, qte_entry, dem_entry, batch_entry, 
                                     fab_entry, exp_entry, mois_entry, alerte_entry)
                messagebox.showinfo("Succès", "Produit(s) supprimé(s) avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit : {str(e)}")

        def modify_selected_product():
            try:
                selected = self.linked_product_tree.selection()
                if not selected:
                    messagebox.showwarning("Attention", "Veuillez sélectionner un produit à modifier")
                    return
                
                idx = self.linked_product_tree.index(selected[0])
                prod = {
                    "Prix": prix_entry.get(),
                    "Quantité": qte_entry.get(),
                    "DEM": dem_entry.get(),
                    "Batch": batch_entry.get(),
                    "Date fabrication": fab_entry.get(),
                    "Date expiration": exp_entry.get(),
                    "Alerte": mois_entry.get(),
                    "Seuil": alerte_entry.get()
                }
                self.detail_products[idx] = prod
                self.linked_product_tree.item(selected[0], values=tuple(prod.values()))
                
                from models.article import ArticleModel
                ArticleModel().modify_article(article["code"], {**article, "produits": self.detail_products})
                
                # Reset des champs du formulaire de détail après modification
                self.clear_form_fields(prix_entry, qte_entry, dem_entry, batch_entry, 
                                     fab_entry, exp_entry, mois_entry, alerte_entry)
                messagebox.showinfo("Succès", "Produit modifié avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification du produit : {str(e)}")

        def fill_form_from_selected():
            """Remplit le formulaire avec la ligne sélectionnée du tableau"""
            try:
                selected = self.linked_product_tree.selection()
                if not selected:
                    return
                values = self.linked_product_tree.item(selected[0], "values")
                
                # Clear and fill form fields
                fields = [prix_entry, qte_entry, dem_entry, batch_entry, 
                         fab_entry, exp_entry, mois_entry, alerte_entry]
                for field, value in zip(fields, values):
                    field.delete(0, tk.END)
                    field.insert(0, str(value) if value else "")
            except Exception as e:
                print(f"Erreur lors du remplissage du formulaire : {e}")

        # Boutons pour gérer les produits liés
        prod_btns = ttk.Frame(linked_table_frame)
        prod_btns.grid(row=2, column=0, columnspan=2, pady=5)
        
        add_btn = ttk.Button(prod_btns, text="Ajouter produit", command=add_product)
        add_btn.pack(side=tk.LEFT, padx=5)
        modify_btn = ttk.Button(prod_btns, text="Modifier produit", command=modify_selected_product)
        modify_btn.pack(side=tk.LEFT, padx=5)
        delete_btn = ttk.Button(prod_btns, text="Supprimer produit", command=delete_selected_product)
        delete_btn.pack(side=tk.LEFT, padx=5)

        # Bind event pour remplir le formulaire lors de la sélection
        self.linked_product_tree.bind("<ButtonRelease-1>", lambda e: fill_form_from_selected())

    def clear_form_fields(self, *fields):
        """Fonction utilitaire pour effacer les champs du formulaire"""
        for field in fields:
            try:
                field.delete(0, tk.END)
            except Exception as e:
                print(f"Erreur lors de l'effacement du champ : {e}")

    def get_form_data(self):
        """Récupère les données du formulaire principal"""
        return {
            "code": self.code_entry.get(),
            "designation": self.designation_entry.get(),
            "type": self.type_combo.get()
        }

    def clear_main_form(self):
        """Efface le formulaire principal"""
        self.code_entry.delete(0, tk.END)
        self.designation_entry.delete(0, tk.END)
        self.type_combo.current(0)

    def set_selected_article(self, article):
        """Remplit le formulaire principal avec les données de l'article sélectionné"""
        self.clear_main_form()
        self.code_entry.insert(0, article.get("code", ""))
        self.designation_entry.insert(0, article.get("designation", ""))
        
        # Sélectionner le type dans la combobox
        type_value = article.get("type", "")
        if type_value in ["additif", "matiere premiere"]:
            self.type_combo.set(type_value)