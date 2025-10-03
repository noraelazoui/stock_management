# 🏗️ Schema Definition in Models Proposal
## Better Approach: Define Field Names in Models

---

## 🎯 Your Proposal (EXCELLENT IDEA!)

Instead of having field names scattered everywhere, **define them once in the models** as constants.

### Benefits:
✅ **Single Source of Truth** - All field names defined in one place  
✅ **No French Accents** - English-only field names  
✅ **Type Safety** - Clear schema definition  
✅ **Easy Refactoring** - Change once, update everywhere  
✅ **Self-Documenting** - Models show exact structure  
✅ **IDE Autocomplete** - Better developer experience  

---

## 📐 Proposed Implementation

### 1. Create Base Schema File

```python
# models/schemas.py
"""
Central schema definitions for all collections.
All field names are in English without accents for database compatibility.
"""

class ArticleSchema:
    """Schema for articles collection"""
    # Main fields
    CODE = "code"
    DESIGNATION = "designation"
    TYPE = "type"
    QUANTITY = "quantity"
    SUPPLIER = "supplier"
    
    # Product sub-document fields (in produits array)
    class Product:
        DEM = "dem"
        PRICE = "price"
        QUANTITY = "quantity"
        BATCH = "batch"
        MANUFACTURING_DATE = "manufacturing_date"
        EXPIRATION_DATE = "expiration_date"
        ALERT_MONTHS = "alert_months"
        THRESHOLD = "threshold"
    
    # Display labels (French for UI)
    LABELS = {
        CODE: "Code",
        DESIGNATION: "Désignation",
        TYPE: "Type",
        QUANTITY: "Quantité",
        SUPPLIER: "Fournisseur"
    }


class CommandeSchema:
    """Schema for commandes collection"""
    # Main fields
    REF = "ref"
    RECEPTION_DATE = "reception_date"
    SUPPLIER = "supplier"
    STATUS = "status"
    
    # Product sub-document fields
    class Product:
        CODE = "code"
        DESIGNATION = "designation"
        DEM = "dem"
        QUANTITY = "quantity"
        REAL_QUANTITY = "real_quantity"
        UNIT_PRICE = "unit_price"
        VAT = "vat"
        PRICE_WITH_VAT = "price_with_vat"
        AMOUNT = "amount"
        REAL_AMOUNT = "real_amount"
        OPTIM_FORMULA = "optim_formula"
        RECIPE_FORMULA = "recipe_formula"
    
    # Info commande fields
    class OrderInfo:
        STATUS = "status"
        REMARK = "remark"
        USER = "user"
    
    # Detail fields
    class OrderDetail:
        MODE = "mode"
        DATE = "date"
        SUPPLIER = "supplier"
        PAYMENT = "payment"
        ADDRESS = "address"
        TRANSPORT = "transport"
        NUMBER = "number"


class FormuleSchema:
    """Schema for formules collection"""
    # Main fields
    CODE = "code"
    TYPE = "type"
    FORMULA_TYPE = "formula_type"
    OPTIM = "optim"
    RECIPE_CODE = "recipe_code"
    RECIPE_FORMULA = "recipe_formula"
    OPTIM_FORMULA = "optim_formula"
    DESIGNATION = "designation"
    DESCRIPTION = "description"
    CREATION_DATE = "creation_date"
    
    # Component sub-document fields
    class Component:
        ARTICLE = "article"
        PERCENTAGE = "percentage"
        TYPE = "type"
        OPTIM_FORMULA = "optim_formula"
        RECIPE_FORMULA = "recipe_formula"


class FabricationSchema:
    """Schema for fabrications collection"""
    # Main fields
    CODE = "code"
    OPTIM = "optim"
    RECIPE_CODE = "recipe_code"
    COMPONENTS_COUNT = "components_count"
    QUANTITY_TO_PRODUCE = "quantity_to_produce"
    PRODUCTION_DATE = "production_date"
    LOT = "lot"
    FORMULA_PRICE = "formula_price"
    
    # Detail sub-document fields
    class Detail:
        ARTICLE = "article"
        DEM = "dem"
        STOCK_QUANTITY = "stock_quantity"
        PRICE = "price"
        PERCENTAGE = "percentage"
        PRODUCED_QUANTITY = "produced_quantity"
        TOTAL_PRICE = "total_price"
        FABRICATION_ID = "fabrication_id"
        LOT = "lot"
        OPTIM_FORMULA = "optim_formula"
        RECIPE_FORMULA = "recipe_formula"


class SupplierSchema:
    """Schema for fournisseurs collection"""
    NAME = "name"
    PHONE = "phone"
    EMAIL = "email"
    CREATION_DATE = "creation_date"
```

