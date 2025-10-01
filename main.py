import sys
# ...existing code...

from views.main_view import GestionApp
import tkinter as tk

# Suppression des articles de test
import models.database as db
db.db.articles.delete_many({"name": "Test Article"})

if __name__ == "__main__":
    app = GestionApp()
    app.mainloop()

