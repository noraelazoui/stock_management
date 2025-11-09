import tkinter as tk
from tkinter import ttk, messagebox

class GestionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application de Gestion")
        
        # Get screen dimensions
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Set window to maximized but keep window decorations and taskbar visible
        # Leave some space for taskbar (typically 40-50px)
        taskbar_height = 50
        window_height = screen_height - taskbar_height
        self.geometry(f"{screen_width}x{window_height}+0+0")
        
        # Allow window resizing
        self.resizable(True, True)
        
        # Try to maximize window (platform specific) - this keeps taskbar visible
        try:
            self.state('zoomed')  # For Windows and some Linux systems
        except:
            pass  # Use geometry setting above as fallback
        
        # Add close button functionality
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Liste partagée des articles
        self.articles = []

        # Liste partagée des fournisseurs
        self.fournisseurs = []

        # Barre d’outils (optionnelle)
        self.toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Création des onglets
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill='both')
        self.create_tabs()
        
        # Bind click event to close DateEntry popups when clicking outside
        self.bind_all("<Button-1>", self._on_click, add="+")

        # Barre de statut
        self.status = tk.StringVar(value="Prêt")
        status_bar = tk.Label(self, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Menu principal
        self.create_menu()

        # Couleurs professionnelles harmonisées
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook.Tab", background="#2C3E50", foreground="white")
        style.map("TNotebook.Tab", background=[("selected", "#586E86")], foreground=[("selected", "#33C435")])
        style.configure("TFrame", background="#F4F4F4")
        style.configure("TLabel", background="#ECF0F1", foreground="#222222", font=("Arial", 11))
        style.configure("TButton", background="#2C3E50", foreground="white")
        style.map("TButton", background=[("active", "#34495E")])
        style.configure("TLabelframe", background="#ECF0F1")
        style.configure("TLabelframe.Label", background="#F4F4F4", foreground="#222222",font=("Arial", 11,"bold"))
        self.configure(bg="#F4F4F4")

        # Synchronisation CommandeView <-> Fournisseurs
        self.commande_view = None

        # Ajout callback pour synchronisation articles
        self.on_add_article = None

        # Synchronisation FormuleView <-> Articles
        self.formule_view = None

    # -------------------------
    # Window Control
    # -------------------------
    def on_closing(self):
        """Handle window close button click"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application ?"):
            self.destroy()
    
    def _on_click(self, event):
        """Close DateEntry popups when clicking outside of them"""
        try:
            widget = event.widget
            
            # Check if click is inside a DateEntry or its popup
            from tkcalendar import DateEntry
            
            # Get the widget that was clicked
            current = widget
            is_dateentry_related = False
            
            # Check if we clicked on a DateEntry or inside a calendar popup
            while current:
                if isinstance(current, DateEntry):
                    is_dateentry_related = True
                    break
                # Check if it's a Toplevel (calendar popup)
                if isinstance(current, tk.Toplevel):
                    # Check if this toplevel contains calendar widgets
                    for child in current.winfo_children():
                        if 'Calendar' in str(type(child).__name__):
                            is_dateentry_related = True
                            break
                    break
                try:
                    current = current.master
                except:
                    break
            
            # If click is outside DateEntry, close all calendar popups
            if not is_dateentry_related:
                self._close_all_calendar_popups()
        except:
            pass
    
    def _close_all_calendar_popups(self):
        """Close all open DateEntry calendar popups"""
        try:
            # Find all Toplevel windows that are calendar popups
            for widget in self.winfo_children():
                self._find_and_close_calendars(widget)
        except:
            pass
    
    def _find_and_close_calendars(self, widget):
        """Recursively find and close calendar popups"""
        try:
            from tkcalendar import DateEntry
            
            if isinstance(widget, DateEntry):
                # Check if it has an open popup
                if hasattr(widget, '_top_cal') and widget._top_cal:
                    try:
                        if widget._top_cal.winfo_exists():
                            widget._top_cal.withdraw()
                    except:
                        pass
            
            # Check children recursively
            for child in widget.winfo_children():
                self._find_and_close_calendars(child)
        except:
            pass

    # -------------------------
    # Menu
    # -------------------------
    def create_menu(self):
        # Suppression du menu principal (Fichier, Édition, Aide)
        pass

    # -------------------------
    # Onglets
    # -------------------------
    def create_tabs(self):
        # Onglet Articles
        self.article_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.article_tab, text='Articles')
        self.init_article_tab()

        # Onglet Formules
        self.formule_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.formule_tab, text='Formules')
        self.init_formule_tab()

        # Onglet Commandes
        self.commande_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.commande_tab, text='Commandes')
        self.init_commande_tab()

        # Onglet Fabrication
        self.fabrication_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.fabrication_tab, text='Fabrication')
        self.init_fabrication_tab()

        # Onglet Fournisseurs
        self.fournisseur_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.fournisseur_tab, text='Fournisseurs')
        self.init_fournisseur_tab()

    def init_fournisseur_tab(self):
        from models.fournisseur import FournisseurModel
        from views.fournisseur_view import FournisseurView
        from controllers.fournisseur_controller import FournisseurController

        model = FournisseurModel()
        view = FournisseurView(self.fournisseur_tab)
        controller = FournisseurController(model, view)
        # Ajout callback pour synchronisation
        view.on_add_fournisseur = self.on_add_fournisseur

    # -------------------------
    # Initialisation des onglets
    # -------------------------
    def init_article_tab(self):
        from controllers.article_controller import ArticleController
        controller = ArticleController(self.article_tab, main_notebook=self.tab_control)
        controller.view.on_add_article = self.add_article_callback

    def init_formule_tab(self):
        from views.formule_view import FormuleView
        view = FormuleView(self.formule_tab, articles=self.articles)
        self.formule_view = view

    def init_commande_tab(self):
        """Initialise l'onglet Commandes en MVC"""
        from models.commande import CommandeModel
        from controllers.commande_controller import CommandeController
        from views.commande_view import CommandeView

        model = CommandeModel()
        view = CommandeView(self.commande_tab, main_notebook=self.tab_control)
        view.set_fournisseurs(self.fournisseurs)
        self.commande_view = view
        controller = CommandeController(model, view)

    def init_fabrication_tab(self):
        from views.fabrication_view import FabricationView
        self.fabrication_view = FabricationView(master=self.fabrication_tab)

    # -------------------------
    # Actions du menu
    # -------------------------
    def new_file(self):
        self.status.set("Nouveau fichier")
        messagebox.showinfo("Nouveau", "Créer un nouveau fichier")

    def open_file(self):
        self.status.set("Ouverture d'un fichier")
        messagebox.showinfo("Ouvrir", "Ouvrir un fichier")

    def show_about(self):
        messagebox.showinfo("À propos", "Application de gestion professionnelle\nVersion 1.0")

    def on_add_fournisseur(self, nom):
        self.fournisseurs.append(nom)
        if self.commande_view:
            self.commande_view.update_fournisseurs(self.fournisseurs)

    def add_article_callback(self, article):
        self.articles.append(article)
        if self.commande_view:
            self.commande_view.update_articles(self.articles)
        if self.formule_view:
            self.formule_view.update_articles(self.articles)


if __name__ == "__main__":
    app = GestionApp()
    app.mainloop()
