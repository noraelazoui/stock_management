import sys
# Configure matplotlib backend BEFORE any other imports
import matplotlib
matplotlib.use('TkAgg')

# ...existing code...

from views.main_view import GestionApp
import tkinter as tk

# Suppression des articles de test


if __name__ == "__main__":
    app = GestionApp()
    app.mainloop()

