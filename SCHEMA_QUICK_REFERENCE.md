# Quick Reference: Schema Implementation

## How to Use Schemas in Your Code

### 1. Import Schema at the Top of File
```python
# For articles
from models.schemas import ArticleSchema as Schema, get_field_value

# For commandes
from models.schemas import CommandeSchema as Schema, get_field_value

# For formules
from models.schemas import FormuleSchema as Schema, get_field_value

# For fabrications
from models.schemas import FabricationSchema as Schema, get_field_value

# For fournisseurs
from models.schemas import SupplierSchema as Schema, get_field_value
```

### 2. Access Fields Using Schema Constants

#### Simple Field Access
```python
# OLD WAY (avoid this)
code = article.get("code")

# NEW WAY (recommended)
code = article.get(Schema.CODE)
```

#### Field Access with Backward Compatibility
```python
# When you need to support old field names
code = get_field_value(article, Schema.CODE, "code", "Code", "CODE")

# This checks: article[Schema.CODE] or article["code"] or article["Code"] or article["CODE"]
# Returns first found value, or empty string if none found
```

### 3. Common Patterns

#### Reading Article Data
```python
from models.schemas import ArticleSchema as ASchema, get_field_value

article = db.articles.find_one({ASchema.CODE: "MPA"})
code = get_field_value(article, ASchema.CODE, "code")
designation = get_field_value(article, ASchema.DESIGNATION, "designation")
quantity = get_field_value(article, ASchema.QUANTITY, "quantite", "Quantité")
```

#### Reading Article Products
```python
from models.schemas import ArticleSchema as ASchema, get_field_value
P = ASchema.Product

for prod in article.get("produits", []):
    dem = get_field_value(prod, P.DEM, "DEM", "dem")
    price = get_field_value(prod, P.PRICE, "prix", "Prix", "price")
    quantity = get_field_value(prod, P.QUANTITY, "quantite", "Quantité", "quantity")
    batch = get_field_value(prod, P.BATCH, "lot", "Lot", "batch")
```

#### Reading Commande Products
```python
from models.schemas import CommandeSchema as CSchema, get_field_value
P = CSchema.Product

commande = db.commandes.find_one({CSchema.REFERENCE: "CMD001"})
produits = get_field_value(commande, CSchema.PRODUCTS, "produits", "products")

for prod in produits:
    code = get_field_value(prod, P.CODE, "code", "Code")
    dem = get_field_value(prod, P.DEM, "DEM", "dem")
    quantity = get_field_value(prod, P.QUANTITY, "quantite", "QUANTITE")
```

#### Reading Fabrication Data
```python
from models.schemas import FabricationSchema as FSchema, get_field_value

fab = db.fabrications.find_one({FSchema.CODE: "PREMIX1"})
code = get_field_value(fab, FSchema.CODE, "code")
optim = get_field_value(fab, FSchema.OPTIM, "optim")
recipe = get_field_value(fab, FSchema.RECIPE_CODE, "recette_code", "recette")
nb_comp = get_field_value(fab, FSchema.COMPONENTS_COUNT, "nb_composantes")
quantity = get_field_value(fab, FSchema.QUANTITY_TO_PRODUCE, "quantite_a_fabriquer")
```

#### Reading Fournisseur Data
```python
from models.schemas import SupplierSchema as SSchema, get_field_value

fournisseur = db.fournisseurs.find_one()
nom = get_field_value(fournisseur, SSchema.NAME, "Nom", "nom", "name")
telephone = get_field_value(fournisseur, SSchema.PHONE, "Téléphone", "telephone")
email = get_field_value(fournisseur, SSchema.EMAIL, "Email", "email")
```

### 4. Writing Data to Database

#### Create New Article with Products
```python
from models.schemas import ArticleSchema as ASchema
P = ASchema.Product

new_article = {
    ASchema.CODE: "MPA",
    ASchema.DESIGNATION: "Matière Première A",
    ASchema.TYPE: "matiere premiere",
    ASchema.QUANTITY: 100,
    ASchema.SUPPLIER: "Fournisseur A",
    "produits": [
        {
            P.DEM: "DEM001",
            P.PRICE: 10.0,
            P.QUANTITY: 100,
            P.BATCH: "LOT001",
            P.MANUFACTURING_DATE: "2025-01-15",
            P.EXPIRATION_DATE: "2026-01-15",
            P.ALERT_MONTHS: 2,
            P.THRESHOLD: 10
        }
    ]
}

db.articles.insert_one(new_article)
```

#### Create New Fabrication
```python
from models.schemas import FabricationSchema as FSchema

new_fab = {
    FSchema.CODE: "PREMIX1",
    FSchema.OPTIM: "1",
    FSchema.RECIPE_CODE: "R001",
    FSchema.COMPONENTS_COUNT: 2,
    FSchema.QUANTITY_TO_PRODUCE: 20,
    FSchema.PRODUCTION_DATE: "2025-10-01",
    FSchema.LOT: "L001",
    FSchema.FORMULA_PRICE: 11.4
}

db.fabrications.insert_one(new_fab)
```

### 5. Querying Database