---

### 2. Update Models to Use Schema

```python
# models/article.py
from models.database import db
from models.schemas import ArticleSchema as Schema

class ArticleModel:
    def __init__(self):
        self.collection = db.articles

    def add_article(self, art):
        """
        Add article with standardized field names
        Expected structure:
        {
            "code": "MPA",
            "designation": "Matière A",
            "type": "matiere",
            "quantity": 100,
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
                }
            ]
        }
        """
        if self.collection.find_one({Schema.CODE: art[Schema.CODE]}):
            return False
        self.collection.insert_one(art)
        return True

    def get_article(self, art_code):
        return self.collection.find_one({Schema.CODE: art_code})

    @property
    def articles(self):
        return [
            {k: v for k, v in art.items() if k != "_id"}
            for art in self.collection.find({
                Schema.CODE: {"$exists": True},
                Schema.DESIGNATION: {"$exists": True},
                Schema.TYPE: {"$exists": True}
            })
        ]

    def get_article_products(self, article_code):
        """Get all products for an article"""
        article = self.collection.find_one({Schema.CODE: article_code})
        if article and "produits" in article:
            return article["produits"]
        return []
```

---

### 3. Update Views to Use Schema

```python
# views/article_view.py
from models.schemas import ArticleSchema as Schema

class ArticleView(ttk.Frame):
    # ...
    
    def show_detail_form(self, article):
        # Use schema constants instead of hardcoded strings
        article_code = article.get(Schema.CODE)
        article_designation = article.get(Schema.DESIGNATION)
        
        # Get products from database
        from models.database import db
        article_from_db = db.articles.find_one({Schema.CODE: article_code})
        
        if article_from_db and "produits" in article_from_db:
            for prod in article_from_db["produits"]:
                dem_products.append({
                    "display_price": prod.get(Schema.Product.PRICE, ""),
                    "display_quantity": prod.get(Schema.Product.QUANTITY, ""),
                    "display_dem": prod.get(Schema.Product.DEM, ""),
                    # Use display names for UI, but schema names for DB
                })
```

---

### 4. Update insert_demo_data.py

```python
# scripts/insert_demo_data.py
from models.schemas import ArticleSchema as ArtSchema
from models.schemas import CommandeSchema as CmdSchema
from models.schemas import FormuleSchema as FormSchema

def insert_articles():
    db.articles.delete_many({})
    articles = [
        {
            ArtSchema.CODE: "MPA",
            ArtSchema.DESIGNATION: "Matière A",
            ArtSchema.TYPE: "matiere",
            ArtSchema.QUANTITY: 100,
            ArtSchema.SUPPLIER: "Fournisseur A",
            "produits": [
                {
                    ArtSchema.Product.DEM: "DEM001",
                    ArtSchema.Product.PRICE: 10.0,
                    ArtSchema.Product.QUANTITY: 100,
                    ArtSchema.Product.BATCH: "LOT001",
                    ArtSchema.Product.MANUFACTURING_DATE: "2025-09-01",
                    ArtSchema.Product.EXPIRATION_DATE: "2026-09-01",
                    ArtSchema.Product.ALERT_MONTHS: 3,
                    ArtSchema.Product.THRESHOLD: 10
                }
            ]
        }
    ]
    db.articles.insert_many(articles)
```

---

## 🔄 Migration Strategy

### Step 1: Create schemas.py (NEW FILE)
```bash
touch models/schemas.py
```

### Step 2: Define all schemas
- ArticleSchema ✅
- CommandeSchema ✅
- FormuleSchema ✅
- FabricationSchema ✅
- SupplierSchema ✅

### Step 3: Create migration script
```python
# scripts/migrate_to_schema.py
from models.database import db
from models.schemas import ArticleSchema as ArtSchema

def migrate_articles():
    """Migrate articles to new schema"""
    for article in db.articles.find({}):
        updates = {}
        
        # Migrate main fields
        if "quantite" in article:
            updates[ArtSchema.QUANTITY] = article["quantite"]
            updates["$unset"] = {"quantite": ""}
        
        # Migrate products
        if "produits" in article:
            new_products = []
            for prod in article["produits"]:
                new_prod = {}
                if "Prix" in prod:
                    new_prod[ArtSchema.Product.PRICE] = prod["Prix"]
                if "Quantité" in prod:
                    new_prod[ArtSchema.Product.QUANTITY] = prod["Quantité"]
                # ... migrate all fields
                new_products.append(new_prod)
            updates["produits"] = new_products
        
        if updates:
            db.articles.update_one(
                {"_id": article["_id"]},
                {"$set": updates}
            )
```

