# controller.py
from models.dashbord import StockModel
from views.dashbord_view import StockView

class StockController:
    def __init__(self):
        self.model = StockModel()
        self.view = StockView(self)

    def run(self):
        self.view.mainloop()

class DashbordController:
    def __init__(self):
        self.model = StockModel()

    def get_stock_premix(self):
        return self.model.get_stock_premix()

    def get_stock_usine(self):
        return self.model.get_stock_usine()

    def get_stock_global(self):
        return self.model.get_stock_global()

    def get_inventaire(self):
        return self.model.get_inventaire()

    def get_fournisseur(self, nom):
        return self.model.get_fournisseur(nom)

    def get_alertes(self):
        """Récupère les alertes de stock et d'expiration"""
        return self.model.verifier_alertes()
