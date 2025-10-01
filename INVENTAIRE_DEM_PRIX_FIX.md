# Inventaire DEM and Prix Fix

**Date**: January 2025  
**Status**: ✅ Complete  
**Files Modified**: 1
- `views/dashbord_view.py` (+40 lines modified)

---

## 📋 Problem

User reported: "i cant see each dem and Prix unitaire"

The inventory tab was not showing DEM and Prix values because:
1. Articles in the database have a `produits` array containing multiple DEMs with prices
2. The code was looking for `dem` and `prix` at the article root level
3. Each article can have multiple products with different DEMs and prices

**Database Structure Discovered**:
```python
{
  "code": "MPA",
  "designation": "Matière A",
  "type": "matiere",
  "supplier": "Fournisseur A",
  "produits": [
    {
      "dem": "DEM001",
      "price": 10.0,
      "quantity": 100,
      "batch": "LOT001",
      "manufacturing_date": "2025-09-01",
      "expiration_date": "2026-09-01",
      "alert_months": 3,
      "threshold": 10
    },
    {
      "dem": "DEM002",
      "price": 11.0,
      "quantity": 50,
      "batch": "LOT002",
      ...
    }
  ]
}
```

---

## ✅ Solution

### 1. **Display Each DEM as Separate Row**

Changed the inventory display to iterate through the `produits` array and show each DEM as a separate row:

```python
for art in articles:
    produits = art.get("produits", [])
    
    if produits:
        # Display each DEM as a separate row
        for produit in produits:
            dem_value = produit.get("dem", "-")
            prix_value = produit.get("price", "-")
            quantite_value = produit.get("quantity", 0)
            
            item_id = self.inventaire_tree.insert("", "end", values=(
                art.get("code", "-"),
                art.get("designation", "-"),
                art.get("type", "-"),
                dem_value,          # ← Now shows DEM from product
                quantite_value,     # ← Quantity per DEM
                prix_value          # ← Price per DEM
            ))
```

### 2. **Store Combined Data**

Merged article data with product data for detail view:

```python
# Store full article data with product info
self.articles_data[item_id] = {
    **art,              # Article-level fields
    **produit,          # Product-level fields (DEM, price, etc.)
    "current_dem": dem_value  # Track which DEM is selected
}
```

### 3. **Updated Detail Display**

Enhanced the detail view to show product-specific information:

```python
# DEM (highlighted)
dem_value = article.get("current_dem") or article.get("dem", "-")

# Batch/Lot
if article.get("batch"):
    self.detail_text.insert(tk.END, "Lot: ", "label")
    self.detail_text.insert(tk.END, f"{article.get('batch')}\n\n", "value")

# Quantité - prioritize product quantity
quantite = article.get("quantity", article.get("quantite", 0))

# Prix - prioritize product price
prix = article.get("price", article.get("prix", "-"))

# Additional product fields
- Manufacturing date
- Expiration date
- Alert months
- Threshold
```

---

## 📊 Before and After

### Before (Not Working)
```
Code | Désignation | Type | DEM  | Quantité | Prix
─────┼─────────────┼──────┼──────┼──────────┼─────
MPA  | Matière A   | MP   | -    | 88       | -
MPB  | Matière B   | MP   | -    | 191.5    | -
```
❌ No DEM shown  
❌ No Prix shown  
❌ Only article-level data displayed

### After (Working)
```
Code | Désignation | Type | DEM     | Quantité | Prix
─────┼─────────────┼──────┼─────────┼──────────┼─────
MPA  | Matière A   | MP   | DEM001  | 100      | 10.0
MPA  | Matière A   | MP   | DEM002  | 50       | 11.0
MPA  | Matière A   | MP   | DEM003  | 30       | 12.0
MPB  | Matière B   | MP   | DEM004  | 200      | 12.0
MPB  | Matière B   | MP   | DEM005  | 80       | 13.0
```
✅ Each DEM shown as separate row  
✅ Prix unitaire displayed correctly  
✅ Quantity per DEM shown  
✅ Same article appears multiple times (one per DEM)

---

## 🎯 Key Changes

### 1. **Inventory Display Loop**

**Before**:
```python
for art in articles:
    dem_value = art.get("dem", "-")  # ❌ Not in article root
    prix = art.get("prix", "-")       # ❌ Not in article root
    
    item_id = self.inventaire_tree.insert("", "end", values=(
        art.get("code"), art.get("designation"), art.get("type"),
        dem_value, art.get("quantite"), prix
    ))
```

**After**:
```python
for art in articles:
    produits = art.get("produits", [])
    
    if produits:
        for produit in produits:  # ✅ Iterate through products
            dem_value = produit.get("dem", "-")    # ✅ From product
            prix_value = produit.get("price", "-")  # ✅ From product
            quantite_value = produit.get("quantity", 0)  # ✅ Per DEM
            
            item_id = self.inventaire_tree.insert("", "end", values=(
                art.get("code"), art.get("designation"), art.get("type"),
                dem_value, quantite_value, prix_value
            ))
            # Store merged data
            self.articles_data[item_id] = {**art, **produit, "current_dem": dem_value}
```

### 2. **Detail View Fields**

Added product-specific fields to detail display:

```python
# New fields shown in detail view:
✅ DEM (highlighted)
✅ Lot/Batch
✅ Quantité en stock (per DEM)
✅ Prix unitaire (per DEM)
✅ Date de fabrication
✅ Date d'expiration
✅ Alerte (mois)
✅ Seuil minimal
✅ Fournisseur
```

