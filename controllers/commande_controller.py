from datetime import datetime
from tkinter import messagebox
from models.schemas import CommandeSchema as Schema, get_field_value

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
        
        # Initialisation de l'affichage
        self.refresh_tree()
        self.view.update_fournisseurs()

    def refresh_tree(self):
        """Rafraîchit l'arbre principal des commandes"""
        self.view.tree.delete(*self.view.tree.get_children())
        for c in self.model.commandes:
            ref = get_field_value(c, [Schema.REF, "ref"])
            if ref:
                # Get first info from infos_commande_detail if exists
                info_detail = c.get(Schema.ORDER_DETAIL, c.get("infos_commande_detail", [{}]))[0] if c.get(Schema.ORDER_DETAIL, c.get("infos_commande_detail")) else {}
                infos_gen = c.get(Schema.ORDER_INFO, c.get("infos_commande", [{}]))[0] if c.get(Schema.ORDER_INFO, c.get("infos_commande")) else {}
                
                self.view.tree.insert("", "end", values=(
                    ref,
                    get_field_value(c, [Schema.RECEPTION_DATE, "date_reception"], ""),
                    get_field_value(info_detail, [Schema.OrderDetail.MODE, "mode"], ""),
                    get_field_value(info_detail, [Schema.OrderDetail.SUPPLIER, "fournisseur"], get_field_value(c, ["fournisseur"], "")),
                    get_field_value(info_detail, [Schema.OrderDetail.PAYMENT, "payement"], ""),
                    get_field_value(info_detail, [Schema.OrderDetail.TRANSPORT, "transport"], ""),
                    get_field_value(info_detail, [Schema.OrderDetail.ADDRESS, "adresse"], ""),
                    "Détail"
                ))
        self.view.update_fournisseurs()

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
            
            produits = get_field_value(
                commande,
                [
                    Schema.PRODUCTS,
                    "produits",
                    "Produits",
                    "product",
                    "products",
                    "detail_produits",
                    "produit",
                ],
                default=[]
            )
            if produits is None:
                produits = []
            if not produits:
                # Certains jeux de données stockent les produits dans detail_commande
                alt_produits = get_field_value(
                    commande,
                    ["detail_commande", "detailCommande"],
                    default=[]
                )
                if isinstance(alt_produits, list):
                    produits = alt_produits
            print(f"DEBUG - Produits à charger: {produits}")
            
            for produit in produits:
                if isinstance(produit, dict):
                    P = Schema.Product
                    # Assurer l'ordre des colonnes
                    values = [
                        get_field_value(produit, [P.CODE, "Code"], ""),
                        get_field_value(produit, [P.DESIGNATION, "DESIGNATION ARTICLE"], ""),
                        get_field_value(produit, [P.DEM, "DEM"], ""),
                        get_field_value(produit, [P.QUANTITY, "QUANTITE"], ""),
                        get_field_value(produit, [P.REAL_QUANTITY, "QUANTITE REEL"], ""),
                        get_field_value(produit, [P.UNIT_PRICE, "Prix UNI."], ""),
                        get_field_value(produit, [P.VAT, "TVA"], ""),
                        get_field_value(produit, [P.PRICE_WITH_VAT, "Prix TTC"], ""),
                        get_field_value(produit, [P.AMOUNT, "MONTANT"], ""),
                        get_field_value(produit, [P.REAL_AMOUNT, "MONTANT REEL"], "")
                    ]
                elif isinstance(produit, (list, tuple)):
                    values = list(produit)
                else:
                    values = [str(produit)] + [""] * 9
                    
                tree.insert("", "end", values=values)
                print(f"DEBUG - Produit inséré: {values}")

    # === GESTION DES COMMANDES PRINCIPALES ===
    def add_commande(self):
        """Ajoute une nouvelle commande"""
        ref = self.view.ref_entry.get().strip()
        date_reception = self.view.date_reception_entry.get().strip() or datetime.now().strftime("%Y-%m-%d")
        mode = self.view.mode_entry.get().strip()
        fournisseur = self.view.fournisseur_combo.get().strip()
        payement = self.view.payement_entry.get().strip()
        transport = self.view.transport_entry.get().strip()
        adresse = self.view.adresse_entry.get().strip()
        # Champs supprimés de l'interface
        numero = ""
        statut = "Créé"
        remarque = ""
        utilisateur = ""

        if not ref:
            messagebox.showwarning("Champs manquants", "Veuillez saisir la référence.")
            return
        # Vérifier si la référence existe déjà
        if any(c.get("ref") == ref for c in self.model.commandes if "ref" in c):
            messagebox.showwarning("Doublon", "Cette référence existe déjà.")
            return

        cmd = {
            Schema.REF: ref,
            Schema.RECEPTION_DATE: date_reception,
            Schema.SUPPLIER: fournisseur,
            Schema.PRODUCTS: [],
            Schema.ORDER_INFO: [{
                Schema.OrderInfo.STATUS: statut,
                Schema.OrderInfo.REMARK: remarque,
                Schema.OrderInfo.USER: utilisateur
            }],
            Schema.ORDER_DETAIL: [{
                Schema.OrderDetail.MODE: mode,
                Schema.OrderDetail.DATE: date_reception,
                Schema.OrderDetail.SUPPLIER: fournisseur,
                Schema.OrderDetail.PAYMENT: payement,
                Schema.OrderDetail.ADDRESS: adresse,
                Schema.OrderDetail.TRANSPORT: transport,
                Schema.OrderDetail.NUMBER: numero
            }],
            "statut": statut  # Keep backward compatibility
        }
        self.model.add_commande(cmd)
        self.refresh_tree()
        self.reset_form()
        self.view.update_fournisseurs()
        messagebox.showinfo("Succès", f"Commande {ref} ajoutée avec succès.")

    def modify_commande(self):
        """Modifie une commande existante"""
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Sélectionnez une commande à modifier.")
            return
            
        item = selected[0]
        old_ref = self.view.tree.item(item, "values")[0]
        
        ref = self.view.ref_entry.get().strip()
        date_reception = self.view.date_reception_entry.get().strip()
        mode = self.view.mode_entry.get().strip()
        fournisseur = self.view.fournisseur_combo.get().strip()
        payement = self.view.payement_entry.get().strip()
        transport = self.view.transport_entry.get().strip()
        adresse = self.view.adresse_entry.get().strip()
        
        if not ref:
            messagebox.showwarning("Champs manquants", "Référence obligatoire.")
            return
        
        # Get existing command to preserve produits
        old_cmd = self.model.get_commande(old_ref)
        
        existing_products = get_field_value(old_cmd, [Schema.PRODUCTS, "produits"], []) if old_cmd else []
        existing_details = get_field_value(old_cmd, [Schema.ORDER_DETAIL, "infos_commande_detail"], []) if old_cmd else []
        existing_infos = get_field_value(old_cmd, [Schema.ORDER_INFO, "infos_commande"], []) if old_cmd else []

        updated_details = []
        if existing_details:
            first_detail = dict(existing_details[0])
            first_detail.update({
                Schema.OrderDetail.MODE: mode,
                Schema.OrderDetail.DATE: date_reception,
                Schema.OrderDetail.SUPPLIER: fournisseur,
                Schema.OrderDetail.PAYMENT: payement,
                Schema.OrderDetail.ADDRESS: adresse,
                Schema.OrderDetail.TRANSPORT: transport,
            })
            updated_details.append(first_detail)
            if len(existing_details) > 1:
                updated_details.extend([dict(detail) for detail in existing_details[1:]])
        else:
            updated_details.append({
                Schema.OrderDetail.MODE: mode,
                Schema.OrderDetail.DATE: date_reception,
                Schema.OrderDetail.SUPPLIER: fournisseur,
                Schema.OrderDetail.PAYMENT: payement,
                Schema.OrderDetail.ADDRESS: adresse,
                Schema.OrderDetail.TRANSPORT: transport,
                Schema.OrderDetail.NUMBER: ""
            })

        updated_infos = [dict(info) for info in existing_infos] if existing_infos else [{
            Schema.OrderInfo.STATUS: get_field_value(old_cmd, ["statut"], "Créé"),
            Schema.OrderInfo.REMARK: "",
            Schema.OrderInfo.USER: ""
        }]

        statut_value = get_field_value(updated_infos[0], [Schema.OrderInfo.STATUS, "statut"], get_field_value(old_cmd, ["statut"], "")) if updated_infos else get_field_value(old_cmd, ["statut"], "")

        new_cmd = {
            Schema.REF: ref,
            Schema.RECEPTION_DATE: date_reception,
            Schema.SUPPLIER: fournisseur,
            Schema.PRODUCTS: existing_products,
            Schema.ORDER_INFO: updated_infos,
            Schema.ORDER_DETAIL: updated_details,
            "statut": statut_value
        }
            
        self.model.update_commande(old_ref, new_cmd)
        self.refresh_tree()
        self.reset_form()
        messagebox.showinfo("Succès", "Commande modifiée avec succès.")
        self.view.update_fournisseurs()

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
            self.view.update_fournisseurs()

    def reset_form(self):
        """Remet à zéro le formulaire principal"""
        self.view.ref_entry.delete(0, "end")
        self.view.date_reception_entry.delete(0, "end")
        self.view.date_reception_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        for attr in (
            "mode_entry",
            "fournisseur_combo",
            "payement_entry",
            "transport_entry",
            "adresse_entry",
            "numero_entry",
            "statut_entry",
            "remarque_entry",
            "utilisateur_entry",
        ):
            widget = getattr(self.view, attr, None)
            if not widget:
                continue
            if hasattr(widget, "delete"):
                try:
                    widget.delete(0, "end")
                except Exception:
                    try:
                        widget.set("")
                    except Exception:
                        pass
            elif hasattr(widget, "set"):
                widget.set("")

    # === GESTION DES PRODUITS ===
    def add_product_row(self, ref, product_data):
        """Ajoute un produit à la commande ET met à jour la base de données"""
        try:
            print(f"DEBUG - add_product_row: ref={ref}")
            print(f"DEBUG - product_data={product_data}")
            
            self.model.add_produit_to_commande(ref, product_data)
            print(f"DEBUG - Produit ajouté à la commande")

            # Mettre à jour l'article correspondant si nécessaire
            self._update_article_from_product(product_data, action="add")

            print(f"DEBUG - Produit ajouté à la base: {product_data}")
            return True
        except Exception as e:
            print(f"Erreur ajout produit: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit: {e}")
            return False

    def modify_product_row(self, ref, old_product, new_product):
        """Modifie un produit dans la commande ET met à jour la base de données"""
        try:
            self.model.update_produit_in_commande(ref, old_product, new_product)

            # Mettre à jour l'article correspondant si nécessaire
            self._update_article_from_product(new_product, action="update", old_product=old_product)

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
            self._update_article_from_product(product_data, action="delete")
            print(f"DEBUG - Produit supprimé de la base: {product_data}")
            return True
        except Exception as e:
            print(f"Erreur suppression produit: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit: {e}")
            return False

    def _update_article_from_product(self, product_data, action="add", old_product=None):
        """Met à jour l'article correspondant au produit - logique basée sur DEM"""
        try:
            from models.article import ArticleModel
            from models.schemas import ArticleSchema as ArtSchema

            code_article = get_field_value(product_data, [Schema.Product.CODE, "Code", "code"])
            print(f"DEBUG - _update_article_from_product: code={code_article}, action={action}")
            
            if not code_article:
                print("DEBUG - Pas de code article")
                return

            article_model = ArticleModel()
            article = article_model.get_article(code_article)
            if not article:
                print(f"DEBUG - Article {code_article} non trouvé")
                return

            produits = get_field_value(article, [ArtSchema.PRODUCTS, "produits"], default=[])
            if not isinstance(produits, list):
                produits = list(produits) if produits else []

            print(f"DEBUG - Produits existants: {len(produits)}")
            new_product = self._build_article_product_data(product_data)
            new_dem = str(new_product.get("dem", "")).strip()
            
            print(f"DEBUG - Nouveau produit DEM={new_dem}, quantite={new_product.get('quantite')}")

            # Chercher un produit avec le même DEM
            found_index = None
            for idx, prod in enumerate(produits):
                if not isinstance(prod, dict):
                    continue
                existing_dem = str(get_field_value(prod, [ArtSchema.Product.DEM, "DEM", "dem"], "")).strip()
                if existing_dem == new_dem and new_dem:
                    found_index = idx
                    print(f"DEBUG - Produit avec DEM={new_dem} trouvé à l'index {idx}")
                    break

            if action == "add":
                if found_index is not None:
                    # Mettre à jour le produit existant avec le même DEM
                    old_quantity = float(get_field_value(produits[found_index], ["Quantité", "quantite", "quantity"], 0))
                    new_quantity_add = float(new_product.get("quantite", 0))
                    total_quantity = old_quantity + new_quantity_add
                    
                    # Mettre à jour TOUS les champs du produit existant
                    produits[found_index]["quantite"] = str(total_quantity)
                    produits[found_index]["Quantité"] = str(total_quantity)
                    produits[found_index]["quantity"] = str(total_quantity)
                    
                    # Mettre à jour le prix
                    produits[found_index]["prix"] = new_product.get("prix", "")
                    produits[found_index]["Prix"] = new_product.get("prix", "")
                    produits[found_index]["price"] = new_product.get("prix", "")
                    produits[found_index]["prix_ttc"] = new_product.get("prix_ttc", "")
                    produits[found_index]["price_ttc"] = new_product.get("price_ttc", "")
                    
                    # Mettre à jour les dates
                    produits[found_index]["date_fab"] = new_product.get("date_fab", "")
                    produits[found_index]["Date fabrication"] = new_product.get("Date fabrication", "")
                    produits[found_index]["manufacturing_date"] = new_product.get("manufacturing_date", "")
                    produits[found_index]["date_fabrication"] = new_product.get("date_fabrication", "")
                    
                    produits[found_index]["date_exp"] = new_product.get("date_exp", "")
                    produits[found_index]["Date expiration"] = new_product.get("Date expiration", "")
                    produits[found_index]["expiration_date"] = new_product.get("expiration_date", "")
                    produits[found_index]["date_expiration"] = new_product.get("date_expiration", "")
                    
                    print(f"DEBUG - Quantite mise a jour: {old_quantity} + {new_quantity_add} = {total_quantity}")
                else:
                    # Ajouter un nouveau produit
                    produits.append(new_product)
                    print(f"DEBUG - Nouveau produit ajoute avec DEM={new_dem}")

            elif action == "update":
                if old_product:
                    old_normalized = self._build_article_product_data(old_product)
                    old_dem = str(old_normalized.get("dem", "")).strip()
                    
                    # Chercher l'ancien produit par DEM
                    old_index = None
                    for idx, prod in enumerate(produits):
                        if not isinstance(prod, dict):
                            continue
                        existing_dem = str(get_field_value(prod, [ArtSchema.Product.DEM, "DEM", "dem"], "")).strip()
                        if existing_dem == old_dem and old_dem:
                            old_index = idx
                            break
                    
                    if old_index is not None:
                        produits[old_index] = new_product
                        print(f"DEBUG - Produit avec DEM={old_dem} mis à jour")
                    else:
                        produits.append(new_product)
                        print(f"DEBUG - Ancien produit non trouvé, nouveau ajouté")
                else:
                    if found_index is not None:
                        produits[found_index] = new_product
                    else:
                        produits.append(new_product)

            elif action == "delete":
                if found_index is not None:
                    del produits[found_index]
                    print(f"DEBUG - Produit avec DEM={new_dem} supprimé")

            produits = [dict(prod) for prod in produits]
            save_result = article_model._save_article_products(code_article, produits)
            print(f"DEBUG - Sauvegarde: {save_result}")
            
            article_model.recalculate_main_quantity(code_article)

        except Exception as e:
            print(f"Erreur mise à jour article: {e}")
            import traceback
            traceback.print_exc()

    def _build_article_product_data(self, product_data):
        from models.schemas import ArticleSchema as ArtSchema

        price = get_field_value(product_data, ["Prix TTC", "prix_ttc", "price_ttc", "price", "Prix", "prix", "Prix UNI.", "price_with_vat", Schema.Product.UNIT_PRICE, Schema.Product.PRICE_WITH_VAT], "")
        quantity = get_field_value(product_data, ["QUANTITE REEL", "QUANTITE", "quantite", "Quantité", "quantity", Schema.Product.QUANTITY], "")
        dem = get_field_value(product_data, ["DEM", "dem", Schema.Product.DEM], "")
        date_fab = get_field_value(product_data, ["date_fab", "Date fabrication", "manufacturing_date"], "")
        date_exp = get_field_value(product_data, ["date_exp", "Date expiration", "expiration_date"], "")

        normalized = {
            "Prix": price,
            "prix": price,
            "prix_ttc": price,
            "price_ttc": price,
            "Quantité": quantity,
            "quantite": quantity,
            "quantity": quantity,
            "DEM": dem,
            "dem": dem,
            "Date fabrication": date_fab,
            "date_fab": date_fab,
            "date_fabrication": date_fab,
            "manufacturing_date": date_fab,
            "Date expiration": date_exp,
            "date_exp": date_exp,
            "date_expiration": date_exp,
            "expiration_date": date_exp,
        }
        # Ajouter les constantes du schéma si elles existent
        if hasattr(ArtSchema.Product, 'PRICE'):
            normalized[ArtSchema.Product.PRICE] = price
        if hasattr(ArtSchema.Product, 'QUANTITY'):
            normalized[ArtSchema.Product.QUANTITY] = quantity
        if hasattr(ArtSchema.Product, 'DEM'):
            normalized[ArtSchema.Product.DEM] = dem
        if hasattr(ArtSchema.Product, 'MANUFACTURING_DATE'):
            normalized[ArtSchema.Product.MANUFACTURING_DATE] = date_fab
        if hasattr(ArtSchema.Product, 'EXPIRATION_DATE'):
            normalized[ArtSchema.Product.EXPIRATION_DATE] = date_exp
        
        return normalized

    def _find_article_product_index(self, produits, target_product):
        from models.schemas import ArticleSchema as ArtSchema

        if not target_product:
            return None

        for idx, prod in enumerate(produits):
            if not isinstance(prod, dict):
                continue
            price = get_field_value(prod, ["prix", "Prix", "prix_ttc", "Prix TTC", "price_ttc", "price"], "")
            quantity = get_field_value(prod, ["quantite", "Quantité", "QUANTITE", "quantity"], "")
            dem = get_field_value(prod, ["dem", "DEM"], "")
            date_fab = get_field_value(prod, ["date_fab", "date_fabrication", "Date fabrication", "manufacturing_date"], "")
            date_exp = get_field_value(prod, ["date_exp", "date_expiration", "Date expiration", "expiration_date"], "")

            if (
                str(price) == str(target_product.get("prix", ""))
                and str(quantity) == str(target_product.get("quantite", ""))
                and str(dem) == str(target_product.get("dem", ""))
                and str(date_fab) == str(target_product.get("date_fab", ""))
                and str(date_exp) == str(target_product.get("date_exp", ""))
            ):
                return idx
        return None

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