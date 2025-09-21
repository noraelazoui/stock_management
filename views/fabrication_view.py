import tkinter as tk
import traceback
from tkinter import ttk
from datetime import datetime
from models.formule import FormuleManager
from tkcalendar import DateEntry

class FabricationView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        
        # Initialiser le gestionnaire de formules
        self.formule_manager = FormuleManager()
        

        # Cadre principal avec titre pour les boutons radio et champs
        self.info_labelframe = ttk.Labelframe(self, text="Informations de fabrication", padding=(10, 10))
        self.info_labelframe.pack(fill=tk.X, padx=10, pady=10)
        self.top_frame = ttk.Frame(self.info_labelframe)
        self.top_frame.pack(fill=tk.X)
        
        # Variable pour stocker la sélection
        self.radio_var = tk.StringVar(value="Premix")
        
        # Frame pour les boutons radio
        self.radio_frame = ttk.Frame(self.top_frame)
        self.radio_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        # Création des boutons radio
        self.radio_premix = ttk.Radiobutton(
            self.radio_frame, 
            text="Premix", 
            variable=self.radio_var, 
            value="Premix",
            command=self.update_code_combobox
        )
        self.radio_usine = ttk.Radiobutton(
            self.radio_frame, 
            text="Usine", 
            variable=self.radio_var, 
            value="Usine",
            command=self.update_code_combobox
        )
        
        # Placement des boutons radio
        self.radio_premix.pack(side=tk.LEFT, padx=5)
        self.radio_usine.pack(side=tk.LEFT, padx=5)

        # Création des champs de saisie
        self.entries = {}
        
        # Configuration des champs spéciaux (combobox)
        # Frame pour Code
        code_container = ttk.Frame(self.top_frame)
        code_container.pack(side=tk.LEFT, padx=3)
        ttk.Label(code_container, text="Code:").pack(side=tk.LEFT, padx=(0, 2))
        self.code_combo = ttk.Combobox(code_container, width=15, state="readonly")
        self.code_combo.pack(side=tk.LEFT)
        self.entries["Code"] = self.code_combo
        # Lier l'événement de changement de code
        self.code_combo.bind('<<ComboboxSelected>>', self.on_code_selected)

        # Frame pour Optim
        optim_container = ttk.Frame(self.top_frame)
        optim_container.pack(side=tk.LEFT, padx=3)
        ttk.Label(optim_container, text="Optim:").pack(side=tk.LEFT, padx=(0, 2))
        self.optim_combo = ttk.Combobox(optim_container, width=15, state="readonly")
        self.optim_combo.pack(side=tk.LEFT)
        self.entries["Optim"] = self.optim_combo
        # Lier l'événement de changement d'optimisation
        self.optim_combo.bind('<<ComboboxSelected>>', self.on_optim_selected)

        from datetime import datetime

        # Fonction pour obtenir la date et l'heure actuelles formatées
        def get_current_datetime():
            return datetime.now().strftime("%Y-%m-%d %H:%M")

        # Création des autres champs normaux
        other_fields = [
            ("Recette:", 15),
            ("NBcomposante:", 10)
        ]

        # Création des champs avec leurs labels
        for field, width in other_fields:
            container = ttk.Frame(self.top_frame)
            container.pack(side=tk.LEFT, padx=3)
            
            # Label et Entry sur la même ligne
            ttk.Label(container, text=field).pack(side=tk.LEFT, padx=(0, 2))
            entry = ttk.Entry(container, width=width)
            entry.pack(side=tk.LEFT)
            self.entries[field.rstrip(":")] = entry

        # Ajout du champ Quantité à fabriquer (Kg)
        # Validation pour float
        def validate_float(P):
            if P == "":
                return True
            try:
                float(P)
                return True
            except ValueError:
                return False
        vcmd_float = (self.top_frame.register(validate_float), '%P')

        quantite_container = ttk.Frame(self.top_frame)
        quantite_container.pack(side=tk.LEFT, padx=3)
        ttk.Label(quantite_container, text="Quantité à fabriquer (Kg):").pack(side=tk.LEFT, padx=(0, 2))
        quantite_entry = ttk.Entry(quantite_container, width=12, validate="key", validatecommand=vcmd_float)
        quantite_entry.pack(side=tk.LEFT)
        self.entries["Quantité à fabriquer"] = quantite_entry
        
        # Création spéciale du champ Date Fabrication avec DateEntry (tkcalendar)
        from tkcalendar import DateEntry
        date_container = ttk.Frame(self.top_frame)
        date_container.pack(side=tk.LEFT, padx=3)
        ttk.Label(date_container, text="Date Fabrication:").pack(side=tk.LEFT, padx=(0, 2))
        date_entry = DateEntry(date_container, width=16, date_pattern='y-mm-dd')
        date_entry.pack(side=tk.LEFT)
        self.entries["Date Fabrication"] = date_entry

        # Ajout du champ Lot juste après Date Fabrication
        # Validation pour int
        def validate_int(P):
            if P == "":
                return True
            return P.isdigit()
        vcmd_int = (self.top_frame.register(validate_int), '%P')

        lot_container = ttk.Frame(self.top_frame)
        lot_container.pack(side=tk.LEFT, padx=3)
        ttk.Label(lot_container, text="Lot:").pack(side=tk.LEFT, padx=(0, 2))
        lot_entry = ttk.Entry(lot_container, width=10, validate="key", validatecommand=vcmd_int)
        lot_entry.pack(side=tk.LEFT)
        self.entries["Lot"] = lot_entry

        # Création des boutons à côté du champ Lot
        self.btn_ajouter = ttk.Button(lot_container, text="Ajouter", command=self.ajouter)
        self.btn_modifier = ttk.Button(lot_container, text="Modifier", command=self.modifier)
        self.btn_supprimer = ttk.Button(lot_container, text="Supprimer", command=self.supprimer)
        self.btn_valider = ttk.Button(lot_container, text="Valider", command=self.valider)
        self.btn_ajouter.pack(side=tk.LEFT, padx=2)
        self.btn_modifier.pack(side=tk.LEFT, padx=2)
        self.btn_supprimer.pack(side=tk.LEFT, padx=2)
        self.btn_valider.pack(side=tk.LEFT, padx=2)

        # Garder une référence aux articles disponibles
        self.articles_disponibles = []

        # Mettre à jour le combobox code au démarrage
        self.update_code_combobox()

        # Création d'un cadre avec titre pour le tableau de fabrication
        self.table_labelframe = ttk.Labelframe(self, text="Tableau des fabrications", padding=(10, 10))
        self.table_labelframe.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.table_frame = ttk.Frame(self.table_labelframe)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Création du tableau avec les colonnes
        columns = ("Code", "Optime", "Recette", "NBcomposante", "Quantité à fabriquer (Kg)", "Date Fabrication", "Lot", "Prix de Formule", "Détail")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        # Configuration des en-têtes et largeurs des colonnes avec centrage
        self.tree.column("Code", width=100, anchor="center")
        self.tree.column("Optime", width=100, anchor="center")
        self.tree.column("Recette", width=150, anchor="center")
        self.tree.column("NBcomposante", width=120, anchor="center")
        self.tree.column("Quantité à fabriquer (Kg)", width=150, anchor="center")
        self.tree.column("Date Fabrication", width=120, anchor="center")
        self.tree.column("Lot", width=100, anchor="center")
        self.tree.column("Prix de Formule", width=120, anchor="center")
        self.tree.column("Détail", width=150, anchor="center")

        # Configuration des en-têtes avec centrage
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")

        # Création et configuration des scrollbars
        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Placement du tableau et des scrollbars avec grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configuration du redimensionnement
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Variable pour suivre si la fenêtre de détails est ouverte
        self.detail_window_open = False
        
        # Lier l'événement de double-clic sur le tableau
        self.tree.bind('<Double-Button-1>', self.on_tree_double_click)

    def on_tree_double_click(self, event):
        try:
            print("[DEBUG] Double-clic détecté sur le tableau.")
            if self.detail_window_open:
                print("[DEBUG] Fenêtre de détails déjà ouverte, aucune action.")
                return
            region = self.tree.identify_region(event.x, event.y)
            print(f"[DEBUG] Région cliquée : {region}")
            if region == "cell":
                column = self.tree.identify_column(event.x)
                print(f"[DEBUG] Colonne cliquée : {column}")
                selected = self.tree.selection()
                if not selected:
                    print("[DEBUG] Aucune ligne sélectionnée.")
                    return
                item = selected[0]
                detail_col = "#" + str(self.tree["columns"].index("Détail") + 1)
                print(f"[DEBUG] Index colonne Détail : {detail_col}")
                if column == detail_col:
                    values = self.tree.item(item)['values']
                    code = values[0]
                    optim = values[1]
                    print(f"[DEBUG] Ouverture des détails pour code={code}, optim={optim}")
                    self.afficher_details(code, optim)
        except Exception as e:
            print(f"Erreur lors du clic sur le tableau: {str(e)}")
            import traceback
            traceback.print_exc()

    def afficher_details(self, code, optim):
        try:
            print(f"\n=== DÉBUT AFFICHAGE DÉTAILS ===")
            print(f"Affichage des détails pour code: '{code}', optim: '{optim}'")
            
            # Créer un nouveau Frame pour les détails
            detail_frame = ttk.Frame(self)
            detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # Frame pour les champs de saisie en haut
            fields_frame = ttk.Frame(detail_frame)
            fields_frame.pack(fill=tk.X, padx=5, pady=5)

            # Définir les champs à créer pour la saisie
            self.input_fields = [
                "Article",
                "DEM",
                "Prix",
                "Quantité en stock",
                "Pourcentage",
                "Optim",      # Ajout du champ Optim
                "Recette"     # Ajout du champ Recette
            ]
            # Définir les colonnes du tableau (inclut Quantité fabriquée et Prix Total)
            self.fields = self.input_fields + ["Quantité fabriquée", "Prix Total", "Lot"]

            # Sauvegarder les références de la formule active
            self.current_code = code
            self.current_optim = optim
            print(f"Variables de formule active définies: current_code='{self.current_code}', current_optim='{self.current_optim}'")
            
            # Créer les champs de saisie en une seule ligne
            self.detail_entries = {}
            
            # Chargement des articles de la formule
            from models.formule import Formule
            try:
                # Récupérer la formule complète
                formule = Formule.get_by_code_optim(code, optim)
                if formule and formule.composantes:
                    # Extraire les articles des composantes
                    self.articles_disponibles = []
                    print(f"Composantes de la formule: {len(formule.composantes)}")
                    for comp in formule.composantes:
                        article_code = comp.article
                        if article_code:
                            if ' - ' in article_code:
                                code_part = article_code.split(' - ', 1)[0].strip()
                                print(f"Article trouvé dans composante: '{article_code}', code extrait: '{code_part}'")
                                self.articles_disponibles.append(code_part)
                            else:
                                print(f"Article trouvé dans composante (sans tiret): '{article_code}'")
                                self.articles_disponibles.append(article_code)
                    print(f"Articles disponibles: {self.articles_disponibles}")
                else:
                    print("Aucune formule ou composante trouvée")
                    self.articles_disponibles = []
            except Exception as e:
                print(f"Erreur lors du chargement des composantes: {str(e)}")
                import traceback
                traceback.print_exc()
                self.articles_disponibles = []


            # Créer les champs de saisie en utilisant self.input_fields
            for field in self.input_fields:
                # Frame pour chaque champ
                field_frame = ttk.Frame(fields_frame)
                field_frame.pack(side=tk.LEFT, padx=2)

                # Label sur la même ligne
                ttk.Label(field_frame, text=field + ":").pack(side=tk.LEFT, padx=(0, 2))

                if field == "Article":
                    entry = ttk.Combobox(field_frame, width=15, state='readonly', values=self.articles_disponibles)
                    def on_article_change(event, self=self):
                        # Vider tous les autres champs
                        for k, e in self.detail_entries.items():
                            if k != "Article":
                                if isinstance(e, ttk.Combobox):
                                    e.set("")
                                elif isinstance(e, ttk.Entry):
                                    e.config(state='normal')
                                    e.delete(0, 'end')
                        # Appeler la logique de remplissage
                        self.on_article_selected(event)
                        # Remettre tous les Entry en readonly après remplissage
                        for k, e in self.detail_entries.items():
                            if isinstance(e, ttk.Entry):
                                e.config(state='readonly')
                    entry.bind('<<ComboboxSelected>>', on_article_change)
                elif field == "DEM":
                    entry = ttk.Combobox(field_frame, width=15, state='readonly')
                    def on_dem_change(event, self=self):
                        # Rendre les champs modifiables
                        for k, e in self.detail_entries.items():
                            if isinstance(e, ttk.Entry):
                                e.config(state='normal')
                        self.on_dem_selected(event)
                        # Remettre readonly
                        for k, e in self.detail_entries.items():
                            if isinstance(e, ttk.Entry):
                                e.config(state='readonly')
                    entry.bind('<<ComboboxSelected>>', on_dem_change)
                else:
                    entry = ttk.Entry(field_frame, width=15)
                    entry.config(state='readonly')
                entry.pack(side=tk.LEFT)
                self.detail_entries[field] = entry

            # Les boutons sont maintenant placés à côté du champ Recette

            # Placer les boutons à côté du champ Recette
            for field in self.input_fields:
                if field == "Recette":
                    btn_ajouter = ttk.Button(field_frame, text="Ajouter", command=self.ajouter_detail, width=12)
                    btn_modifier = ttk.Button(field_frame, text="Modifier", command=self.modifier_detail, width=12)
                    btn_supprimer = ttk.Button(field_frame, text="Supprimer", command=self.supprimer_detail, width=12)
                    btn_ajouter.pack(side=tk.LEFT, padx=2)
                    btn_modifier.pack(side=tk.LEFT, padx=2)
                    btn_supprimer.pack(side=tk.LEFT, padx=2)


            # Cadre avec titre pour le tableau de détail fabrication
            detail_table_labelframe = ttk.Labelframe(detail_frame, text="Détail de la fabrication", padding=(10, 10))
            detail_table_labelframe.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            table_frame = ttk.Frame(detail_table_labelframe)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # Créer le tableau avec les mêmes colonnes
            columns = self.fields
            detail_tree = ttk.Treeview(table_frame, columns=columns, show="headings")

            # Configuration des colonnes
            for col in columns:
                detail_tree.column(col, anchor="center", width=100)
                detail_tree.heading(col, text=col)

            # Scrollbars pour le tableau
            scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=detail_tree.yview)
            scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=detail_tree.xview)
            detail_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)


            # Placement du tableau et des scrollbars avec grid
            detail_tree.grid(row=0, column=0, sticky="nsew")
            scrollbar_y.grid(row=0, column=1, sticky="ns")
            scrollbar_x.grid(row=1, column=0, sticky="ew")
            table_frame.grid_rowconfigure(0, weight=1)
            table_frame.grid_columnconfigure(0, weight=1)

            # Bouton retour en bas
            btn_retour = ttk.Button(detail_frame, text="Retour", command=lambda: self.retour_vue_principale(detail_frame), width=15)
            btn_retour.pack(pady=10)

            # Sauvegarder les références dont nous aurons besoin
            self.current_detail_frame = detail_frame
            self.detail_tree = detail_tree
            self.current_code = code
            self.current_optim = optim
            from models.fabrication import Fabrication
            details = Fabrication.get_details_fabrication(code, optim)
            
            if details:
                print(f"Détails récupérés: {len(details)} éléments")
                
                # Au lieu de créer un nouveau Treeview, utiliser celui qui existe déjà (self.detail_tree)
                # et ajuster ses colonnes
                
                # Définir des colonnes appropriées pour les détails
                new_columns = (
                    "Article", "DEM", "Prix", "Quantité en stock", "Pourcentage", "Optim Formule",
                    "Recette Formule", "Quantité Fabriquée"
                )
                
                # Mettre à jour la variable self.fields pour qu'elle corresponde aux colonnes du tableau
                self.fields = list(new_columns) + ["Prix Total"]
                
                # Reconfigurer le Treeview existant
                self.detail_tree['columns'] = self.fields
                
                # Configuration des colonnes avec des largeurs appropriées
                column_widths = {
                    "Article": 100,
                    "DEM": 80,
                    "Prix": 80,
                    "Quantité en stock": 100,
                    "Pourcentage": 80,
                    "Optim Formule": 100,
                    "Recette Formule": 120,
                    "Quantité Fabriquée": 120,
                    "Prix Total": 100
                }

                # Configuration des colonnes
                for col in self.fields:
                    if col in column_widths:
                        self.detail_tree.column(col, anchor="center", width=column_widths[col])
                    else:
                        self.detail_tree.column(col, anchor="center", width=100)
                    self.detail_tree.heading(col, text=col, anchor="center")
                
                # Vider le Treeview avant d'ajouter de nouveaux éléments
                for item in self.detail_tree.get_children():
                    self.detail_tree.delete(item)

                # Ajouter les détails dans le tableau
                for detail in details:
                    # Préparer toutes les valeurs
                    values = []
                    for col in self.fields:
                        if col == "Article":
                            values.append(detail.get("article", ""))
                        elif col == "DEM":
                            values.append(detail.get("dem", ""))
                        elif col == "Prix":
                            values.append(f"{detail.get('prix', 0)}")
                        elif col == "Quantité en stock":
                            values.append(f"{detail.get('quantite_stock', 0)}")
                        elif col == "Pourcentage":
                            values.append(f"{detail.get('pourcentage', 0)}%")
                        elif col == "Optim Formule":
                            values.append(detail.get("optim_formule", ""))
                        elif col == "Recette Formule":
                            values.append(detail.get("recette_formule", ""))
                        elif col == "Quantité Fabriquée":
                            values.append(f"{detail.get('quantite_fabrique', 0)}")
                        elif col == "Prix Total":
                            # Calculer le prix total si nécessaire
                            if "prix_total" in detail:
                                values.append(f"{detail.get('prix_total', 0)}")
                            else:
                                prix = float(detail.get('prix', 0))
                                quantite = float(detail.get('quantite_fabrique', 0))
                                prix_total = prix * quantite
                                values.append(f"{prix_total}")
                    
                    # Insérer dans le tableau
                    self.detail_tree.insert('', 'end', values=values)
                
                print(f"Tableau mis à jour avec {len(details)} détails")

                # Style pour le Treeview
                style = ttk.Style()
                style.configure("Treeview", rowheight=25)  # Augmente la hauteur des lignes
                style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))  # Style des en-têtes

                # Frame pour contenir le Treeview et les scrollbars
                tree_frame = ttk.Frame(detail_frame)
                tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

                # Mettre à jour les scrollbars pour utiliser le Treeview existant
                scrollbar_y.config(command=self.detail_tree.yview)
                scrollbar_x.config(command=self.detail_tree.xview)
                self.detail_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

                # S'assurer que le Treeview est bien placé
                self.detail_tree.pack(in_=tree_frame, fill=tk.BOTH, expand=True, side=tk.LEFT)
                scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
                scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
                
                # Marquer la fenêtre de détails comme ouverte
                self.detail_window_open = True
                print("Affichage des détails terminé avec succès")

        except Exception as e:
            print(f"Erreur lors de l'affichage des détails: {str(e)}")
            import traceback
            traceback.print_exc()

    def retour_vue_principale(self, detail_frame):
        print("[DEBUG] Fermeture de la fenêtre de détails.")
        detail_frame.destroy()
        self.detail_window_open = False

    def ajouter(self):
        try:
            # Récupérer les valeurs des champs
            code = self.code_combo.get()
            optim = self.optim_combo.get()
            recette = self.entries["Recette"].get()
            nb_composantes = self.entries["NBcomposante"].get()
            quantite_a_fabriquer = self.entries["Quantité à fabriquer"].get()
            date_fabrication = self.entries["Date Fabrication"].get()
            lot = self.entries["Lot"].get()  # Ajout du champ 'lot'

            # Vérification obligatoire
            if not all([code, optim, recette, lot]):
                print("Erreur : Code, Optim, Recette et Lot sont requis")
                return



            # Vérifier si le lot existe déjà dans le tableau (Treeview)
            columns = self.tree['columns']
            try:
                lot_index = columns.index('Lot')
            except ValueError:
                lot_index = 6  # fallback si colonne non trouvée
            code_index = columns.index('Code') if 'Code' in columns else 0
            optim_index = columns.index('Optime') if 'Optime' in columns else 1

            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                if (
                    len(values) > max(lot_index, code_index, optim_index)
                    and str(values[code_index]) == str(code)
                    and str(values[optim_index]) == str(optim)
                    and str(values[lot_index]) == str(lot)
                ):
                    from tkinter import messagebox
                    messagebox.showerror("Erreur", f"Le lot '{lot}' existe déjà pour ce code et cette optimisation (dans le tableau).")
                    return

            # Vérifier si le lot existe déjà pour ce code et optim dans la base MongoDB
            from models.database import db
            lot_existe = db.fabrications.find_one({
                "code": code,
                "optim": optim,
                "lot": lot
            })
            if lot_existe:
                from tkinter import messagebox
                messagebox.showerror("Erreur", f"Le lot '{lot}' existe déjà pour ce code et cette optimisation (en base).")
                return

            # Ajouter à la vue tableau uniquement
            self.tree.insert('', 'end', values=(
                code, optim, recette, nb_composantes, quantite_a_fabriquer,
                date_fabrication, lot, "", "Détail"  # Lot ajouté
            ))

            print("Fabrication ajoutée à la vue tableau uniquement.")

        except Exception as e:
            print(f"Erreur lors de l'ajout de la fabrication: {str(e)}")
            import traceback
            traceback.print_exc()

    def modifier(self):
        try:
            # Vérifier si une ligne est sélectionnée
            selection = self.tree.selection()
            if not selection:
                print("Veuillez sélectionner une ligne à modifier")
                return

            # Récupérer les nouvelles valeurs
            code = self.code_combo.get()
            optim = self.optim_combo.get()
            recette = self.entries["Recette"].get()
            nb_composantes = self.entries["NBcomposante"].get()
            quantite_a_fabriquer = self.entries["Quantité à fabriquer"].get()
            date_fabrication = self.entries["Date Fabrication"].get()

            from models.fabrication import Fabrication

            # Mettre à jour la fabrication
            nouvelles_donnees = {
                "recette_code": recette,
                "nb_composantes": nb_composantes,
                "quantite_a_fabriquer": quantite_a_fabriquer,
                "date_fabrication": date_fabrication
            }
            
            Fabrication.modifier_fabrication(code, optim, nouvelles_donnees)

            # Mettre à jour la vue tableau
            self.tree.item(selection[0], values=(
                code, optim, recette, nb_composantes, quantite_a_fabriquer,
                date_fabrication, "", "", "Détail"  # Lot et Prix de Formule vides
            ))

            print("Fabrication modifiée avec succès")

        except Exception as e:
            print(f"Erreur lors de la modification de la fabrication: {str(e)}")
            import traceback
            traceback.print_exc()

    def supprimer(self):
        try:
            # Vérifier si une ligne est sélectionnée
            selection = self.tree.selection()
            if not selection:
                print("Veuillez sélectionner une ligne à supprimer")
                return

            # Récupérer les valeurs de la ligne sélectionnée
            values = self.tree.item(selection[0])['values']
            code = values[0]
            optim = values[1]

            from models.fabrication import Fabrication

            # Supprimer la fabrication
            Fabrication.supprimer_fabrication(code, optim)

            # Supprimer de la vue tableau
            self.tree.delete(selection[0])

            print("Fabrication supprimée avec succès")

        except Exception as e:
            print(f"Erreur lors de la suppression de la fabrication: {str(e)}")
            import traceback
            traceback.print_exc()

    def update_formule_info(self, formule):
        if formule:
            # Mettre à jour la recette
            recette = formule.get('recette_code', '')
            self.entries["Recette"].delete(0, tk.END)
            self.entries["Recette"].insert(0, str(recette))
            
            # Mettre à jour le nombre de composantes
            composantes = formule.get('composantes', [])
            nb_composantes = len(composantes) if composantes else 0
            self.entries["NBcomposante"].delete(0, tk.END)
            self.entries["NBcomposante"].insert(0, str(nb_composantes))
            
            print(f"Mise à jour des informations pour l'optimisation {formule.get('optim')}:")
            print(f"Recette: {recette}")
            print(f"Nombre de composantes: {nb_composantes}")
    
    def on_optim_selected(self, event):
        try:
            selected_code = self.code_combo.get()
            selected_optim = self.optim_combo.get()
            
            print(f"\n=== Sélection Optimisation ===")
            print(f"Code sélectionné: {selected_code}")
            print(f"Optimisation sélectionnée: {selected_optim}")
            
            if not selected_code or not selected_optim:
                return
                
            from models.database import db
            # Récupérer la formule spécifique avec ce code et cette optimisation
            formule_type = "simple" if self.radio_var.get() == "Premix" else "mixte"
            formule = db.formules.find_one({
                "code": selected_code,
                "optim": selected_optim,
                "type_formule": formule_type
            })
            
            print(f"Formule trouvée: {formule}")
            
            if formule:
                # Mettre à jour la recette
                recette = formule.get('recette_code', '')
                self.entries["Recette"].delete(0, tk.END)
                self.entries["Recette"].insert(0, str(recette))
                
                # Mettre à jour le nombre de composantes
                composantes = formule.get('composantes', [])
                nb_composantes = len(composantes) if composantes else 0
                self.entries["NBcomposante"].delete(0, tk.END)
                self.entries["NBcomposante"].insert(0, str(nb_composantes))
                
                print(f"Recette mise à jour: {recette}")
                print(f"Nombre de composantes: {nb_composantes}")
            
            print("=== Fin Sélection Optimisation ===\n")
            
        except Exception as e:
            print(f"Erreur lors de la sélection de l'optimisation: {str(e)}")
            import traceback
            traceback.print_exc()

    def update_code_combobox(self):
        # Vider le combobox
        self.code_combo.set('')
        self.optim_combo.set('')
        
        try:
            from models.database import db
            # Récupérer les formules selon le type sélectionné
            if self.radio_var.get() == "Premix":
                # Pour Premix, on veut les formules de type 'simple'
                formules = list(db.formules.find({"type_formule": "simple"}))
            else:
                # Pour Usine, on veut les formules de type 'mixte'
                formules = list(db.formules.find({"type_formule": "mixte"}))
            
            # Extraire les codes des formules
            codes = [f.get('code') for f in formules if f.get('code')]
            
            # Debug: afficher les codes trouvés
            print(f"Type sélectionné: {self.radio_var.get()}")
            print(f"Codes trouvés: {codes}")
            
            # Mettre à jour les valeurs du combobox
            self.code_combo['values'] = codes
        
        except Exception as e:
            print(f"Erreur lors de la mise à jour des codes: {str(e)}")
        
    def on_code_selected(self, event):
        try:
            selected_code = self.code_combo.get()
            if not selected_code:
                return
                
            from models.database import db
            # Récupérer la formule sélectionnée avec le bon type
            formule_type = "simple" if self.radio_var.get() == "Premix" else "mixte"
            selected_formule = db.formules.find_one({
                "code": selected_code,
                "type_formule": formule_type
            })
            
            print("\n=== Débug Détaillé ===")
            print(f"Code sélectionné: {selected_code}")
            print(f"Type de formule recherché: {formule_type}")
            print(f"Formule trouvée: {selected_formule}")
            
            if selected_formule:
                # Récupérer la recette avec la bonne clé
                recette = selected_formule.get('recette_code', '')
                
                # Récupérer toutes les formules avec le même code
                from models.database import db
                formules_meme_code = list(db.formules.find({"code": selected_code}))
                
                # Extraire toutes les optimisations pour ce code
                optimisations = [str(f.get('optim', '')) for f in formules_meme_code if f.get('optim')]
                optimisations = [opt for opt in optimisations if opt]  # Enlever les valeurs vides
                
                print(f"Optimisations trouvées pour le code {selected_code}: {optimisations}")
                
                # Mettre à jour le combobox Optim avec toutes les optimisations
                self.optim_combo['values'] = optimisations
                if optimisations:
                    self.optim_combo.set(optimisations[0])  # Sélectionner la première optimisation
                
                # Récupérer le nombre de composantes
                composantes = selected_formule.get('composantes', [])
                nb_composantes = len(composantes) if composantes else 0
                
                print(f"Recette trouvée: {recette}")
                print(f"Nombre de composantes: {nb_composantes}")
                
                # Mettre à jour le champ Recette
                self.entries["Recette"].delete(0, tk.END)
                self.entries["Recette"].insert(0, str(recette))
                
                # Mettre à jour le champ NBcomposante
                self.entries["NBcomposante"].delete(0, tk.END)
                self.entries["NBcomposante"].insert(0, str(nb_composantes))
                
                # Mettre à jour la date de fabrication avec la date et l'heure actuelles
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.entries["Date Fabrication"].delete(0, tk.END)
                self.entries["Date Fabrication"].insert(0, current_datetime)
                
            print("=== Fin Débug ===\n")
            
        except Exception as e:
            print(f"Erreur: {str(e)}")

    def ajouter_detail(self):
        try:
            # Vérifier si des articles sont disponibles
            if not self.articles_disponibles:
                print("Erreur: Aucun article disponible")
                return
            # Utiliser le premier article disponible
            article = self.articles_disponibles[0]
            self.articles_disponibles.remove(article)

            # Récupérer les valeurs des champs
            valeurs = []
            detail = {}
            quantite_fabriquee = ""
            quantite_a_fabriquer = self.entries.get("Quantité à fabriquer").get()
            try:
                pourcentage = float(self.detail_entries.get("Pourcentage").get())
                quantite_a_fabriquer = float(quantite_a_fabriquer)
                quantite_fabriquee = str((pourcentage * quantite_a_fabriquer) / 100)
            except Exception:
                quantite_fabriquee = ""
            prix = 0.0
            # On récupère le prix depuis le champ Prix
            try:
                prix = float(self.detail_entries.get("Prix").get())
            except Exception:
                prix = 0.0
            for field in self.fields:
                if field == "Prix Total":
                    # Calculer Prix Total = prix * quantite_fabriquee
                    try:
                        prix_total = prix * float(quantite_fabriquee)
                    except Exception:
                        prix_total = 0.0
                    valeurs.append(str(prix_total))
                    detail["prix_total"] = prix_total
                    continue
                if field == "Quantité fabriquée":
                    valeurs.append(quantite_fabriquee)
                    detail["quantite_fabriquee"] = quantite_fabriquee
                    continue
                if field == "Lot":
                    value = self.detail_entries["Lot"].get() if "Lot" in self.detail_entries else ""
                    valeurs.append(value)
                    key = field.lower().replace(" ", "_")
                    detail[key] = value
                    continue
                value = article if field == "Article" else self.detail_entries[field].get()
                valeurs.append(value)
                key = field.lower().replace(" ", "_")
                detail[key] = value

            # Déterminer la couleur de la ligne selon la comparaison
            try:
                quantite_stock = float(self.detail_entries.get("Quantité en stock").get())
                quantite_fabriquee_float = float(quantite_fabriquee)
                if quantite_fabriquee_float <= quantite_stock:
                    tag = "vert"
                else:
                    tag = "rouge"
            except Exception:
                tag = ""

            # Ajouter les tags de couleur
            if not self.detail_tree.tag_has("vert"):
                self.detail_tree.tag_configure("vert", background="#b6fcb6")
            if not self.detail_tree.tag_has("rouge"):
                self.detail_tree.tag_configure("rouge", background="#fcb6b6")

            # Insérer dans le tableau
            self.detail_tree.insert('', 'end', values=valeurs, tags=(tag,))

            # Créer le détail dans le format voulu pour MongoDB
            detail_mongo = {
                "article": detail.get("article", ""),
                "dem": detail.get("dem", ""),
                "prix": prix,
                "quantite_stock": detail.get("quantite_en_stock", ""),
                "pourcentage": pourcentage,
                "quantite_fabrique": quantite_fabriquee,
                "prix_total": prix_total if "prix_total" in locals() else 0.0
            }

            # Récupérer l'état actuel des détails dans MongoDB
            from models.database import db
            fabrication = db.fabrications.find_one({"code": self.current_code, "optim": self.current_optim})
            details = fabrication.get("detail-fabrication", {}).get("article", []) if fabrication else []
            details.append(detail_mongo)

            # Mettre à jour MongoDB avec tous les détails
            from models.fabrication import Fabrication
            Fabrication.set_details_fabrication(self.current_code, self.current_optim, details)

            # Vider les champs sauf Article qui n'existe plus
            for field, entry in self.detail_entries.items():
                if hasattr(entry, 'delete'):
                    entry.delete(0, tk.END)
                elif hasattr(entry, 'set'):
                    entry.set('')

            # Sauvegarder automatiquement après ajout
            self.enregistrer_details_fabrication()
        except Exception as e:
            print(f"Erreur lors de l'ajout: {str(e)}")

    def modifier_detail(self):
        try:
            # Vérifier qu'une ligne est sélectionnée
            selection = self.detail_tree.selection()
            if not selection:
                print("Veuillez sélectionner une ligne à modifier")
                return

            # Récupérer l'article depuis la ligne sélectionnée
            current_values = self.detail_tree.item(selection[0])['values']
            article_selectionne = current_values[0]  # Article est la première colonne

            # Récupérer les valeurs dans l'ordre des colonnes
            valeurs = []
            for field in self.fields:
                if field == "Article":
                    valeurs.append(article_selectionne)  # Garder l'article existant
                else:
                    valeurs.append(self.detail_entries[field].get())

            # Mettre à jour la ligne sélectionnée
            self.detail_tree.item(selection[0], values=valeurs)

            # Vider les champs sauf Article qui n'existe plus
            for field, entry in self.detail_entries.items():
                if hasattr(entry, 'delete'):
                    entry.delete(0, tk.END)
                elif hasattr(entry, 'set'):
                    entry.set('')

            # Sauvegarder automatiquement après modification
            self.enregistrer_details_fabrication()
        except Exception as e:
            print(f"Erreur lors de la modification: {str(e)}")

    def supprimer_detail(self):
        try:
            # Vérifier qu'une ligne est sélectionnée
            selection = self.detail_tree.selection()
            if not selection:
                print("Veuillez sélectionner une ligne à supprimer")
                return

            # Supprimer la ligne sélectionnée
            self.detail_tree.delete(selection[0])

            # Sauvegarder automatiquement après suppression
            self.enregistrer_details_fabrication()
        except Exception as e:
            print(f"Erreur lors de la suppression: {str(e)}")

    def on_article_selected(self, event):

        # Ajout d'un événement pour le combobox Lot afin de remplir Prix et Quantité en stock
        def on_lot_selected(event_lot):
            # Rendre les champs modifiables
            for k, e in self.detail_entries.items():
                if isinstance(e, ttk.Entry):
                    e.config(state='normal')
            lot_combo = self.detail_entries["Lot"]
            selected_lot = lot_combo.get()
            # On récupère la recette et l'optim depuis les champs Optim et Recette
            recette_value = self.detail_entries["Recette"].get() if "Recette" in self.detail_entries else ""
            optim_value = self.detail_entries["Optim"].get() if "Optim" in self.detail_entries else ""
            from models.database import db
            fabrication = db.fabrications.find_one({
                "recette_code": recette_value,
                "optim": optim_value,
                "lot": selected_lot
            })
            prix = fabrication.get("prix_formule", "") if fabrication else ""
            quantite = fabrication.get("quantite_a_fabriquer", "") if fabrication else ""
            if "Prix" in self.detail_entries:
                self.detail_entries["Prix"].delete(0, tk.END)
                self.detail_entries["Prix"].insert(0, prix)
            if "Quantité en stock" in self.detail_entries:
                self.detail_entries["Quantité en stock"].delete(0, tk.END)
                self.detail_entries["Quantité en stock"].insert(0, quantite)
            # Remettre readonly
            for k, e in self.detail_entries.items():
                if isinstance(e, ttk.Entry):
                    e.config(state='readonly')

        """
        Gère l'événement de sélection d'un article dans le combobox.
        Met à jour le combobox DEM et les champs Prix et Quantité en stock pour les articles, sinon laisse vides pour les formules (seul le pourcentage s'affiche, sauf si la formule est fabriquée : alors afficher prix et quantité).
        """
        try:
            article_code = self.detail_entries["Article"].get()
            from models.database import db
            # Vérifier si l'article sélectionné est une formule
            formule_composante = db.formules.find_one({"code": article_code})
            if formule_composante:
                # Ajout/Mise à jour du combobox Lot dans la section détail
                lots_disponibles = []
                # Récupérer les lots depuis la base fabrication pour cette recette et cet optim
                recette_value = formule_composante.get("recette_code", "")
                optim_value = formule_composante.get("optim", "")
                from models.database import db
                lots_cursor = db.fabrications.find({
                    "recette_code": recette_value,
                    "optim": optim_value
                })
                for fab in lots_cursor:
                    lot_val = fab.get("lot")
                    if lot_val:
                        lots_disponibles.append(str(lot_val))

                # Créer ou mettre à jour le combobox Lot dans la section détail
                if "Lot" not in self.detail_entries:
                    # Créer le combobox Lot dans le layout (dans le même parent que les autres champs)
                    lot_frame = ttk.Frame(event.widget.master)
                    lot_frame.pack(side=tk.LEFT, padx=2)
                    ttk.Label(lot_frame, text="Lot:").pack(side=tk.LEFT, padx=(0, 2))
                    lot_combo = ttk.Combobox(lot_frame, width=12, state="readonly", values=lots_disponibles)
                    lot_combo.pack(side=tk.LEFT)
                    lot_combo.bind('<<ComboboxSelected>>', on_lot_selected)
                    self.detail_entries["Lot"] = lot_combo
                else:
                    lot_combo = self.detail_entries["Lot"]
                    lot_combo["values"] = lots_disponibles
                    lot_combo.set(lots_disponibles[0] if lots_disponibles else "")
                    lot_combo.unbind('<<ComboboxSelected>>')
                    lot_combo.bind('<<ComboboxSelected>>', on_lot_selected)
                optim_value = formule_composante.get("optim", "")
                recette_value = formule_composante.get("recette_code", "")
                if "Optim" in self.detail_entries:
                    self.detail_entries["Optim"].delete(0, tk.END)
                    self.detail_entries["Optim"].insert(0, optim_value)
                if "Recette" in self.detail_entries:
                    self.detail_entries["Recette"].delete(0, tk.END)
                    self.detail_entries["Recette"].insert(0, recette_value)
                # Cherche la fabrication associée à cette formule
                fabrication = db.fabrications.find_one({
                    "code": article_code,
                    "optim": optim_value,
                    "recette_code": recette_value
                })
                if fabrication:
                    prix_formule = fabrication.get("prix_formule", "")
                    quantite_fabrique = fabrication.get("quantite_a_fabriquer", "")
                    if "Prix" in self.detail_entries:
                        self.detail_entries["Prix"].delete(0, tk.END)
                        self.detail_entries["Prix"].insert(0, prix_formule)
                    if "Quantité en stock" in self.detail_entries:
                        self.detail_entries["Quantité en stock"].delete(0, tk.END)
                        self.detail_entries["Quantité en stock"].insert(0, quantite_fabrique)
                else:
                    if "Prix" in self.detail_entries:
                        self.detail_entries["Prix"].delete(0, tk.END)
                    if "Quantité en stock" in self.detail_entries:
                        self.detail_entries["Quantité en stock"].delete(0, tk.END)
                # Affiche le pourcentage
                pourcentage = self.get_pourcentage_article(article_code)
                if "Pourcentage" in self.detail_entries:
                    self.detail_entries["Pourcentage"].delete(0, tk.END)
                    self.detail_entries["Pourcentage"].insert(0, f"{pourcentage:.2f}")
                # Vide DEM (combobox)
                if "DEM" in self.detail_entries:
                    dem_combobox = self.detail_entries["DEM"]
                    dem_combobox.set("")
                    dem_combobox["values"] = []
            else:
                # Si c'est un article, remplir DEM, Prix et Quantité en stock
                article = db.articles.find_one({"code": article_code})
                if article:
                    dem_values = set()
                    if article.get("dem"):
                        dem_values.add(article["dem"])
                    for produit in article.get("produits", []):
                        if produit.get("DEM"):
                            dem_values.add(produit["DEM"])
                    dem_values = sorted(list(dem_values))
                    dem_combobox = self.detail_entries["DEM"]
                    if dem_values:
                        dem_combobox["values"] = dem_values
                        dem_combobox.set(dem_values[0])
                    else:
                        dem_combobox["values"] = []
                        dem_combobox.set("")
                    prix = article.get("prix", "")
                    quantite = article.get("quantite", "")
                    if "Prix" in self.detail_entries:
                        self.detail_entries["Prix"].delete(0, tk.END)
                        self.detail_entries["Prix"].insert(0, prix)
                    if "Quantité en stock" in self.detail_entries:
                        self.detail_entries["Quantité en stock"].delete(0, tk.END)
                        self.detail_entries["Quantité en stock"].insert(0, quantite)
                    # Afficher le pourcentage
                    pourcentage = self.get_pourcentage_article(article_code)
                    if "Pourcentage" in self.detail_entries:
                        self.detail_entries["Pourcentage"].delete(0, tk.END)
                        self.detail_entries["Pourcentage"].insert(0, f"{pourcentage:.2f}")
                    # Vider DEM
                    if "DEM" in self.detail_entries:
                        self.detail_entries["DEM"].set("")
                    if "Pourcentage" in self.detail_entries:
                        self.detail_entries["Pourcentage"].delete(0, tk.END)
                        self.detail_entries["Pourcentage"].insert(0, f"{pourcentage:.2f}")
        except Exception as e:
            print(f"Erreur lors de la sélection de l'article: {str(e)}")
            import traceback
            traceback.print_exc()
            selected_article_code = self.detail_entries["Article"].get()
            if not selected_article_code:
                print("Aucun article sélectionné")
                return

            # Récupérer les informations de l'article et de la formule
            from models.database import db
            from models.article import ArticleModel
            from models.formule import Formule
            
            print(f"\n=== Début recherche DEM pour article: {selected_article_code} ===")
            
            # Récupérer la formule actuelle
            formule = None
            if hasattr(self, 'current_code') and hasattr(self, 'current_optim'):
                formule = db.formules.find_one({"code": self.current_code, "optim": self.current_optim})
                
            # Vérifier si l'article sélectionné est une formule
            est_une_formule = False
            if formule:
                for comp in formule.get('composantes', []):
                    comp_article = comp.get('article', '')
                    # Vérifier si l'article de la composante correspond au code sélectionné
                    article_match = (comp_article == selected_article_code or 
                                   (' - ' in comp_article and comp_article.split(' - ', 1)[0] == selected_article_code))
                    
                    if article_match and (comp.get('optim_formule') or comp.get('recette_formule')):
                        est_une_formule = True
                        print(f"L'article {selected_article_code} est une formule")
                        break
            
            # Rechercher l'article directement par son code
            cursor = db.articles.find({"code": selected_article_code})
            article_list = list(cursor)
            
            # Récupérer les DEMs uniquement si ce n'est PAS une formule
            dems = []
            if not est_une_formule:
                # Utiliser la méthode du modèle pour récupérer les DEMs en utilisant le code de l'article
                article_model = ArticleModel()
                dems = article_model.get_article_dems(selected_article_code)
                print(f"Récupération des DEMs pour l'article {selected_article_code}")
            else:
                print(f"Pas de récupération de DEM car {selected_article_code} est une formule")
            
            print(f"Nombre d'articles trouvés: {len(article_list)}")
            print(f"Total DEM uniques trouvées: {len(dems)}")
            print(f"Liste des DEM: {dems}")
            
            # Mettre à jour le combobox DEM
            if "DEM" in self.detail_entries:
                dem_combo = self.detail_entries["DEM"]
                if hasattr(dem_combo, 'configure'):
                    # Si c'est un Combobox
                    if est_une_formule:
                        # Si c'est une formule, vider le combobox DEM
                        dem_combo['values'] = []
                        dem_combo.set('')
                        print("Combobox DEM vidé car l'article sélectionné est une formule")
                    else:
                        # Si c'est un article normal, afficher les DEMs
                        dem_combo['values'] = dems
                        if dems:
                            dem_combo.set(dems[0])
                            print(f"Combobox DEM mis à jour avec: {dems}")
                        else:
                            dem_combo.set('')
                            print("Aucune DEM trouvée pour cet article")
            
            # Récupérer la formule actuelle
            formule = None
            if hasattr(self, 'current_code') and hasattr(self, 'current_optim'):
                formule = db.formules.find_one({"code": self.current_code, "optim": self.current_optim})
            
            # Si nous avons un article et une formule, mettre à jour les autres champs
            if article_list and formule:
                article = article_list[0]  # Utiliser le premier article trouvé
                
                # Trouver la composante correspondante dans la formule
                # Chercher soit avec le code exact, soit avec un format "code - designation"
                composante = None
                for comp in formule.get('composantes', []):
                    comp_article = comp.get('article', '')
                    # Vérifier si l'article de la composante correspond au code sélectionné
                    if comp_article == selected_article_code or (
                            ' - ' in comp_article and 
                            comp_article.split(' - ', 1)[0] == selected_article_code):
                        composante = comp
                        break
                
                if composante:
                    # Utiliser le pourcentage de la composante
                    pourcentage = float(composante.get('pourcentage', 0))
                    
                    # Mettre à jour tous les champs avec les informations disponibles
                    fields_to_update = {
                        "Prix": str(article.get('prix', '0.00')),
                        "Quantité en stock": str(article.get('quantite', '0.00')),
                        "Pourcentage": f"{pourcentage:.2f}",
                        "Optim Formule": str(composante.get('optim_formule', '')),
                        "Recette Formule": str(composante.get('recette_formule', '')),
                        "Quantité Fabriquée": ""
                    }
                    
                    # Calculer la quantité fabriquée si possible
                    if hasattr(self, 'current_code') and hasattr(self, 'current_optim'):
                        nb_composantes = float(self.entries["NBcomposante"].get() or 0)
                        if nb_composantes > 0 and "quantite" in composante:
                            quantite_comp = float(composante.get('quantite', 0))
                            quantite_fabrique = nb_composantes * quantite_comp
                            fields_to_update["Quantité Fabriquée"] = f"{quantite_fabrique:.2f}"
                    
                    # Mettre à jour chaque champ s'il existe
                    for field, value in fields_to_update.items():
                        if field in self.detail_entries:
                            entry = self.detail_entries[field]
                            if hasattr(entry, 'delete') and hasattr(entry, 'insert'):
                                entry.delete(0, tk.END)
                                entry.insert(0, value)
                            elif hasattr(entry, 'set'):
                                entry.set(value)
                    
                    print("Tous les champs ont été mis à jour avec succès")
                else:
                    print(f"Aucune composante trouvée pour l'article {selected_article_code} dans la formule")
            else:
                print("Article ou formule non trouvé")
                
        except Exception as e:
            print(f"Erreur lors de la sélection de l'article: {str(e)}")
            import traceback
            traceback.print_exc()

    def on_dem_selected(self, event):
        """
        Gère l'événement de sélection d'un DEM dans le combobox.
        Met à jour les champs Prix et Quantité uniquement depuis la base de données.
        """
        try:
            selected_dem = self.detail_entries["DEM"].get()

            if not selected_dem:
                print("[ERREUR] Aucun DEM sélectionné.")
                return

            # Import de la base
            from models.database import db

            # Rechercher directement le produit par son DEM dans la base
            article = db.articles.find_one({"produits.DEM": selected_dem}, {
                "produits.$": 1  # Projection pour récupérer uniquement le produit correspondant
            })

            if article and "produits" in article:
                produit = article["produits"][0]  # Le produit correspondant au DEM

                # Mise à jour des champs Prix et Quantité
                self.detail_entries["Prix"].delete(0, tk.END)
                self.detail_entries["Prix"].insert(0, str(produit.get("Prix", 0)))
                self.detail_entries["Quantité en stock"].delete(0, tk.END)
                self.detail_entries["Quantité en stock"].insert(0, str(produit.get("Quantité", 0)))

                print("[INFO] Champs mis à jour avec succès.")
            else:
                print(f"[ERREUR] Aucun produit trouvé pour le DEM '{selected_dem}'.")

        except Exception as e:
            import traceback
            print(f"[ERREUR] Une erreur s'est produite lors de la sélection du DEM: {str(e)}")
        traceback.print_exc()

    def get_pourcentage_article(self, code_article):
        """
        Récupère le pourcentage d'un article dans la formule actuelle.
        
        Args:
            code_article (str): Le code de l'article pour lequel récupérer le pourcentage
            
        Returns:
            float: Le pourcentage de l'article dans la formule, ou 0 si non trouvé
        """
        try:
            print(f"\n=== DÉBUT RECHERCHE POURCENTAGE ===")
            print(f"Recherche pourcentage pour l'article: '{code_article}'")
            
            if not hasattr(self, 'current_code') or not hasattr(self, 'current_optim'):
                print(f"Pas de formule active (current_code ou current_optim manquant)")
                return 0
            
            print(f"Formule active: code='{self.current_code}', optim='{self.current_optim}'")
                
            from models.database import db
            
            # Imprimer toutes les formules pour déboguer
            print("\nVoici toutes les formules dans la base de données:")
            formules = list(db.formules.find())
            for i, f in enumerate(formules, 1):
                print(f"{i}. code='{f.get('code')}', optim='{f.get('optim')}', type='{f.get('type_formule')}'")
                composantes = f.get('composantes', [])
                for j, comp in enumerate(composantes, 1):
                    print(f"   {j}. article='{comp.get('article')}', pourcentage={comp.get('pourcentage')}")
            
            # Récupérer la formule actuelle directement avec les valeurs littérales
            formule = db.formules.find_one({
                "code": self.current_code, 
                "optim": self.current_optim
            })
            
            if not formule:
                # Essayer avec optim converti en nombre
                try:
                    optim_numeric = int(self.current_optim)
                    formule = db.formules.find_one({
                        "code": self.current_code, 
                        "optim": optim_numeric
                    })
                    if formule:
                        print(f"Formule trouvée avec optim numérique: {optim_numeric}")
                except ValueError:
                    pass
                
                # Si toujours pas trouvé et optim est un nombre, essayer avec optim comme chaîne
                if not formule and isinstance(self.current_optim, (int, float)):
                    formule = db.formules.find_one({
                        "code": self.current_code, 
                        "optim": str(self.current_optim)
                    })
                    if formule:
                        print(f"Formule trouvée avec optim string: {str(self.current_optim)}")
                
                if not formule:
                    print(f"Aucune formule trouvée après plusieurs tentatives")
                    return 0
            
            print(f"Formule trouvée: {formule.get('code')}-{formule.get('optim')}")
            
            # Code article sans espaces ou caractères spéciaux pour comparaison normalisée
            code_article_normalized = code_article.strip().lower()
            
            # Afficher toutes les composantes de la formule pour déboguer
            composantes = formule.get("composantes", [])
            print(f"Nombre de composantes dans la formule: {len(composantes)}")
            for i, comp in enumerate(composantes):
                comp_article = comp.get("article", "")
                comp_pourcentage = comp.get("pourcentage", 0)
                print(f"  Composante {i+1}: article='{comp_article}', pourcentage={comp_pourcentage}")
                
                # Vérification directe
                if comp_article.strip().lower() == code_article_normalized:
                    print(f"    MATCH EXACT! '{comp_article}' correspond à '{code_article}'")
                    pourcentage = float(comp_pourcentage)
                    print(f"    Pourcentage trouvé: {pourcentage}%")
                    print(f"=== FIN RECHERCHE POURCENTAGE ===\n")
                    return pourcentage
                
                # Si la composante contient un tiret, extraire le code et comparer
                if ' - ' in comp_article:
                    comp_code = comp_article.split(' - ', 1)[0].strip().lower()
                    print(f"    Code extrait: '{comp_code}'")
                    
                    # Vérifier si ce code correspond à notre code recherché
                    if comp_code == code_article_normalized:
                        print(f"    MATCH TROUVÉ! Code '{comp_code}' correspond à '{code_article_normalized}'")
                        pourcentage = float(comp_pourcentage)
                        print(f"    Pourcentage trouvé: {pourcentage}%")
                        print(f"=== FIN RECHERCHE POURCENTAGE ===\n")
                        return pourcentage
                    else:
                        print(f"    Pas de correspondance entre '{comp_code}' et '{code_article_normalized}'")
            
            # Essayer une recherche moins stricte (contient)
            for comp in composantes:
                comp_article = comp.get("article", "").strip().lower()
                if code_article_normalized in comp_article:
                    print(f"    MATCH PARTIEL! '{comp_article}' contient '{code_article_normalized}'")
                    pourcentage = float(comp.get("pourcentage", 0))
                    print(f"    Pourcentage trouvé (match partiel): {pourcentage}%")
                    print(f"=== FIN RECHERCHE POURCENTAGE ===\n")
                    return pourcentage
            
            print(f"Aucune composante ne correspond au code '{code_article}'")
            print(f"=== FIN RECHERCHE POURCENTAGE ===\n")
            return 0
            
        except Exception as e:
            print(f"Erreur lors de la récupération du pourcentage: {str(e)}")
            import traceback
            traceback.print_exc()
            return 0

    def setup_table(self):
        # Création du frame pour le tableau et les scrollbars
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Création du tableau avec les colonnes
        columns = ("Code", "Optime", "Recette", "NBcomposante", "Date Fabrication", "Lot", "Prix de Formule", "Détail")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        # Configuration des en-têtes
        for col in columns:
            self.tree.heading(col, text=col)

        # Configuration des largeurs de colonnes avec centrage
        self.tree.column("Code", width=100, anchor="center")
        self.tree.column("Optime", width=100, anchor="center")
        self.tree.column("Recette", width=150, anchor="center")
        self.tree.column("NBcomposante", width=120, anchor="center")
        self.tree.column("Date Fabrication", width=120, anchor="center")
        self.tree.column("Lot", width=100, anchor="center")
        self.tree.column("Prix de Formule", width=120, anchor="center")
        self.tree.column("Détail", width=150, anchor="center")

        # Création des scrollbars
        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        # Configuration du tableau pour utiliser les scrollbars
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Placement des éléments avec grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configuration du redimensionnement
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

    def enregistrer_details_fabrication(self):
        # Récupérer tous les détails du tableau et les enregistrer dans MongoDB
        details = []
        for item in self.detail_tree.get_children():
            values = self.detail_tree.item(item, 'values')
            # Récupérer les valeurs nécessaires
            article = values[self.fields.index("Article")] if "Article" in self.fields else ""
            dem = values[self.fields.index("DEM")] if "DEM" in self.fields else ""
            prix = float(values[self.fields.index("Prix")]) if "Prix" in self.fields else 0.0
            quantite_stock = float(values[self.fields.index("Quantité en stock")]) if "Quantité en stock" in self.fields else 0.0
            pourcentage = float(values[self.fields.index("Pourcentage")]) if "Pourcentage" in self.fields else 0.0
            quantite_fabrique = float(values[self.fields.index("Quantité fabriquée")]) if "Quantité fabriquée" in self.fields else 0.0
            prix_total = float(values[self.fields.index("Prix Total")]) if "Prix Total" in self.fields else 0.0
            optim = values[self.fields.index("Optim")] if "Optim" in self.fields else ""
            recette = values[self.fields.index("Recette")] if "Recette" in self.fields else ""
            detail = {
                "article": article,
                "dem": dem,
                "prix": prix,
                "quantite_stock": quantite_stock,
                "pourcentage": pourcentage,
                "prix_total": prix_total,
                "optim": optim,
                "recette": recette
            }
            details.append(detail)
            
        print(f"Enregistrement de {len(details)} détails pour la fabrication {self.current_code}-{self.current_optim}")
        
        # Mettre à jour MongoDB avec la liste complète
        from models.fabrication import Fabrication
        result = Fabrication.set_details_fabrication(self.current_code, self.current_optim, details)
        print(f"Résultat de l'enregistrement des détails: matched_count={result.matched_count}, modified_count={result.modified_count}")
    
    def valider(self):
        # Diminution dans le détail-article (array produits)
        from models.database import db
        for item in self.detail_tree.get_children():
            values = self.detail_tree.item(item, 'values')
            try:
                # Récupérer le code article et le DEM
                code_article = values[self.fields.index("Article")]
                dem = values[self.fields.index("DEM")]
                quantite_fabriquee = float(values[self.fields.index("Quantité fabriquée")])
                # Récupérer l'article
                article = db.articles.find_one({"code": code_article})
                if article and "produits" in article:
                    produits = article["produits"]
                    for produit in produits:
                        if str(produit.get("DEM")) == str(dem):
                            old_qte = float(produit.get("Quantité", 0))
                            new_qte = old_qte - quantite_fabriquee
                            produit["Quantité"] = str(new_qte)
                            print(f"[DEBUG] Diminution produit DEM={dem}: {old_qte} -> {new_qte}")
                            break
                    db.articles.update_one({"code": code_article}, {"$set": {"produits": produits}})

                    # Diminution du stock dans la table fabrication en prenant en compte le lot sélectionné
                    # Correction : utiliser le lot de la ligne du détail, pas celui du formulaire principal
                    idx_lot = self.fields.index("Lot") if "Lot" in self.fields else None
                    lot_detail = values[idx_lot] if idx_lot is not None else ""
                    db.fabrications.update_one(
                        {"code": self.current_code, "optim": self.current_optim, "lot": lot_detail, "detail-fabrication.article": code_article},
                        {"$inc": {"detail-fabrication.$.quantite_stock": -quantite_fabriquee}}
                    )
            except Exception as e:
                print(f"[ERROR] Diminution stock produit: {e}")
        """Méthode pour valider une fabrication et mettre à jour les stocks"""
        # Vérification des quantités fabriquées vs stock
        erreur_stock = False
        for item in self.detail_tree.get_children():
            values = self.detail_tree.item(item, 'values')
            try:
                idx_qte_fab = self.fields.index("Quantité fabriquée")
                idx_qte_stock = self.fields.index("Quantité en stock")
                quantite_fabriquee = float(values[idx_qte_fab])
                quantite_stock = float(values[idx_qte_stock])
                if quantite_fabriquee > quantite_stock:
                    erreur_stock = True
                    break
            except Exception:
                continue
        if erreur_stock:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Erreur Stock", "Impossible de valider : une quantité fabriquée dépasse la quantité en stock.")
            return

        # Vérification si une quantité en stock est vide ou non numérique
        quantite_stock_vide = False
        for item in self.detail_tree.get_children():
            values = self.detail_tree.item(item, 'values')
            try:
                idx_qte_stock = self.fields.index("Quantité en stock")
                quantite_stock = values[idx_qte_stock]
                if quantite_stock == "" or quantite_stock is None:
                    quantite_stock_vide = True
                    break
                float(quantite_stock)  # Test conversion
            except Exception:
                quantite_stock_vide = True
                break
        if quantite_stock_vide:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Erreur Stock", "Impossible de valider : une ou plusieurs composantes ont une quantité en stock vide ou non valide.")
            return

        # Validation des champs requis
        code = self.entries["Code"].get()
        optim = self.entries["Optim"].get()
        date_fabrication = self.entries["Date Fabrication"].get()
        quantite_a_fabriquer = self.entries["Quantité à fabriquer"].get()
        recette_code = self.entries.get("Recette", "").get()
        lot = self.entries.get("Lot", "").get()

        print(f"[DEBUG] Lot récupéré : {lot}")

        if not code or not optim or not date_fabrication or not quantite_a_fabriquer or not recette_code:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Erreur Validation", "Veuillez sélectionner un code, un optim, une date de fabrication, une quantité à fabriquer et une recette valides.")
            return

        # Conversion de la quantité à fabriquer en nombre
        try:
            quantite_a_fabriquer = float(quantite_a_fabriquer)
        except ValueError:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Erreur Validation", "La quantité à fabriquer doit être un nombre valide.")
            return

        # Récupération des détails de fabrication
        detail_fabrication = []
        for item in self.detail_tree.get_children():
            values = self.detail_tree.item(item, 'values')
            try:
                dem_value = values[self.fields.index("DEM")]
                lot_utilise = values[self.fields.index("Lot")]
                print(f"[DEBUG] lot_utilise récupéré : {lot_utilise}")
                
                dem = float(dem_value) if dem_value else 0.0
                detail = {
                    "article": values[self.fields.index("Article")],
                    "dem": dem,
                    "lot": lot_utilise,
                    "prix": float(values[self.fields.index("Prix")]),
                    "quantite_stock": float(values[self.fields.index("Quantité en stock")]),
                    "pourcentage": float(values[self.fields.index("Pourcentage")]),
                    "optim": values[self.fields.index("Optim")],
                    "recette": values[self.fields.index("Recette")],
                    "quantite_fabrique": float(values[self.fields.index("Quantité fabriquée")]),
                    "prix_total": float(values[self.fields.index("Prix Total")])
                }
                print(f"[DEBUG] Détail récupéré : {detail}")
                detail_fabrication.append(detail)
            except ValueError as e:
                print(f"[DEBUG] Erreur lors de la conversion de DEM : {e}")
                continue

        if not detail_fabrication:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Erreur Validation", "Aucun détail de fabrication valide trouvé.")
            return

        # Calculer le prix formule avant l'insertion
        prix_total_somme = 0.0
        for item in self.detail_tree.get_children():
            values = self.detail_tree.item(item, 'values')
            try:
                idx_prix_total = self.fields.index("Prix Total")
                prix_total = float(values[idx_prix_total])
                prix_total_somme += prix_total
            except Exception as e:
                print(f"[DEBUG] Erreur lors de la récupération du prix total : {e}")

        try:
            prix_formule = round(prix_total_somme / quantite_a_fabriquer, 4) if quantite_a_fabriquer else 0.0
            print(f"[DEBUG] Calcul prix formule : somme_prix_total={prix_total_somme}, quantite_a_fabriquer={quantite_a_fabriquer}, prix_formule={prix_formule}")
        except ZeroDivisionError:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Erreur Calcul", "La quantité à fabriquer est zéro, impossible de calculer le prix formule.")
            return

        # Créer la fabrication dans la base de données
        try:
            from models.fabrication import Fabrication
            result = Fabrication.creer_fabrication(
                code=code,
                optim=optim,
                recette_code=recette_code,
                nb_composantes=len(detail_fabrication),
                quantite_a_fabriquer=quantite_a_fabriquer,
                date_fabrication=date_fabrication,
                lot=lot,
                prix_formule=prix_formule
            )
            
            if result:
                print("Détails de fabrication insérés avec succès dans la base de données.")
                Fabrication.set_details_fabrication(code, optim,lot, detail_fabrication)
                print(f"[DEBUG] Détails insérés dans `detail-fabrication` : {detail_fabrication}")
            else:
                import tkinter.messagebox as msgbox
                msgbox.showerror("Erreur Base de Données", "Échec de l'insertion des détails de fabrication dans la base de données.")
                return
        except Exception as e:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Erreur Base de Données", f"Erreur lors de la création de la fabrication : {str(e)}")
            return

        # MISE À JOUR DES STOCKS (UNE SEULE FOIS)
        try:
            from models.database import db
            print("[DEBUG] Début de la mise à jour des stocks")
            
            for detail in detail_fabrication:
                try:
                    code_article = detail.get("article", "")
                    quantite_fabriquee = float(detail.get("quantite_fabrique", 0))
                    dem_utilise = detail.get("dem", None)
                    lot_utilise = detail.get("lot", None)
                    recette_utilisee = detail.get("recette", "")
                    optim_utilise = detail.get("optim", "")
                    print(f"[DEBUG] Traitement article: {code_article}, Quantité à diminuer: {quantite_fabriquee}, DEM: {dem_utilise}, Lot: {lot_utilise}")
                    
                    if dem_utilise is not None and str(dem_utilise) != "" and float(dem_utilise) != 0.0:
                        # Recherche dans articles par code et DEM
                        article = db.articles.find_one({"code": code_article})
                        if article:
                            produits = article.get("produits", [])
                            produit_trouve = None
                            for produit in produits:
                                if str(produit.get("DEM")) == str(dem_utilise):
                                    produit_trouve = produit
                                    break
                            if produit_trouve:
                                old_qte = float(produit_trouve.get("Quantité", 0))
                                new_qte = old_qte - quantite_fabriquee
                                produit_trouve["Quantité"] = str(new_qte)
                                print(f"[DEBUG] Diminution produit DEM={dem_utilise}: {old_qte} -> {new_qte}")
                                db.articles.update_one({"code": code_article}, {"$set": {"produits": produits}})
                            else:
                                print(f"[WARNING] Aucun produit trouvé avec DEM={dem_utilise} pour l'article {code_article}")
                        else:
                            print(f"[WARNING] Article non trouvé: {code_article}")
                    elif lot_utilise is not None and str(lot_utilise) != "" and float(lot_utilise) != 0.0:
                        # Recherche dans fabrications par lot
                        fabrication = db.fabrications.find_one({"code": code_article,"optim": optim_utilise, "recette_code": recette_utilisee, "lot": lot_utilise})
                        if fabrication:
                            quantite_stock_actuelle = float(fabrication.get("quantite_a_fabriquer", 0))
                            nouvelle_quantite_stock = quantite_stock_actuelle - quantite_fabriquee
                            print(f"[DEBUG] Lot utilisé 2: {lot_utilise}")
                            db.fabrications.update_one(
                                {
                                    "code": code_article,
                                    "optim": optim_utilise,
                                    "recette_code": recette_utilisee,
                                    "lot": lot_utilise
                                },
                                {"$set": {"quantite_a_fabriquer": nouvelle_quantite_stock}}
                            )
                            print(f"[DEBUG] Fabrication mise à jour: {quantite_stock_actuelle} -> {nouvelle_quantite_stock}")
                        else:
                            print(f"[WARNING] Fabrication non trouvée: {code_article} lot={lot_utilise}")
                    else:
                        print(f"[WARNING] Ni DEM ni Lot valide pour l'article {code_article}")
                except Exception as e:
                    print(f"[ERROR] Erreur lors de la mise à jour de l'article {detail.get('article', 'UNKNOWN')}: {e}")
            
            print("[DEBUG] Quantités en stock mises à jour après validation.")
            
        except Exception as e:
            print(f"[ERROR] Erreur lors de la mise à jour des stocks : {e}")
            import tkinter.messagebox as msgbox
            msgbox.showwarning("Avertissement", f"La fabrication a été créée mais il y a eu des erreurs lors de la mise à jour des stocks : {str(e)}")

        # Mise à jour de l'interface utilisateur
        try:
            prix_formule_result = result.get("prix_formule", 0) if result else 0
            selected_item = self.tree.selection()
            if selected_item:
                self.tree.set(selected_item, "Prix de Formule", prix_formule_result)
                print(f"Prix formule mis à jour: {prix_formule_result}")
            else:
                print("Aucune ligne sélectionnée dans le tableau.")
            
            # Mettre à jour l'interface
            if hasattr(self, 'update_code_combobox'):
                self.update_code_combobox()
            self.detail_tree.delete(*self.detail_tree.get_children())
            print("[DEBUG] Interface utilisateur mise à jour après validation.")
            
            # Message de succès
            import tkinter.messagebox as msgbox
            msgbox.showinfo("Succès", f"Fabrication validée avec succès!\nCode: {code}\nOptim: {optim}")
            
        except Exception as e:
            print(f"[ERROR] Erreur lors de la mise à jour de l'interface : {e}")