### 3. **Data Priority**

When displaying values, prioritize product-level data over article-level:

```python
# Quantity: product first, then article
quantite = article.get("quantity", article.get("quantite", 0))

# Price: product first, then article
prix = article.get("price", article.get("prix", "-"))

# DEM: current_dem first, then other variations
dem_value = article.get("current_dem") or article.get("dem", "-")

# Supplier: fournisseur or supplier field
supplier = article.get("fournisseur") or article.get("supplier")
```

---

## 🧪 Testing Results

### Display Tests
- ✅ Each DEM appears as separate row
- ✅ DEM column shows correct values (DEM001, DEM002, etc.)
- ✅ Prix column shows correct prices (10.0, 11.0, 12.0, etc.)
- ✅ Quantité shows per-DEM quantity
- ✅ Same article code appears multiple times (correct)
- ✅ All columns aligned and readable

### Detail View Tests
- ✅ Clicking on DEM row shows correct details
- ✅ DEM highlighted in yellow/red
- ✅ Batch/Lot shown correctly
- ✅ Price shows product price
- ✅ Quantity shows product quantity
- ✅ Manufacturing and expiration dates displayed
- ✅ Alert months and threshold shown
- ✅ Supplier information displayed

### Data Structure Tests
- ✅ Articles with `produits` array: Display each product
- ✅ Articles without `produits` array: Fallback to article-level data
- ✅ Missing fields: Show "-" placeholder
- ✅ Multiple products per article: All shown correctly

---

## 💡 Benefits

### For Users
1. **See All DEMs**: Each DEM is now visible in the table
2. **See Prices**: Prix unitaire displayed for each DEM
3. **Detailed Information**: Click to see manufacturing dates, expiration, etc.
4. **Better Tracking**: Track quantity and price per DEM
5. **Complete View**: All product variations visible at a glance

### For System
1. **Accurate Data**: Shows actual database structure
2. **Flexible Design**: Handles articles with/without products array
3. **Scalable**: Works with any number of products per article
4. **Maintainable**: Clear data flow from database to display

---

## 📈 Example Usage

### Scenario: Check prices for different DEMs of MPA

1. **Open Inventaire de stock tab**
2. **View the table**:
   ```
   MPA | Matière A | matiere | DEM001 | 100 | 10.0
   MPA | Matière A | matiere | DEM002 | 50  | 11.0
   MPA | Matière A | matiere | DEM003 | 30  | 12.0
   ```
3. **Click on DEM002 row**
4. **See detailed information**:
   ```
   Article Sélectionné
   ========================================
   
   Code: MPA
   Désignation: Matière A
   Type: matiere
   
   DEM:  DEM002  ← Highlighted
   
   Lot: LOT002
   
   Quantité en stock: 50
   
   Prix unitaire: 11.0
   
   ========================================
   Informations supplémentaires
   
   Date de fabrication: 2025-09-15
   Date d'expiration: 2026-09-15
   Alerte (mois): 3
   Seuil minimal: 10
   Fournisseur: Fournisseur A
   ```

---

## 🔍 Technical Details

### Data Merging Strategy

Used Python's `**` unpacking to merge dictionaries:

```python
merged_data = {
    **art,          # Article fields: code, designation, type, supplier
    **produit,      # Product fields: dem, price, quantity, batch, dates
    "current_dem": dem_value  # Track which DEM for detail view
}
```

This creates a single dictionary with:
- All article-level fields
- All product-level fields
- A marker for the current DEM being displayed

### Fallback Mechanism

If an article doesn't have the `produits` array (old data or different structure):

```python
else:
    # Fallback: Display article without DEM details
    dem_value = art.get("dem") or art.get("DEM") or art.get("Dem", "-")
    
    item_id = self.inventaire_tree.insert("", "end", values=(
        art.get("code"), art.get("designation"), art.get("type"),
        dem_value, art.get("quantite", art.get("quantity", 0)),
        art.get("prix", art.get("price", "-"))
    ))
    self.articles_data[item_id] = art
```

This ensures backwards compatibility with different data structures.

---

## ✅ Verification

### Data in Database
```bash
python3 -c "
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['stock_manager']
articles = list(db.articles.find({}, {'_id': 0}).limit(1))
print(articles[0])
"
```

**Output**:
```python
{
  'code': 'MPA',
  'designation': 'Matière A',
  'produits': [
    {'dem': 'DEM001', 'price': 10.0, 'quantity': 100, 'batch': 'LOT001', ...},
    {'dem': 'DEM002', 'price': 11.0, 'quantity': 50, 'batch': 'LOT002', ...},
    {'dem': 'DEM003', 'price': 12.0, 'quantity': 30, 'batch': 'LOT003', ...}
  ],
  ...
}
```

### Display in Application
✅ Each DEM from `produits` array appears as separate row  
✅ Price from `produit.price` shown in Prix column  
✅ Quantity from `produit.quantity` shown per DEM

---

## 🎉 Conclusion

Successfully fixed the inventory display to show:
- ✅ **Each DEM** as a separate row in the table
- ✅ **Prix unitaire** from the product's price field
- ✅ **Quantity per DEM** instead of total article quantity
- ✅ **Batch/Lot information** in detail view
- ✅ **Manufacturing and expiration dates** in detail view
- ✅ **Comprehensive product tracking** per DEM

**Result**: Users can now see all DEMs with their respective prices and quantities in the Inventaire de stock tab!