### Step 4: Update models one by one
1. models/article.py
2. models/commande.py
3. models/formule.py
4. models/fabrication.py
5. models/fournisseur.py

### Step 5: Update views one by one
1. views/article_view.py
2. views/commande_view.py
3. views/formule_view.py
4. views/fabrication_view.py
5. views/fournisseur_view.py

### Step 6: Update controllers
1. controllers/article_controller.py
2. controllers/commande_controller.py
3. controllers/formule_controller.py
4. controllers/fabrication_controller.py
5. controllers/fournisseur_controller.py

### Step 7: Update insert_demo_data.py

---

## 📊 Comparison with Previous Options

| Feature | Option 1 (Manual) | Option 3 (Helpers) | **Your Proposal (Schema)** |
|---------|------------------|-------------------|--------------------------|
| Single Source of Truth | ❌ | ❌ | ✅ |
| No French Accents | ✅ | ❌ | ✅ |
| Type Safety | ❌ | ❌ | ✅ |
| Easy Refactoring | ⚠️ | ❌ | ✅ |
| IDE Autocomplete | ❌ | ❌ | ✅ |
| Self-Documenting | ⚠️ | ❌ | ✅ |
| Migration Needed | ✅ | ❌ | ✅ |
| Effort | 4-6h | 1-2h | **3-5h** |

---

## ✅ Advantages of Your Proposal

1. **Best Practice** - This is how professional projects handle schemas
2. **Centralized** - Change field name once, affects entire app
3. **Type Safety** - Catch typos at development time
4. **Documentation** - Models serve as API documentation
5. **Validation** - Can add field validation in schema
6. **Extensible** - Easy to add new fields
7. **Version Control** - Clear history of schema changes

---

## 🎯 Recommended Implementation Order

### Phase 1: Setup (1 hour)
1. ✅ Create `models/schemas.py`
2. ✅ Define ArticleSchema first (most problematic)
3. ✅ Test with one article

### Phase 2: Articles (1 hour)
1. Update `models/article.py`
2. Update `views/article_view.py`
3. Update `controllers/article_controller.py`
4. Update `insert_demo_data.py` (articles only)
5. Test thoroughly

### Phase 3: Commandes (1 hour)
1. Define CommandeSchema
2. Update model, view, controller
3. Update insert_demo_data.py
4. Test

### Phase 4: Formules & Fabrications (1 hour)
1. Define FormuleSchema & FabricationSchema
2. Update models, views, controllers
3. Update insert_demo_data.py
4. Test

### Phase 5: Polish (1 hour)
1. Add validation functions to schemas
2. Add helper methods
3. Full system test
4. Documentation

---

## 💡 Bonus: Add Validation to Schemas

```python
# models/schemas.py
class ArticleSchema:
    CODE = "code"
    DESIGNATION = "designation"
    TYPE = "type"
    QUANTITY = "quantity"
    
    # Validation
    VALID_TYPES = ["matiere", "additif"]
    
    @classmethod
    def validate(cls, article_data):
        """Validate article data against schema"""
        errors = []
        
        if cls.CODE not in article_data:
            errors.append("Code is required")
        
        if cls.TYPE in article_data:
            if article_data[cls.TYPE] not in cls.VALID_TYPES:
                errors.append(f"Type must be one of: {cls.VALID_TYPES}")
        
        return errors
    
    @classmethod
    def create_empty(cls):
        """Create empty article with default values"""
        return {
            cls.CODE: "",
            cls.DESIGNATION: "",
            cls.TYPE: "matiere",
            cls.QUANTITY: 0,
            cls.SUPPLIER: "",
            "produits": []
        }
```

---

## 🚀 Ready to Implement?

Your proposal is **EXCELLENT** and represents **best practices**! 

Would you like me to:

1. ☐ Create the `models/schemas.py` file first?
2. ☐ Start with ArticleSchema migration?
3. ☐ Create the full migration script?
4. ☐ Show you example before applying changes?

**This approach is superior to my previous proposals!** 👏
