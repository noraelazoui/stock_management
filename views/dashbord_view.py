# view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

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



        # Nouveaux onglets : Stock Article, Stock Fabrication et Inventaire de stock
        self.tab_stock_article = ttk.Frame(self.notebook)
        self.tab_stock_fabrication = ttk.Frame(self.notebook)
        self.tab_inventaire_stock = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_stock_article, text="Stock Article")
        self.notebook.add(self.tab_stock_fabrication, text="Stock Fabrication")
        self.notebook.add(self.tab_inventaire_stock, text="Inventaire de stock")

        # Responsive layout uniquement pour les deux onglets principaux
        for tab in [self.tab_stock_article, self.tab_stock_fabrication]:
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)

        # Bouton Actualiser pour Stock Article
        self.btn_actualiser_article = ttk.Button(self.tab_stock_article, text="Actualiser", command=self.refresh_stock_article)
        self.btn_actualiser_article.pack(anchor="ne", padx=10, pady=8)

        # Bouton Actualiser pour Stock Fabrication
        self.btn_actualiser_fabrication = ttk.Button(self.tab_stock_fabrication, text="Actualiser", command=self.refresh_stock_fabrication)
        self.btn_actualiser_fabrication.pack(anchor="ne", padx=10, pady=8)

        # Bouton Actualiser pour Inventaire de stock
        self.btn_actualiser_inventaire = ttk.Button(self.tab_inventaire_stock, text="Actualiser", command=self.refresh_inventaire_stock)
        self.btn_actualiser_inventaire.pack(anchor="ne", padx=10, pady=8)

        # Chargement des tableaux dans les onglets
        self.afficher_stock_article()
        self.afficher_stock_fabrication()
        self.afficher_inventaire_stock()
    def refresh_inventaire_stock(self):
        # Efface le contenu de l'onglet et recharge
        for widget in self.tab_inventaire_stock.winfo_children():
            if widget != self.btn_actualiser_inventaire:
                widget.destroy()
        self.afficher_inventaire_stock()

    def afficher_inventaire_stock(self):
        """
        Affiche la liste complète des articles dans l'onglet Inventaire de stock
        """
        articles = self.controller.get_inventaire()
        columns = ("Code", "Désignation", "Type", "Quantité", "Prix")
        tree = ttk.Treeview(self.tab_inventaire_stock, columns=columns, show="headings", height=18)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        for art in articles:
            tree.insert("", "end", values=(
                art.get("code", "-"),
                art.get("designation", art.get("name", "-")),
                art.get("type", "-"),
                art.get("quantite", art.get("quantity", 0)),
                art.get("prix", "-")
            ))
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def refresh_stock_article(self):
        # Efface le contenu de l'onglet et recharge
        for widget in self.tab_stock_article.winfo_children():
            if widget != self.btn_actualiser_article:
                widget.destroy()
        self.afficher_stock_article()

    def refresh_stock_fabrication(self):
        # Efface le contenu de l'onglet et recharge
        for widget in self.tab_stock_fabrication.winfo_children():
            if widget != self.btn_actualiser_fabrication:
                widget.destroy()
        self.afficher_stock_fabrication()

    def afficher_stock_article(self):
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
            ax.set_xticklabels(noms, rotation=45, ha="right", fontsize=13)
        else:
            ax.set_xticklabels(noms, fontsize=13)

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

    def afficher_stock_fabrication(self):
        """
        Affiche la liste des fabrications dans l'onglet Stock Fabrication
        """
        columns = ("Code", "Optim", "Recette", "Nb Composantes", "Quantité à fabriquer", "Date Fabrication", "Lot", "Prix Formule")
        tree = ttk.Treeview(self.tab_stock_fabrication, columns=columns, show="headings", height=16)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Import FabricationController ici pour éviter les imports circulaires
        from controllers.fabrication_controller import FabricationController
        fabrication_controller = FabricationController()
        fabrications = fabrication_controller.get_all_fabrications()
        codes = []
        quantites = []
        dates = []
        for fab in fabrications:
            tree.insert("", "end", values=(
                fab.get("code", "-"),
                fab.get("optim", "-"),
                fab.get("recette_code", "-"),
                fab.get("nb_composantes", "-"),
                fab.get("quantite_a_fabriquer", "-"),
                fab.get("date_fabrication", "-"),
                fab.get("lot", "-"),
                fab.get("prix_formule", "-")
            ))
            codes.append(fab.get("code", "-"))
            try:
                quantites.append(float(fab.get("quantite_a_fabriquer", 0)))
            except Exception:
                quantites.append(0)
            dates.append(str(fab.get("date_fabrication", "-")))

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
            ax.set_xticklabels(codes, rotation=45, ha="right", fontsize=13)
        else:
            ax.set_xticklabels(codes, fontsize=13)

        mplcursors.cursor(bars, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{codes[sel.index]}: {quantites[sel.index]}\n{dates[sel.index]}") )

        canvas = FigureCanvasTkAgg(fig, master=self.tab_stock_fabrication)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.X, padx=30, pady=8)

    