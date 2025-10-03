#!/usr/bin/env python3
"""
Test script to verify the crash fix is working
Run this to check if the application will start correctly
"""

import sys
import os

print("="*60)
print("STOCK MANAGEMENT APPLICATION - CRASH FIX VERIFICATION")
print("="*60)

# Test 1: Matplotlib backend configuration
print("\n1. Testing matplotlib backend configuration...")
try:
    import matplotlib
    matplotlib.use('TkAgg')
    print("   ✓ Matplotlib backend set to TkAgg")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# Test 2: Import dependencies
print("\n2. Testing dependencies...")
try:
    import tkinter as tk
    print("   ✓ Tkinter imported")
    
    import matplotlib.pyplot as plt
    print("   ✓ Matplotlib.pyplot imported")
    
    from tkcalendar import DateEntry
    print("   ✓ tkcalendar imported")
    
    from dateutil.relativedelta import relativedelta
    print("   ✓ python-dateutil imported")
    
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# Test 3: Database connection
print("\n3. Testing database connection...")
try:
    from models.database import db
    print("   ✓ Database connected")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# Test 4: Model imports
print("\n4. Testing model imports...")
try:
    from models.dashbord import StockModel
    model = StockModel()
    print("   ✓ StockModel created")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# Test 5: Alert system
print("\n5. Testing alert system...")
try:
    alertes = model.verifier_alertes()
    print(f"   ✓ Stock bas alerts: {len(alertes['stock_bas'])}")
    print(f"   ✓ Expiration alerts: {len(alertes['expiration'])}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# Test 6: Controller imports
print("\n6. Testing controller imports...")
try:
    from controllers.dashbord_controller import DashbordController
    controller = DashbordController()
    print("   ✓ DashbordController created")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# Test 7: View imports
print("\n7. Testing view imports...")
try:
    from views.dashbord_view import StockView
    print("   ✓ StockView imported")
    
    from views.main_view import GestionApp
    print("   ✓ GestionApp imported")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# Test 8: Tkinter window creation (minimal test)
print("\n8. Testing Tkinter window creation...")
try:
    root = tk.Tk()
    root.withdraw()  # Hide window
    root.title("Test")
    root.destroy()
    print("   ✓ Tkinter window created and destroyed successfully")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    sys.exit(1)

# All tests passed
print("\n" + "="*60)
print("✓✓✓ ALL TESTS PASSED! ✓✓✓")
print("="*60)
print("\nThe application should now run without crashes.")
print("\nTo start the application, run:")
print("  python3 main.py")
print("\nOr with virtual environment:")
print("  source venv/bin/activate")
print("  python3 main.py")
print("\n" + "="*60)
