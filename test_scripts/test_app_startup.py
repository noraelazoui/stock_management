#!/usr/bin/env python3
"""
Quick test to verify the application starts without crashing
"""
import sys
import matplotlib
matplotlib.use('TkAgg')

print("="*60)
print("TESTING APPLICATION STARTUP")
print("="*60)

try:
    print("\n1. Importing main components...")
    from views.main_view import GestionApp
    print("   ✓ Main view imported")
    
    print("\n2. Testing dashboard components...")
    from controllers.dashbord_controller import DashbordController
    from views.dashbord_view import StockView
    print("   ✓ Dashboard components imported")
    
    print("\n3. Testing matplotlib charts...")
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    
    controller = DashbordController()
    view = StockView(controller, root)
    
    # Test all display methods
    view.afficher_stock_article()
    print("   ✓ Stock Article charts work")
    
    view.afficher_stock_fabrication()
    print("   ✓ Stock Fabrication charts work")
    
    view.afficher_alertes()
    print("   ✓ Alert Stock tab works")
    
    root.destroy()
    
    print("\n" + "="*60)
    print("✓✓✓ ALL TESTS PASSED ✓✓✓")
    print("="*60)
    print("\nThe application is ready to use!")
    print("\nTo start the application:")
    print("  python3 main.py")
    print("\n" + "="*60)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
