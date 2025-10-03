# view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import DateEntry

# Configure matplotlib backend before importing pyplot
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import matplotlib.patheffects as patheffects

class StockView(tk.Frame):
    def __init__(self, controller, master=None):
        super().__init__(master)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)

        # Seuils par défaut si non fournis par le modèle
        self.seuil_min = getattr(self.controller.model, "seuil_min", 10)
        self.seuil_max = getattr(self.controller.model, "seuil_max", 1000)

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)



        # Nouveaux onglets : Stock Article, Stock Fabrication, Inventaire de stock et Alertes
        self.tab_stock_article = ttk.Frame(self.notebook)
        self.tab_stock_fabrication = ttk.Frame(self.notebook)
        self.tab_inventaire_stock = ttk.Frame(self.notebook)
        self.tab_alertes = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_stock_article, text="Stock Article")
        self.notebook.add(self.tab_stock_fabrication, text="Stock Fabrication")
        self.notebook.add(self.tab_inventaire_stock, text="Inventaire de stock")
        self.notebook.add(self.tab_alertes, text="⚠️ Alertes Stock")

        # Responsive layout uniquement pour les deux onglets principaux
        for tab in [self.tab_stock_article, self.tab_stock_fabrication]:
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)

        # Initialize filter variables for fabrication
        self.date_from = None
        self.date_to = None
        self.filter_dem = tk.StringVar(value="Tous")
        self.filter_lot = tk.StringVar(value="Tous")

        # Bouton Actualiser pour Stock Article
        self.btn_actualiser_article = ttk.Button(self.tab_stock_article, text="Actualiser", command=self.refresh_stock_article)
        self.btn_actualiser_article.pack(anchor="ne", padx=10, pady=8)

        # Setup Stock Fabrication tab with filters
        self.setup_fabrication_filters()

        # Bouton Actualiser pour Inventaire de stock
        self.btn_actualiser_inventaire = ttk.Button(self.tab_inventaire_stock, text="Actualiser", command=self.refresh_inventaire_stock)
        self.btn_actualiser_inventaire.pack(anchor="ne", padx=10, pady=8)

        # Bouton Actualiser pour Alertes
        self.btn_actualiser_alertes = ttk.Button(self.tab_alertes, text="Actualiser", command=self.refresh_alertes)
        self.btn_actualiser_alertes.pack(anchor="ne", padx=10, pady=8)

        # Chargement des tableaux dans les onglets - delayed to avoid segfault
        # Use after_idle() to defer chart creation until window is fully initialized
        self.after_idle(self.afficher_stock_article)
        self.after_idle(self.afficher_stock_fabrication)
        self.after_idle(self.afficher_inventaire_stock)
        self.after_idle(self.afficher_alertes)
    def setup_fabrication_filters(self):
        """Setup filter frame for Stock Fabrication tab"""
        # Filter frame at the top
        filter_frame = ttk.LabelFrame(self.tab_stock_fabrication, text="Filtres", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        # Date range filter
        date_frame = ttk.Frame(filter_frame)
        date_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(date_frame, text="Date de:").grid(row=0, column=0, padx=5, sticky="e")
        self.date_from_entry = DateEntry(date_frame, width=12, background='darkblue',
                                         foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.date_from_entry.grid(row=0, column=1, padx=5)

        ttk.Label(date_frame, text="à:").grid(row=0, column=2, padx=5, sticky="e")
        self.date_to_entry = DateEntry(date_frame, width=12, background='darkblue',
                                       foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.date_to_entry.grid(row=0, column=3, padx=5)

        # DEM filter
        dem_frame = ttk.Frame(filter_frame)
        dem_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(dem_frame, text="DEM:").pack(side=tk.LEFT, padx=5)
        self.dem_combobox = ttk.Combobox(dem_frame, textvariable=self.filter_dem, width=15, state="readonly")
        self.dem_combobox.pack(side=tk.LEFT, padx=5)

        # Lot filter
        lot_frame = ttk.Frame(filter_frame)
        lot_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(lot_frame, text="Lot:").pack(side=tk.LEFT, padx=5)
        self.lot_combobox = ttk.Combobox(lot_frame, textvariable=self.filter_lot, width=15, state="readonly")
        self.lot_combobox.pack(side=tk.LEFT, padx=5)

        # Button frame
        button_frame = ttk.Frame(filter_frame)
        button_frame.pack(side=tk.LEFT, padx=10)

        # Apply filter button
        self.btn_appliquer_filtre = ttk.Button(button_frame, text="Appliquer", 
                                               command=self.apply_fabrication_filters, width=12)
        self.btn_appliquer_filtre.pack(side=tk.LEFT, padx=5)

        # Reset filter button
        self.btn_reset_filtre = ttk.Button(button_frame, text="Réinitialiser", 
                                           command=self.reset_fabrication_filters, width=12)
        self.btn_reset_filtre.pack(side=tk.LEFT, padx=5)

        # Actualiser button
        self.btn_actualiser_fabrication = ttk.Button(button_frame, text="Actualiser", 
                                                     command=self.refresh_stock_fabrication, width=12)
        self.btn_actualiser_fabrication.pack(side=tk.LEFT, padx=5)

    def refresh_inventaire_stock(self):
        # Efface le contenu de l'onglet et recharge
        for widget in self.tab_inventaire_stock.winfo_children():
            if widget != self.btn_actualiser_inventaire:
                widget.destroy()
        self.afficher_inventaire_stock()

    def apply_fabrication_filters(self):
        """Apply filters to fabrication stock"""
        for widget in self.tab_stock_fabrication.winfo_children():
            if not isinstance(widget, ttk.LabelFrame):  # Keep filter frame
                widget.destroy()
        self.afficher_stock_fabrication(apply_filters=True)

    def reset_fabrication_filters(self):
        """Reset all filters to default"""
        self.filter_dem.set("Tous")
        self.filter_lot.set("Tous")
        # Reset dates to today
        self.date_from_entry.set_date(datetime.now())
        self.date_to_entry.set_date(datetime.now())
        # Refresh display
        self.apply_fabrication_filters()

    def get_filtered_fabrications(self, fabrications):
        """Filter fabrications based on selected criteria"""
        if not fabrications:
            return []

        filtered = []
        date_from = self.date_from_entry.get_date() if hasattr(self, 'date_from_entry') else None
        date_to = self.date_to_entry.get_date() if hasattr(self, 'date_to_entry') else None
        dem_filter = self.filter_dem.get()
        lot_filter = self.filter_lot.get()

        for fab in fabrications:
            # Date filter
            if date_from and date_to:
                fab_date_str = fab.get("date_fabrication", "")
                if fab_date_str and fab_date_str != "-":
                    try:
                        # Try multiple date formats
                        fab_date = None
                        for fmt in ["%d/%m/%Y", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S"]:
                            try:
                                fab_date = datetime.strptime(fab_date_str, fmt).date()
                                break
                            except ValueError:
                                continue
                        
                        if fab_date and not (date_from <= fab_date <= date_to):
                            continue
                    except Exception:
                        pass  # Skip if date format is invalid

            # DEM filter
            if dem_filter and dem_filter != "Tous":
                # Get DEM from details (check both 'details' and 'detail-fabrication')
                details = fab.get("details", fab.get("detail-fabrication", []))
                has_dem = False
                for detail in details:
                    # Check if detail is dict (article info embedded) or string (article code)
                    if isinstance(detail, dict):
                        dem_value = detail.get("dem") or detail.get("DEM") or detail.get("Dem", "")
                        if dem_value == dem_filter:
                            has_dem = True
                            break
                if not has_dem:
                    continue

            # Lot filter
            if lot_filter and lot_filter != "Tous":
                fab_lot = fab.get("lot", "")
                if fab_lot != lot_filter:
                    continue

            filtered.append(fab)

        return filtered

    def afficher_inventaire_stock(self):
        """
        Affiche la liste complète des articles dans l'onglet Inventaire de stock avec DEM (sans Lot)
        Permet de cliquer sur un article pour voir les détails avec DEM
        """
        # Main container with PanedWindow for split view
        main_container = ttk.PanedWindow(self.tab_inventaire_stock, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel: Article list
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=2)
        
        # Articles table
        articles = self.controller.get_inventaire()
        columns = ("Code", "Désignation", "Type", "DEM", "Quantité", "Prix")
        self.inventaire_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
        
        # Configure columns with better widths (removed Lot)
        column_widths = {
            "Code": 120,
            "Désignation": 220,
            "Type": 130,
            "DEM": 120,
            "Quantité": 100,
            "Prix": 100
        }
        
        for col in columns:
            self.inventaire_tree.heading(col, text=col)
            self.inventaire_tree.column(col, anchor="center", width=column_widths.get(col, 120))
        
        # Store articles data for detail view
        self.articles_data = {}
        
        for art in articles:
            # Check if article has products (DEMs) array
            produits = art.get("produits", [])
            
            if produits:
                # Display each DEM as a separate row
                for produit in produits:
                    dem_value = produit.get("dem", "-")
                    prix_value = produit.get("price", "-")
                    quantite_value = produit.get("quantity", 0)
                    
                    item_id = self.inventaire_tree.insert("", "end", values=(
                        art.get("code", "-"),
                        art.get("designation", art.get("name", "-")),
                        art.get("type", "-"),
                        dem_value,
                        quantite_value,
                        prix_value
                    ))
                    # Store full article data with product info
                    self.articles_data[item_id] = {**art, **produit, "current_dem": dem_value}
            else:
                # Fallback: Display article without DEM details
                dem_value = art.get("dem") or art.get("DEM") or art.get("Dem", "-")
                
                item_id = self.inventaire_tree.insert("", "end", values=(
                    art.get("code", "-"),
                    art.get("designation", art.get("name", "-")),
                    art.get("type", "-"),
                    dem_value,
                    art.get("quantite", art.get("quantity", 0)),
                    art.get("prix", art.get("price", "-"))
                ))
                # Store full article data
                self.articles_data[item_id] = art
        
        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.inventaire_tree.yview)
        self.inventaire_tree.configure(yscrollcommand=scrollbar.set)
        
        self.inventaire_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.inventaire_tree.bind("<<TreeviewSelect>>", self.on_inventaire_select)
        
        # Right panel: Article details
        right_frame = ttk.LabelFrame(main_container, text="Détails de l'article", padding=15)
        main_container.add(right_frame, weight=1)
        
        # Details display area
        self.detail_text = tk.Text(right_frame, wrap=tk.WORD, font=("Arial", 11), 
                                    bg="#f9f9f9", relief=tk.FLAT, padx=10, pady=10)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.detail_text.tag_configure("title", font=("Arial", 14, "bold"), foreground="#2c3e50")
        self.detail_text.tag_configure("label", font=("Arial", 11, "bold"), foreground="#34495e")
        self.detail_text.tag_configure("value", font=("Arial", 11), foreground="#555")
        self.detail_text.tag_configure("dem_highlight", font=("Arial", 12, "bold"), 
                                      foreground="#e74c3c", background="#ffeaa7")
        self.detail_text.tag_configure("separator", font=("Arial", 10), foreground="#bdc3c7")
        
        # Initial message
        self.detail_text.insert("1.0", "\n\n\n    Cliquez sur un article\n    pour voir les détails", "title")
        self.detail_text.config(state=tk.DISABLED)
    
    def on_inventaire_select(self, event):
        """Handle article selection in inventory to show details"""
        selection = self.inventaire_tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        article = self.articles_data.get(item_id)
        
        if not article:
            return
        
        # Clear detail text
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        
        # Display article details with DEM highlighted
        self.detail_text.insert(tk.END, "Article Sélectionné\n", "title")
        self.detail_text.insert(tk.END, "=" * 40 + "\n\n", "separator")
        
        # Code
        self.detail_text.insert(tk.END, "Code: ", "label")
        self.detail_text.insert(tk.END, f"{article.get('code', '-')}\n\n", "value")
        
        # Désignation
        self.detail_text.insert(tk.END, "Désignation: ", "label")
        self.detail_text.insert(tk.END, f"{article.get('designation', article.get('name', '-'))}\n\n", "value")
        
        # Type
        self.detail_text.insert(tk.END, "Type: ", "label")
        self.detail_text.insert(tk.END, f"{article.get('type', '-')}\n\n", "value")
        
        # DEM (highlighted) - check both current_dem and dem fields
        dem_value = article.get("current_dem") or article.get("dem") or article.get("DEM") or article.get("Dem", "-")
        self.detail_text.insert(tk.END, "DEM: ", "label")
        self.detail_text.insert(tk.END, f"  {dem_value}  ", "dem_highlight")
        self.detail_text.insert(tk.END, "\n\n", "value")
        
        # Batch/Lot (if available)
        if article.get("batch"):
            self.detail_text.insert(tk.END, "Lot: ", "label")
            self.detail_text.insert(tk.END, f"{article.get('batch', '-')}\n\n", "value")
        
        # Quantité - prioritize product quantity
        self.detail_text.insert(tk.END, "Quantité en stock: ", "label")
        quantite = article.get("quantity", article.get("quantite", 0))
        self.detail_text.insert(tk.END, f"{quantite}\n\n", "value")
        
        # Prix - prioritize product price
        self.detail_text.insert(tk.END, "Prix unitaire: ", "label")
        prix = article.get("price", article.get("prix", "-"))
        self.detail_text.insert(tk.END, f"{prix}\n\n", "value")
        
        # Additional info if available
        self.detail_text.insert(tk.END, "\n" + "=" * 40 + "\n", "separator")
        self.detail_text.insert(tk.END, "Informations supplémentaires\n\n", "title")
        
        # Manufacturing date
        if article.get("manufacturing_date"):
            self.detail_text.insert(tk.END, "Date de fabrication: ", "label")
            self.detail_text.insert(tk.END, f"{article.get('manufacturing_date', '-')}\n\n", "value")
        
        # Expiration date
        if article.get("expiration_date"):
            self.detail_text.insert(tk.END, "Date d'expiration: ", "label")
            self.detail_text.insert(tk.END, f"{article.get('expiration_date', '-')}\n\n", "value")
        
        # Alert months
        if article.get("alert_months"):
            self.detail_text.insert(tk.END, "Alerte (mois): ", "label")
            self.detail_text.insert(tk.END, f"{article.get('alert_months', '-')}\n\n", "value")
        
        # Threshold
        if article.get("threshold"):
            self.detail_text.insert(tk.END, "Seuil minimal: ", "label")
            self.detail_text.insert(tk.END, f"{article.get('threshold', '-')}\n\n", "value")
        
        # Fournisseur / Supplier
        supplier = article.get("fournisseur") or article.get("supplier")
        if supplier:
            self.detail_text.insert(tk.END, "Fournisseur: ", "label")
            self.detail_text.insert(tk.END, f"{supplier}\n\n", "value")
        
        # Date création
        if article.get("date_creation"):
            self.detail_text.insert(tk.END, "Date de création: ", "label")
            self.detail_text.insert(tk.END, f"{article.get('date_creation', '-')}\n\n", "value")
        
        # Description
        if article.get("description"):
            self.detail_text.insert(tk.END, "Description: ", "label")
            self.detail_text.insert(tk.END, f"{article.get('description', '-')}\n", "value")
        
        self.detail_text.config(state=tk.DISABLED)

    def refresh_stock_article(self):
        # Efface le contenu de l'onglet et recharge
        for widget in self.tab_stock_article.winfo_children():
            if widget != self.btn_actualiser_article:
                widget.destroy()
        self.afficher_stock_article()

    def refresh_stock_fabrication(self):
        # Efface le contenu de l'onglet et recharge (keep filter frame)
        for widget in self.tab_stock_fabrication.winfo_children():
            if not isinstance(widget, ttk.LabelFrame):  # Keep filter frame
                widget.destroy()
        self.afficher_stock_fabrication()

    def afficher_stock_article(self):
        # Close any existing matplotlib figures to prevent memory leaks
        plt.close('all')
        
        # ...existing code...
        articles = self.controller.get_stock_global()
        noms = []
        quantites = []
        if articles:
            for art in articles:
                nom = art.get("designation") or art.get("name") or "-"
                quantite = art.get("quantite", art.get("quantity", 0))
                noms.append(nom)
                try:
                    quantites.append(float(quantite))
                except Exception:
                    quantites.append(0)

        # Ajout du tableau Treeview en haut
        columns = ("Article", "Quantité")
        tree = ttk.Treeview(self.tab_stock_article, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)
        for nom, qte in zip(noms, quantites):
            tree.insert("", "end", values=(nom, qte))
        tree.pack(fill=tk.X, padx=30, pady=8)
        """
        Affiche la liste des articles dans l'onglet Stock Article
        """

        # Récupérer les articles via le contrôleur et préparer les données pour le graphique
        articles = self.controller.get_stock_global()
        noms = []
        quantites = []
        if articles:
            for art in articles:
                nom = art.get("designation") or art.get("name") or "-"
                quantite = art.get("quantite", art.get("quantity", 0))
                noms.append(nom)
                try:
                    quantites.append(float(quantite))
                except Exception:
                    quantites.append(0)

        # Ajout du graphique moderne sous le tableau
        # Palette pastel moderne
        pastel_colors = ["#6EC6FF", "#FFB74D", "#81C784", "#FFD54F", "#BA68C8", "#4DD0E1", "#FF8A65", "#A1887F", "#90A4AE", "#F06292", "#9575CD", "#AED581", "#FFF176", "#E57373", "#64B5F6"]
        colors = pastel_colors * ((len(noms) // len(pastel_colors)) + 1)
        fig, ax = plt.subplots(figsize=(max(6, len(noms)*0.3), 6))
        bars = ax.bar(noms, quantites, color=colors[:len(noms)], edgecolor="none", linewidth=0, zorder=3)
        # Rounded bars and shadow effect
        for bar in bars:
            bar.set_linewidth(0)
            bar.set_alpha(0.95)
            bar.set_zorder(3)
            bar.set_capstyle('round')
            bar.set_path_effects([patheffects.withSimplePatchShadow(offset=(2,-2), alpha=0.15)])
        # Value labels
        for bar, qte in zip(bars, quantites):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.5, f"{qte}", va="bottom", ha="center", fontsize=13, fontweight="bold", color="#222", zorder=4)
        ax.set_ylabel("Quantité", fontsize=16, fontweight="bold", color="#222")
        ax.set_xlabel("Article", fontsize=16, fontweight="bold", color="#222")
        ax.set_title("Répartition des quantités par article", fontsize=20, fontweight="bold", color="#222")
        ax.grid(axis="y", linestyle="--", alpha=0.2, zorder=0)
        ax.set_facecolor("#FAFAFA")
        fig.patch.set_facecolor("#FAFAFA")
        fig.tight_layout()

        # Rotation des labels si beaucoup d'articles
        if len(noms) > 10:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=13)
        else:
            plt.setp(ax.xaxis.get_majorticklabels(), fontsize=13)

        # Tooltips interactifs
        mplcursors.cursor(bars, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{noms[sel.index]}: {quantites[sel.index]}") )

        canvas = FigureCanvasTkAgg(fig, master=self.tab_stock_article)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.X, padx=30, pady=8)

        # Ajout du graphique en camembert moderne (pie chart)
        if len(noms) > 1:
            # Filtrer les quantités négatives
            filtered = [(qte, nom) for qte, nom in zip(quantites, noms) if qte >= 0]
            if len(filtered) > 1:
                quantites_pos, noms_pos = zip(*filtered)
                fig_pie, ax_pie = plt.subplots(figsize=(7, 5))
                explode = [0.08 if i == 0 else 0.02 for i in range(len(noms_pos))]  # Met en avant la plus grande part
                # Trie pour mettre la plus grande part en premier
                sorted_data = sorted(zip(quantites_pos, noms_pos), reverse=True)
                quantites_sorted, noms_sorted = zip(*sorted_data)
                pastel_colors_pie = ["#6EC6FF", "#FFB74D", "#81C784", "#FFD54F", "#BA68C8", "#4DD0E1", "#FF8A65", "#A1887F", "#90A4AE", "#F06292", "#9575CD", "#AED581", "#FFF176", "#E57373", "#64B5F6"]
                colors_pie = pastel_colors_pie * ((len(noms_sorted) // len(pastel_colors_pie)) + 1)
                wedges, texts, autotexts = ax_pie.pie(
                    quantites_sorted,
                    labels=noms_sorted,
                    autopct=lambda pct: f"{pct:.1f}%",
                    startangle=140,
                    colors=colors_pie[:len(noms_sorted)],
                    explode=explode,
                    wedgeprops=dict(width=0.6, edgecolor="#FFF", linewidth=2, alpha=0.95),
                    textprops=dict(color="#222", fontsize=12, fontweight="bold")
                )
                ax_pie.set_title("Répartition en camembert des quantités par article", fontsize=17, fontweight="bold", color="#222")
                fig_pie.patch.set_facecolor("#FAFAFA")
                # Tooltips interactifs sur les parts
                mplcursors.cursor(wedges, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{noms_sorted[sel.index]}: {quantites_sorted[sel.index]}") )
                canvas_pie = FigureCanvasTkAgg(fig_pie, master=self.tab_stock_article)
                canvas_pie.draw()
                canvas_pie.get_tk_widget().pack(fill=tk.X, padx=30, pady=8)

    def afficher_stock_fabrication(self, apply_filters=False):
        """
        Affiche la liste des fabrications dans l'onglet Stock Fabrication avec filtres
        """
        # Close any existing matplotlib figures to prevent memory leaks
        plt.close('all')
        
        # Data container frame
        data_frame = ttk.Frame(self.tab_stock_fabrication)
        data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Enhanced columns with DEM
        columns = ("Code", "Optim", "Recette", "DEM", "Lot", "Nb Composantes", 
                   "Quantité à fabriquer", "Date Fabrication", "Prix Formule")
        tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=12)
        
        # Configure column widths
        column_widths = {
            "Code": 100,
            "Optim": 80,
            "Recette": 100,
            "DEM": 100,
            "Lot": 100,
            "Nb Composantes": 120,
            "Quantité à fabriquer": 150,
            "Date Fabrication": 120,
            "Prix Formule": 100
        }
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=column_widths.get(col, 120))
        tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # Scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        # Import FabricationController ici pour éviter les imports circulaires
        from controllers.fabrication_controller import FabricationController
        fabrication_controller = FabricationController()
        fabrications = fabrication_controller.get_all_fabrications()

        # Apply filters if requested
        if apply_filters:
            fabrications = self.get_filtered_fabrications(fabrications)

        # Update filter comboboxes with unique values
        if not apply_filters:
            self.update_filter_comboboxes(fabrications)

        codes = []
        quantites = []
        dates = []
        for fab in fabrications:
            # Extract DEM from first detail article (or aggregate multiple DEMs)
            dem_list = []
            details = fab.get("details", fab.get("detail-fabrication", []))
            for detail in details:
                # Check if detail is a dict with embedded article info or separate article reference
                if isinstance(detail, dict):
                    dem_value = detail.get("dem") or detail.get("DEM") or detail.get("Dem", "")
                    if dem_value and dem_value not in dem_list:
                        dem_list.append(dem_value)
            dem_display = ", ".join(dem_list) if dem_list else "-"
            
            # Format date for display
            date_str = fab.get("date_fabrication", "-")
            date_display = date_str
            if date_str and date_str != "-":
                try:
                    # Try to parse and format the date nicely
                    for fmt in ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d", "%d/%m/%Y", "%d/%m/%Y %H:%M:%S"]:
                        try:
                            parsed_date = datetime.strptime(date_str, fmt)
                            date_display = parsed_date.strftime("%d/%m/%Y")
                            break
                        except ValueError:
                            continue
                except Exception:
                    date_display = date_str
            
            tree.insert("", "end", values=(
                fab.get("code", "-"),
                fab.get("optim", "-"),
                fab.get("recette_code", "-"),
                dem_display,
                fab.get("lot", "-"),
                fab.get("nb_composantes", "-"),
                fab.get("quantite_a_fabriquer", "-"),
                date_display,
                fab.get("prix_formule", "-")
            ))
            codes.append(fab.get("code", "-"))
            try:
                quantites.append(float(fab.get("quantite_a_fabriquer", 0)))
            except Exception:
                quantites.append(0)
            dates.append(date_display)

        # Ajout du graphique vertical sous le tableau
        pastel_colors = ["#6EC6FF", "#FFB74D", "#81C784", "#FFD54F", "#BA68C8", "#4DD0E1", "#FF8A65", "#A1887F", "#90A4AE", "#F06292", "#9575CD", "#AED581", "#FFF176", "#E57373", "#64B5F6"]
        colors = pastel_colors * ((len(codes) // len(pastel_colors)) + 1)
        fig, ax = plt.subplots(figsize=(max(6, len(codes)*0.3), 6))
        bars = ax.bar(codes, quantites, color=colors[:len(codes)], edgecolor="none", linewidth=0, zorder=3)
        for bar in bars:
            bar.set_linewidth(0)
            bar.set_alpha(0.95)
            bar.set_zorder(3)
            bar.set_capstyle('round')
            bar.set_path_effects([patheffects.withSimplePatchShadow(offset=(2,-2), alpha=0.15)])
        for bar, qte, date in zip(bars, quantites, dates):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.5, f"{qte}\n{date}", va="bottom", ha="center", fontsize=13, fontweight="bold", color="#222", zorder=4)
        ax.set_ylabel("Quantité à fabriquer", fontsize=16, fontweight="bold", color="#222")
        ax.set_xlabel("Code fabrication", fontsize=16, fontweight="bold", color="#222")
        ax.set_title("Répartition des quantités à fabriquer par code", fontsize=20, fontweight="bold", color="#222")
        ax.grid(axis="y", linestyle="--", alpha=0.2, zorder=0)
        ax.set_facecolor("#FAFAFA")
        fig.patch.set_facecolor("#FAFAFA")
        fig.tight_layout()

        if len(codes) > 10:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=13)
        else:
            plt.setp(ax.xaxis.get_majorticklabels(), fontsize=13)

        mplcursors.cursor(bars, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{codes[sel.index]}: {quantites[sel.index]}\n{dates[sel.index]}") )

        canvas = FigureCanvasTkAgg(fig, master=data_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.X, padx=10, pady=8)

        # Add summary statistics
        self.add_fabrication_summary(data_frame, fabrications)

    def update_filter_comboboxes(self, fabrications):
        """Update filter comboboxes with unique values from fabrications"""
        # Extract unique DEMs
        dems = set(["Tous"])
        lots = set(["Tous"])
        
        for fab in fabrications:
            # Get DEMs from details (check both 'details' and 'detail-fabrication')
            details = fab.get("details", fab.get("detail-fabrication", []))
            for detail in details:
                if isinstance(detail, dict):
                    dem_value = detail.get("dem") or detail.get("DEM") or detail.get("Dem", "")
                    if dem_value:
                        dems.add(dem_value)
            
            # Get Lot
            lot_value = fab.get("lot", "")
            if lot_value and lot_value != "-":
                lots.add(lot_value)
        
        # Update comboboxes
        self.dem_combobox['values'] = sorted(list(dems))
        self.lot_combobox['values'] = sorted(list(lots))

    def add_fabrication_summary(self, parent_frame, fabrications):
        """Add summary statistics section"""
        summary_frame = ttk.LabelFrame(parent_frame, text="Statistiques", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        # Calculate statistics
        total_fabrications = len(fabrications)
        total_quantite = sum(float(fab.get("quantite_a_fabriquer", 0)) for fab in fabrications)
        
        # Count by lot
        lot_counts = {}
        for fab in fabrications:
            lot = fab.get("lot", "-")
            lot_counts[lot] = lot_counts.get(lot, 0) + 1

        # Display statistics in grid
        stats_frame = ttk.Frame(summary_frame)
        stats_frame.pack(fill=tk.X)

        ttk.Label(stats_frame, text="Total Fabrications:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(stats_frame, text=str(total_fabrications), font=("Arial", 10)).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(stats_frame, text="Quantité Totale:", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        ttk.Label(stats_frame, text=f"{total_quantite:.2f}", font=("Arial", 10)).grid(row=0, column=3, padx=10, pady=5, sticky="w")

        ttk.Label(stats_frame, text="Lots Uniques:", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=10, pady=5, sticky="w")
        ttk.Label(stats_frame, text=str(len(lot_counts)), font=("Arial", 10)).grid(row=0, column=5, padx=10, pady=5, sticky="w")

    def afficher_alertes(self):
        """Affiche les alertes de stock bas et d'expiration"""
        # Clear existing content
        for widget in self.tab_alertes.winfo_children():
            if widget != self.btn_actualiser_alertes:
                widget.destroy()

        # Main container
        main_frame = ttk.Frame(self.tab_alertes)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Get alerts from controller
        alertes = self.controller.get_alertes()
        
        # Summary frame
        summary_frame = ttk.LabelFrame(main_frame, text="📊 Résumé des Alertes", padding=10)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        nb_stock_bas = len(alertes['stock_bas'])
        nb_expiration = len(alertes['expiration'])
        nb_critique = sum(1 for a in alertes['expiration'] if a['niveau'] in ['EXPIRÉ', 'CRITIQUE'])
        
        ttk.Label(summary_frame, text=f"🔴 Stock Bas: {nb_stock_bas} produit(s)", 
                 font=("Arial", 11, "bold"), foreground="red").grid(row=0, column=0, padx=20, pady=5)
        ttk.Label(summary_frame, text=f"⏰ Expiration: {nb_expiration} produit(s)", 
                 font=("Arial", 11, "bold"), foreground="orange").grid(row=0, column=1, padx=20, pady=5)
        ttk.Label(summary_frame, text=f"⚠️ Critique: {nb_critique} produit(s)", 
                 font=("Arial", 11, "bold"), foreground="darkred").grid(row=0, column=2, padx=20, pady=5)

        # Create notebook for different alert types
        alert_notebook = ttk.Notebook(main_frame)
        alert_notebook.pack(fill=tk.BOTH, expand=True)

        # Stock Bas tab
        stock_bas_frame = ttk.Frame(alert_notebook)
        alert_notebook.add(stock_bas_frame, text=f"🔴 Stock Bas ({nb_stock_bas})")
        
        # Expiration tab
        expiration_frame = ttk.Frame(alert_notebook)
        alert_notebook.add(expiration_frame, text=f"⏰ Expiration ({nb_expiration})")

        # Display Stock Bas alerts
        self._afficher_alertes_stock_bas(stock_bas_frame, alertes['stock_bas'])
        
        # Display Expiration alerts
        self._afficher_alertes_expiration(expiration_frame, alertes['expiration'])

    def _afficher_alertes_stock_bas(self, parent, alertes):
        """Affiche les alertes de stock bas"""
        if not alertes:
            ttk.Label(parent, text="✅ Aucune alerte de stock bas", 
                     font=("Arial", 12), foreground="green").pack(pady=20)
            return

        # Create Treeview
        columns = ("Article", "Code", "DEM", "Batch", "Quantité", "Seuil", "Niveau")
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        # Configure columns
        tree.heading("Article", text="Article")
        tree.heading("Code", text="Code")
        tree.heading("DEM", text="DEM")
        tree.heading("Batch", text="Lot/Batch")
        tree.heading("Quantité", text="Quantité")
        tree.heading("Seuil", text="Seuil")
        tree.heading("Niveau", text="Niveau (%)")
        
        tree.column("Article", width=200)
        tree.column("Code", width=80)
        tree.column("DEM", width=100)
        tree.column("Batch", width=100)
        tree.column("Quantité", width=80, anchor='center')
        tree.column("Seuil", width=80, anchor='center')
        tree.column("Niveau", width=100, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure tags for color coding
        tree.tag_configure('critique', background='#ffcccc')  # Light red
        tree.tag_configure('attention', background='#ffe6cc')  # Light orange
        
        # Insert data
        for alerte in alertes:
            pourcentage = alerte['pourcentage']
            tag = 'critique' if pourcentage < 50 else 'attention'
            
            tree.insert('', 'end', values=(
                alerte['article'],
                alerte['code'],
                alerte['dem'],
                alerte['batch'],
                f"{alerte['quantity']:.1f}",
                f"{alerte['threshold']:.1f}",
                f"{pourcentage:.1f}%"
            ), tags=(tag,))

    def _afficher_alertes_expiration(self, parent, alertes):
        """Affiche les alertes d'expiration"""
        if not alertes:
            ttk.Label(parent, text="✅ Aucune alerte d'expiration", 
                     font=("Arial", 12), foreground="green").pack(pady=20)
            return

        # Create Treeview
        columns = ("Article", "Code", "DEM", "Batch", "Date Exp.", "Jours Restants", "Niveau", "Quantité")
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        # Configure columns
        tree.heading("Article", text="Article")
        tree.heading("Code", text="Code")
        tree.heading("DEM", text="DEM")
        tree.heading("Batch", text="Lot/Batch")
        tree.heading("Date Exp.", text="Date Expiration")
        tree.heading("Jours Restants", text="Jours Restants")
        tree.heading("Niveau", text="Niveau")
        tree.heading("Quantité", text="Quantité")
        
        tree.column("Article", width=180)
        tree.column("Code", width=80)
        tree.column("DEM", width=100)
        tree.column("Batch", width=100)
        tree.column("Date Exp.", width=100, anchor='center')
        tree.column("Jours Restants", width=120, anchor='center')
        tree.column("Niveau", width=100, anchor='center')
        tree.column("Quantité", width=80, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure tags for color coding
        tree.tag_configure('expire', background='#cc0000', foreground='white')  # Dark red
        tree.tag_configure('critique', background='#ff4444', foreground='white')  # Red
        tree.tag_configure('attention', background='#ffaa00')  # Orange
        tree.tag_configure('avertissement', background='#ffffcc')  # Light yellow
        
        # Insert data
        for alerte in alertes:
            niveau = alerte['niveau']
            days = alerte['days_left']
            
            # Choose tag based on level
            if niveau == 'EXPIRÉ':
                tag = 'expire'
                days_text = f"EXPIRÉ ({abs(days)} j)"
            elif niveau == 'CRITIQUE':
                tag = 'critique'
                days_text = f"{days} jours"
            elif niveau == 'ATTENTION':
                tag = 'attention'
                days_text = f"{days} jours"
            else:
                tag = 'avertissement'
                days_text = f"{days} jours"
            
            tree.insert('', 'end', values=(
                alerte['article'],
                alerte['code'],
                alerte['dem'],
                alerte['batch'],
                alerte['exp_date'],
                days_text,
                niveau,
                f"{alerte['quantity']:.1f}"
            ), tags=(tag,))

    def refresh_alertes(self):
        """Rafraîchit l'affichage des alertes"""
        self.afficher_alertes()

    