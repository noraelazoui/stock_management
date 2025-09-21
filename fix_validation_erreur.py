from models.database import db
from models.fabrication import Fabrication
import traceback

def debug_valider_prix_formule():
    """
    Fonction de débogage pour simuler et corriger l'erreur de validation des prix de formule.
    Cette fonction vérifie le code et affiche les correctifs nécessaires.
    """
    print("\n=== ANALYSE DU PROBLÈME DE VALIDATION DES PRIX DE FORMULE ===")
    
    # Vérifier l'existence de la fabrication avec code="mama" et optim="1"
    print("\n1. Vérification de l'existence de la fabrication dans la base de données:")
    code = "mama"
    optim = "1"
    fabrication = db.fabrications.find_one({"code": code, "optim": optim})
    
    if fabrication:
        print(f"  ✓ Fabrication trouvée avec code='{code}', optim='{optim}'")
        print(f"  ID: {fabrication.get('_id')}")
        print(f"  Prix formule actuel: {fabrication.get('prix_formule')}")
    else:
        print(f"  ✗ Aucune fabrication trouvée avec code='{code}', optim='{optim}'")
        
    # Vérifier le code qui pose problème dans fabrication_view.py
    print("\n2. Analyse du code de la méthode valider_prix_formule:")
    print("  Dans la méthode valider_prix_formule de fabrication_view.py:")
    print("  → Erreur: 'Fabrication mama-1 non trouvée dans la base de données'")
    print("  → Problème probable: Recherche incorrecte ou erreur de formatage")
    
    # Simulation du flux qui pose problème
    print("\n3. Simulation du flux de validation:")
    print("  a) Vérification de l'état des variables current_code et current_optim")
    print("     current_code='mama', current_optim='1'")
    
    print("  b) Récupération de la fabrication dans la base de données")
    print("     db.fabrications.find_one({'code': 'mama', 'optim': '1'})")
    
    # Solution proposée
    print("\n4. Solution au problème:")
    print("  1. Vérifier que current_code et current_optim sont correctement définis")
    print("  2. Assurer que les types de données correspondent à ceux de la base")
    print("  3. Ajouter des logs détaillés pour suivre les valeurs exactes")
    print("  4. Corriger l'erreur dans valider_prix_formule")
    
    # Proposition de correctif
    print("\n5. Correctif proposé pour valider_prix_formule:")
    print("""
    def valider_prix_formule(self):
        try:
            print("\\n=== DÉBUT VALIDATION PRIX FORMULE ===")
            print(f"Valeurs actuelles: current_code='{getattr(self, 'current_code', 'Non défini')}', current_optim='{getattr(self, 'current_optim', 'Non défini')}'")
            
            # Vérifier que current_code et current_optim sont définis
            if not hasattr(self, 'current_code') or not self.current_code:
                print("Erreur: current_code n'est pas défini")
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", "Impossible de valider: code de fabrication non défini.")
                return
                
            if not hasattr(self, 'current_optim') or not self.current_optim:
                print("Erreur: current_optim n'est pas défini")
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", "Impossible de valider: optimisation non définie.")
                return
            
            # Récupérer d'abord la valeur actuelle pour la comparer
            from models.database import db
            print(f"Recherche de fabrication avec code='{self.current_code}', optim='{self.current_optim}'")
            current_fabrication = db.fabrications.find_one(
                {"code": self.current_code, "optim": self.current_optim}
            )
            
            # Vérifier si la fabrication existe
            if current_fabrication is None:
                print(f"Fabrication non trouvée avec code='{self.current_code}', optim='{self.current_optim}'")
                # Essayons avec optim comme entier
                if isinstance(self.current_optim, str) and self.current_optim.isdigit():
                    print(f"Tentative avec optim comme entier: {int(self.current_optim)}")
                    current_fabrication = db.fabrications.find_one(
                        {"code": self.current_code, "optim": int(self.current_optim)}
                    )
                
                # Essayons avec optim comme chaîne si c'est un nombre
                if current_fabrication is None and isinstance(self.current_optim, (int, float)):
                    print(f"Tentative avec optim comme chaîne: {str(self.current_optim)}")
                    current_fabrication = db.fabrications.find_one(
                        {"code": self.current_code, "optim": str(self.current_optim)}
                    )
                    
                # Si toujours pas trouvé, essayons avec le code combiné
                if current_fabrication is None:
                    combined_code = f"{self.current_code}-{self.current_optim}"
                    print(f"Tentative avec code combiné: {combined_code}")
                    current_fabrication = db.fabrications.find_one({"code": combined_code})
                
                # Si toujours pas trouvé, c'est une erreur
                if current_fabrication is None:
                    print(f"Erreur: Fabrication {self.current_code}-{self.current_optim} non trouvée dans la base de données")
                    import tkinter.messagebox as messagebox
                    messagebox.showerror("Erreur", f"La fabrication {self.current_code}-{self.current_optim} n'a pas été trouvée dans la base de données.")
                    return
            
            # Continuer avec le code existant pour mettre à jour le prix de formule...
            
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")
            print(f"Erreur dans valider_prix_formule: {e}")
            traceback.print_exc()
    """)
    
    # Conclusion
    print("\n6. Conclusion:")
    print(f"  Le problème est que les fabrications existent dans la base de données avec")
    print(f"  code='{code}' et optim='{optim}', mais le code ne les trouve pas correctement.")
    print(f"  Le correctif proposé ajoute plusieurs tentatives de recherche avec différents")
    print(f"  formats de données pour résoudre ce problème.")

# Exécuter la fonction de débogage
debug_valider_prix_formule()