#### Find with Schema Constants
```python
from models.schemas import ArticleSchema as ASchema

# Find article by code
article = db.articles.find_one({ASchema.CODE: "MPA"})

# Find articles by type
articles = db.articles.find({ASchema.TYPE: "matiere premiere"})

# Find articles with low quantity
articles = db.articles.find({ASchema.QUANTITY: {"$lt": 10}})
```

## All Schema Constants Reference

### ArticleSchema
- `CODE` = "code"
- `DESIGNATION` = "designation"
- `TYPE` = "type"
- `QUANTITY` = "quantity"
- `SUPPLIER` = "supplier"

#### ArticleSchema.Product
- `CODE` = "code"
- `DEM` = "dem"
- `PRICE` = "price"
- `QUANTITY` = "quantity"
- `BATCH` = "batch"
- `MANUFACTURING_DATE` = "manufacturing_date"
- `EXPIRATION_DATE` = "expiration_date"
- `ALERT_MONTHS` = "alert_months"
- `THRESHOLD` = "threshold"

### CommandeSchema
- `REFERENCE` = "reference"
- `DATE` = "date"
- `SUPPLIER` = "supplier"
- `PRODUCTS` = "products"
- `ORDER_INFO` = "order_info"
- `STATUS` = "status"
- `REMARKS` = "remarks"
- `USER` = "user"

#### CommandeSchema.Product
- `CODE` = "code"
- `DESIGNATION` = "designation"
- `DEM` = "dem"
- `QUANTITY` = "quantity"
- `ACTUAL_QUANTITY` = "actual_quantity"
- `UNIT_PRICE` = "unit_price"
- `TVA` = "tva"
- `TTC_PRICE` = "ttc_price"
- `AMOUNT` = "amount"
- `ACTUAL_AMOUNT` = "actual_amount"

### FormuleSchema
- `CODE` = "code"
- `TYPE` = "type"
- `FORMULA_TYPE` = "formula_type"
- `OPTIM` = "optim"
- `RECIPE_CODE` = "recipe_code"
- `DESIGNATION` = "designation"
- `DESCRIPTION` = "description"
- `CREATION_DATE` = "date_creation"
- `COMPONENTS` = "composantes"

#### FormuleSchema.Component
- `ARTICLE` = "article"
- `PERCENTAGE` = "percentage"
- `TYPE` = "type"
- `OPTIM_FORMULA` = "optim_formula"
- `RECIPE_FORMULA` = "recipe_formula"

### FabricationSchema
- `CODE` = "code"
- `OPTIM` = "optim"
- `RECIPE_CODE` = "recipe_code"
- `COMPONENTS_COUNT` = "nb_composantes"
- `QUANTITY_TO_PRODUCE` = "quantite_a_fabriquer"
- `PRODUCTION_DATE` = "date_fabrication"
- `LOT` = "lot"
- `FORMULA_PRICE` = "prix_formule"
- `DETAIL_FABRICATION` = "detail-fabrication"

#### FabricationSchema.Detail
- `ARTICLE` = "article"
- `DEM` = "dem"
- `STOCK_QUANTITY` = "quantite_stock"
- `PRICE` = "price"
- `PERCENTAGE` = "percentage"
- `PRODUCED_QUANTITY` = "quantite_fabrique"
- `TOTAL_PRICE` = "prix_total"

### SupplierSchema
- `NAME` = "name"
- `PHONE` = "phone"
- `EMAIL` = "email"
- `CREATION_DATE` = "creation_date"

## Tips & Best Practices

### ✅ DO
- Always import schema at top of file
- Use `get_field_value()` for reading data (backward compatibility)
- Use schema constants for writing new data
- Use schema constants in database queries
- Document which schema you're using in comments

### ❌ DON'T
- Don't hardcode field names as strings
- Don't use `.get("fieldname")` without backup field names
- Don't mix old and new field names in same function
- Don't forget to import `get_field_value` helper

### 🎯 When in Doubt
1. Check `models/schemas.py` for the exact constant name
2. Use your IDE's autocomplete (Schema. + Ctrl+Space)
3. Look at examples in updated view files
4. Refer to this quick reference guide

## Common Mistakes to Avoid

### Mistake 1: Wrong Schema Name
```python
# WRONG
Schema.COMPONENT_COUNT  # Doesn't exist in FabricationSchema

# CORRECT
Schema.COMPONENTS_COUNT  # Note the 'S'
```

### Mistake 2: Forgetting Nested Classes
```python
# WRONG
get_field_value(prod, Schema.PRICE)  # Schema doesn't have PRICE

# CORRECT
P = Schema.Product
get_field_value(prod, P.PRICE)  # Product class has PRICE
```

### Mistake 3: Not Using Backward Compatibility
```python
# WRONG (will break if old field names exist)
price = prod.get(P.PRICE)

# CORRECT (works with old and new field names)
price = get_field_value(prod, P.PRICE, "prix", "Prix", "price")
```

## Need Help?

1. **Check schema definition**: Open `models/schemas.py`
2. **Look at examples**: Check updated view files
3. **Test in Python shell**: Try field access patterns
4. **Read documentation**: See SCHEMA_IMPLEMENTATION_STATUS.md

---

**Remember**: The schema approach makes your code more maintainable, eliminates typos, and provides IDE autocomplete support. Use it everywhere!
