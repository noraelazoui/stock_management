from datetime import datetime
from tkinter import messagebox

class CommandeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self
        
        # Debug: print all refs available in the database
        print('DEBUG - Commande refs in DB:', [c.get('ref') for c in self.model.commandes])
        
        # Connexion boutons principaux
        self.view.add_btn.config(command=self.add_commande)
        self.view.modify_btn.config(command=self.modify_commande)
        self.view.delete_btn.config(command=self.delete_commande)
        self.view.reset_btn.config(command=self.reset_form)
        
        # Initialisation de l'affichage
        self.refresh_tree()
        self.view.update_fournisseurs()

    def refresh_tree(self):
        """Rafraîchit l'arbre principal des commandes"""
        self.view.tree.delete(*self.view.tree.get_children())
        for c in self.model.commandes:
            if "ref" in c:
                self.view.tree.insert("", "end", values=(
                    c["ref"], 
                    c.get("date_reception", ""), 
                    "Détail"
                ))

    def load_commande_details(self, ref, detail_frame):
        """
        Charge et affiche TOUTES les données (produits, infos_commande, detail_commande) 
        depuis la base pour la commande donnée dans les DataGrids correspondants
        """
        print(f"DEBUG - Chargement des détails pour ref={ref}")
        
        # Récupérer la commande complète
        commande = self.model.get_commande(ref)
        if not commande:
            print(f"DEBUG - Aucune commande trouvée pour ref={ref}")
            return
            
        print(f"DEBUG - Commande récupérée: {commande}")

        # === CHARGEMENT DU TABLEAU PRODUITS ===
        if hasattr(detail_frame, 'product_tree'):
            tree = detail_frame.product_tree
            tree.delete(*tree.get_children())
            
            produits = commande.get("produits", [])
            print(f"DEBUG - Produits à charger: {produits}")
            
            for produit in produits:
                if isinstance(produit, dict):
                    # Assurer l'ordre des colonnes
                    values = [
                        produit.get("Code", ""),
                        produit.get("DESIGNATION ARTICLE", ""),
                        produit.get("DEM", ""),
                        produit.get("QUANTITE", ""),
                        produit.get("QUANTITE REEL", ""),
                        produit.get("Prix UNI.", ""),
                        produit.get("TVA", ""),
                        produit.get("Prix TTC", ""),
                        produit.get("MONTANT", ""),
                        produit.get("MONTANT REEL", "")
                    ]
                elif isinstance(produit, (list, tuple)):
                    values = list(produit)
                else:
                    values = [str(produit)] + [""] * 9
                    
                tree.insert("", "end", values=values)
                print(f"DEBUG - Produit inséré: {values}")

        # === CHARGEMENT DU TABLEAU INFOS COMMANDE (Mode, Date, Fournisseur, etc.) ===
        if hasattr(detail_frame, 'info_commande_table'):
            info_table = detail_frame.info_commande_table
            info_table.delete(*info_table.get_children())
            
            # Utiliser le champ 'infos_commande_detail' pour les infos de commande
            infos_commande_detail = commande.get("infos_commande_detail", [])
            print(f"DEBUG - infos_commande_detail à charger: {infos_commande_detail}")
            
            for info in infos_commande_detail:
                if isinstance(info, dict):
                    values = [
                        info.get("Mode", ""),
                        info.get("Date", ""),
                        info.get("Fournisseur", ""),
                        info.get("Payement", ""),
                        info.get("Adresse", ""),
                        info.get("Transport", ""),
                        info.get("Numéro", "")
                    ]
                elif isinstance(info, (list, tuple)):
                    values = list(info)
                else:
                    values = [str(info)] + [""] * 6
                    
                info_table.insert("", "end", values=values)
                print(f"DEBUG - Info commande insérée: {values}")

        # === CHARGEMENT DU TABLEAU INFOS GENERALES (Statut, Remarque, Utilisateur) ===
        if hasattr(detail_frame, 'infos_generales_table'):
            infos_table = detail_frame.infos_generales_table
            infos_table.delete(*infos_table.get_children())
            
            # Utiliser le champ 'infos_commande' pour les infos générales
            infos_commande = commande.get("infos_commande", [])
            print(f"DEBUG - infos_commande à charger: {infos_commande}")
            
            for info in infos_commande:
                if isinstance(info, dict):
                    values = [
                        info.get("Statut", ""),
                        info.get("Remarque", ""),
                        info.get("Utilisateur", "")
                    ]
                elif isinstance(info, (list, tuple)):
                    values = list(info)
                else:
                    values = [str(info)] + [""] * 2
                    
                infos_table.insert("", "end", values=values)
                print(f"DEBUG - Info générale insérée: {values}")

    # === GESTION DES COMMANDES PRINCIPALES ===
    def add_commande(self):
        """Ajoute une nouvelle commande"""
        ref = self.view.ref_entry.get().strip()
        date_reception = self.view.date_reception_entry.get().strip() or datetime.now().strftime("%Y-%m-%d")
        fournisseur = ""

        if not ref:
            messagebox.showwarning("Champs manquants", "Veuillez saisir la référence.")
            return
        # Vérifier si la référence existe déjà
        if any(c.get("ref") == ref for c in self.model.commandes if "ref" in c):
            messagebox.showwarning("Doublon", "Cette référence existe déjà.")
            return

        cmd = {
            "ref": ref,
            "date_reception": date_reception,
            "fournisseur": fournisseur,
            "produits": [],
            "infos_commande": [],
            "detail_commande": [],
            "statut": "Créé"
        }
        self.model.add_commande(cmd)
        self.refresh_tree()
        self.reset_form()
        messagebox.showinfo("Succès", f"Commande {ref} ajoutée avec succès.")

    def modify_commande(self):
        """Modifie une commande existante"""
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une commande à modifier.")
            return
            
        item = selected[0]
        old_ref = self.view.tree.item(item, "values")[0]
        
        new_cmd = {
            "ref": self.view.ref_entry.get().strip(),
            "date_reception": self.view.date_reception_entry.get().strip(),
            "fournisseur": self.view.fournisseur_combo.get().strip()
        }
        
        if not new_cmd["ref"]:
            messagebox.showwarning("Champs manquants", "Référence obligatoire.")
            return
            
        self.model.update_commande(old_ref, new_cmd)
        self.refresh_tree()
        self.reset_form()
        messagebox.showinfo("Succès", "Commande modifiée avec succès.")

    def delete_commande(self):
        """Supprime une ou plusieurs commandes"""
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une ou plusieurs commandes à supprimer.")
            return
            
        if messagebox.askyesno("Confirmation", f"Supprimer {len(selected)} commande(s) ?"):
            refs_to_delete = [self.view.tree.item(item, "values")[0] for item in selected]
            for ref in refs_to_delete:
                self.model.delete_commande(ref)
            self.refresh_tree()
            self.reset_form()
            messagebox.showinfo("Succès", f"{len(refs_to_delete)} commande(s) supprimée(s).")

    def reset_form(self):
        """Remet à zéro le formulaire principal"""
        self.view.ref_entry.delete(0, "end")
        self.view.date_reception_entry.delete(0, "end")
        self.view.date_reception_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        if hasattr(self.view, 'fournisseur_combo'):
            self.view.fournisseur_combo.set("")

    # === GESTION DES PRODUITS ===
    def add_product_row(self, ref, product_data):
        """Ajoute un produit à la commande ET met à jour la base de données"""
        try:
            self.model.add_produit_to_commande(ref, product_data)
            
            # Mettre à jour l'article correspondant si nécessaire
            self._update_article_from_product(product_data)
            
            print(f"DEBUG - Produit ajouté à la base: {product_data}")
            return True
        except Exception as e:
            print(f"Erreur ajout produit: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit: {e}")
            return False

    def modify_product_row(self, ref, old_product, new_product):
        """Modifie un produit dans la commande ET met à jour la base de données"""
        try:
            self.model.update_produit_in_commande(ref, old_product, new_product)
            
            # Mettre à jour l'article correspondant si nécessaire
            self._update_article_from_product(new_product)
            
            print(f"DEBUG - Produit modifié dans la base: {old_product} -> {new_product}")
            return True
        except Exception as e:
            print(f"Erreur modification produit: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la modification du produit: {e}")
            return False

    def delete_product_row(self, ref, product_data):
        """Supprime un produit de la commande ET met à jour la base de données"""
        try:
            self.model.delete_produit_from_commande(ref, product_data)
            print(f"DEBUG - Produit supprimé de la base: {product_data}")
            return True
        except Exception as e:
            print(f"Erreur suppression produit: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit: {e}")
            return False

    def _update_article_from_product(self, product_data):
        """Met à jour l'article correspondant au produit"""
        try:
            from models.article import ArticleModel
            
            if isinstance(product_data, dict):
                code_article = product_data.get("Code")
                prix_ttc = product_data.get("Prix TTC")
                dem = product_data.get("DEM")
                quantite_reel = product_data.get("QUANTITE REEL")
            else:
                # Si c'est une liste
                code_article = product_data[0] if len(product_data) > 0 else None
                dem = product_data[2] if len(product_data) > 2 else None
                quantite_reel = product_data[4] if len(product_data) > 4 else None
                prix_ttc = product_data[7] if len(product_data) > 7 else None

            update_data = {}
            if prix_ttc is not None and prix_ttc != "":
                update_data["prix"] = prix_ttc
            if dem is not None and dem != "":
                update_data["dem"] = dem
            if quantite_reel is not None and quantite_reel != "":
                update_data["quantite"] = quantite_reel

            if code_article and update_data:
                ArticleModel().modify_article(code_article, update_data)
                
        except Exception as e:
            print(f"Erreur mise à jour article: {e}")

    # === GESTION DES INFOS COMMANDE DETAIL (Mode, Date, Fournisseur, etc.) ===
    def add_info_commande_detail(self, ref, info_data):
        """Ajoute une info détaillée à la commande (Mode, Date, Fournisseur, etc.)"""
        try:
            self.model.add_info_commande_detail(ref, info_data)
            print(f"DEBUG - Info commande detail ajoutée à la base: {info_data}")
            return True
        except Exception as e:
            print(f"Erreur ajout info commande detail: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'info commande: {e}")
            return False

    def modify_info_commande_detail(self, ref, old_info, new_info):
        """Modifie une info détaillée dans la commande"""
        try:
            self.model.update_info_commande_detail(ref, old_info, new_info)
            print(f"DEBUG - Info commande detail modifiée dans la base: {old_info} -> {new_info}")
            return True
        except Exception as e:
            print(f"Erreur modification info commande detail: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la modification de l'info commande: {e}")
            return False

    def delete_info_commande_detail(self, ref, info_data):
        """Supprime une info détaillée de la commande"""
        try:
            self.model.delete_info_commande_detail(ref, info_data)
            print(f"DEBUG - Info commande detail supprimée de la base: {info_data}")
            return True
        except Exception as e:
            print(f"Erreur suppression info commande detail: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la suppression de l'info commande: {e}")
            return False

    # === GESTION DES INFOS GENERALES (infos_commande) ===
    def add_infos_commande(self, ref, infos_data):
        """Ajoute des infos générales à la commande"""
        try:
            self.model.add_infos_commande(ref, infos_data)
            print(f"DEBUG - Infos générales ajoutées à la base: {infos_data}")
            return True
        except Exception as e:
            print(f"Erreur ajout infos générales: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout des infos générales: {e}")
            return False

    def modify_infos_commande(self, ref, old_infos, new_infos):
        """Modifie des infos générales dans la commande"""
        try:
            self.model.update_infos_commande(ref, old_infos, new_infos)
            print(f"DEBUG - Infos générales modifiées dans la base: {old_infos} -> {new_infos}")
            return True
        except Exception as e:
            print(f"Erreur modification infos générales: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la modification des infos générales: {e}")
            return False

    def delete_infos_commande(self, ref, infos_data):
        """Supprime des infos générales de la commande"""
        try:
            self.model.delete_infos_commande(ref, infos_data)
            print(f"DEBUG - Infos générales supprimées de la base: {infos_data}")
            return True
        except Exception as e:
            print(f"Erreur suppression infos générales: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la suppression des infos générales: {e}")
            return False