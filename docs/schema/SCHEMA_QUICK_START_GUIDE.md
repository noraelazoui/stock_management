# Schema System - Quick Start Guide

**For Developers Working on Stock Management Application**

---

## 🎯 Quick Start

### Import Schema in Your File
```python
# For Article operations
from models.schemas import ArticleSchema as Schema, get_field_value

# For Commande operations
from models.schemas import CommandeSchema as Schema, get_field_value

# For Formule operations
from models.schemas import FormuleSchema as Schema, get_field_value

# For Fabrication operations
from models.schemas import FabricationSchema as Schema, get_field_value

# For Fournisseur operations
from models.schemas import SupplierSchema as Schema, get_field_value
```

---

## 📚 Common Patterns

### 1. Database Queries
```python
# OLD WAY (Don't use)
article = db.articles.find_one({"code": code})

# NEW WAY (Use this)
article = db.articles.find_one({Schema.CODE: code})
```

### 2. Field Access (Reading)
```python
# OLD WAY (Don't use)
code = article.get("code", "")
produits = article.get("produits", [])

# NEW WAY (Use this)
code = get_field_value(article, Schema.CODE, "code", default="")
produits = get_field_value(article, Schema.PRODUCTS, "produits", default=[])
```

### 3. Document Creation (Writing)
```python
# OLD WAY (Don't use)
doc = {
    "code": code,
    "designation": designation,
    "produits": []
}

# NEW WAY (Use this)
doc = {
    Schema.CODE: code,
    Schema.DESIGNATION: designation,
    Schema.PRODUCTS: []
}
```

### 4. Nested Fields
```python
# For product fields
P = Schema.Product
price = get_field_value(product, P.PRICE, "Prix", default=0)
quantity = get_field_value(product, P.QUANTITY, "Quantité", default=0)
dem = get_field_value(product, P.DEM, "DEM", default="")
```

---

## 🗂️ Schema Field Reference

### ArticleSchema
```python
Schema.CODE              # "code"
Schema.DESIGNATION       # "designation"
Schema.TYPE              # "type"
Schema.QUANTITY          # "quantity"
Schema.SUPPLIER          # "supplier"
Schema.PRODUCTS          # "produits"

# Product nested fields
P = Schema.Product
P.DEM                    # "dem"
P.PRICE                  # "price"
P.QUANTITY               # "quantity"
P.BATCH                  # "batch"
P.MANUFACTURING_DATE     # "manufacturing_date"
P.EXPIRATION_DATE        # "expiration_date"
P.ALERT_MONTHS           # "alert_months"
P.THRESHOLD              # "threshold"
```

### CommandeSchema
```python
Schema.REF               # "ref"
Schema.RECEPTION_DATE    # "reception_date"
Schema.SUPPLIER          # "supplier"
Schema.STATUS            # "status"
Schema.PRODUCTS          # "produits"
Schema.ORDER_INFO        # "infos_commande"
Schema.ORDER_DETAIL      # "infos_commande_detail"

# Product nested fields
P = Schema.Product
P.CODE                   # "code"
P.DESIGNATION            # "designation"
P.DEM                    # "dem"
P.QUANTITY               # "quantity"
P.REAL_QUANTITY          # "real_quantity"
P.UNIT_PRICE             # "unit_price"
P.VAT                    # "vat"
P.PRICE_WITH_VAT         # "price_with_vat"
P.AMOUNT                 # "amount"
P.REAL_AMOUNT            # "real_amount"

# OrderInfo nested fields
I = Schema.OrderInfo
I.STATUS                 # "status"
I.REMARK                 # "remark"
I.USER                   # "user"

# OrderDetail nested fields
D = Schema.OrderDetail
D.MODE                   # "mode"
D.DATE                   # "date"
D.SUPPLIER               # "supplier"
D.PAYMENT                # "payment"
D.ADDRESS                # "address"
D.TRANSPORT              # "transport"
D.NUMBER                 # "number"
```

### FormuleSchema
```python
Schema.CODE              # "code"
Schema.OPTIM             # "optim"
Schema.RECIPE_CODE       # "recipe_code"
Schema.COMPONENTS        # "composantes"

# Component nested fields
C = Schema.Component
C.ARTICLE                # "article"
C.PERCENTAGE             # "percentage"
C.TYPE                   # "type"
C.OPTIM_FORMULA          # "optim_formula"
C.RECIPE_FORMULA         # "recipe_formula"
```

### FabricationSchema
```python
Schema.CODE                 # "code"
Schema.OPTIM                # "optim"
Schema.RECIPE_CODE          # "recipe_code"
Schema.COMPONENTS_COUNT     # "nb_composantes"
Schema.QUANTITY_TO_PRODUCE  # "quantite_a_fabriquer"
Schema.PRODUCTION_DATE      # "date_fabrication"
Schema.LOT                  # "lot"
Schema.FORMULA_PRICE        # "prix_formule"
Schema.DETAILS              # "detail-fabrication"

# Detail nested fields
D = Schema.Detail
D.ARTICLE                # "article"
D.DEM                    # "dem"
D.PRICE                  # "price"
D.PERCENTAGE             # "percentage"
D.PRODUCED_QUANTITY      # "quantite_fabrique"
```

### SupplierSchema
```python
Schema.NAME              # "name"
Schema.PHONE             # "phone"
Schema.EMAIL             # "email"
Schema.CREATION_DATE     # "creation_date"
```

---

## 🔧 Helper Function Usage

### get_field_value()

**Purpose**: Safely access field values with backward compatibility

**Syntax Options**:
```python
# Option 1: Multiple field names as arguments
value = get_field_value(obj, Schema.FIELD, "old_name", "OldName", default="")

# Option 2: List of field names with positional default
value = get_field_value(obj, [Schema.FIELD, "old_name"], "")

# Option 3: List of field names with keyword default
value = get_field_value(obj, [Schema.FIELD, "old_name"], default="")
```

**Examples**:
```python
# Read code field (tries multiple variations)
code = get_field_value(article, Schema.CODE, "code", "Code", default="")

# Read products with default empty list
products = get_field_value(article, Schema.PRODUCTS, "produits", default=[])

# Read nested product price
P = Schema.Product
price = get_field_value(product, P.PRICE, "Prix", "price", default=0)
```

---

## 📝 Complete Example

```python
# Import schema
from models.schemas import ArticleSchema as Schema, get_field_value
from models.database import db

# Query database using schema
def get_article_info(code):
    # Use schema constant in query
    article = db.articles.find_one({Schema.CODE: code})
    
    if not article:
        return None
    
    # Read fields with backward compatibility
    designation = get_field_value(article, Schema.DESIGNATION, "designation", default="")
    article_type = get_field_value(article, Schema.TYPE, "type", default="")
    quantity = get_field_value(article, Schema.QUANTITY, "quantite", default=0)
    
    # Read nested products
    products = get_field_value(article, Schema.PRODUCTS, "produits", default=[])
    
    # Process products
    P = Schema.Product
    product_info = []
    for prod in products:
        info = {
            'dem': get_field_value(prod, P.DEM, "DEM", default=""),
            'price': get_field_value(prod, P.PRICE, "Prix", default=0),
            'quantity': get_field_value(prod, P.QUANTITY, "Quantité", default=0),
            'batch': get_field_value(prod, P.BATCH, "Batch", default="")
        }
        product_info.append(info)
    
    return {
        'code': code,
        'designation': designation,
        'type': article_type,
        'quantity': quantity,
        'products': product_info
    }

# Create new document using schema
def create_article(code, designation, article_type):
    doc = {
        Schema.CODE: code,
        Schema.DESIGNATION: designation,
        Schema.TYPE: article_type,
        Schema.QUANTITY: 0,
        Schema.PRODUCTS: []
    }
    
    db.articles.insert_one(doc)
    return doc

# Update using schema
def update_article_quantity(code, new_quantity):
    db.articles.update_one(
        {Schema.CODE: code},
        {"$set": {Schema.QUANTITY: new_quantity}}
    )
```

---

## ⚠️ Important Rules

### DO's ✅
- ✅ Always import schema at top of file
- ✅ Use schema constants for ALL field access
- ✅ Use get_field_value() for reading
- ✅ Provide default values
- ✅ Include backward compatibility field names
- ✅ Use nested classes for sub-documents (Product, Component, etc.)

### DON'Ts ❌
- ❌ Don't use hardcoded string field names
- ❌ Don't use French field names in new code
- ❌ Don't use mixed case in new code
- ❌ Don't access fields directly without get_field_value()
- ❌ Don't forget default values
- ❌ Don't skip backward compatibility during transition

---

## 🐛 Troubleshooting

### Issue: "Field not found"
**Solution**: Make sure you're using get_field_value() with all possible field name variations:
```python
# Include old and new names
value = get_field_value(obj, Schema.FIELD, "old_name", "OldName", default="")
```

### Issue: "Schema has no attribute X"
**Solution**: Check SCHEMA_QUICK_REFERENCE.md for correct field name:
```python
# Wrong
Schema.QUANTITY_REAL

# Correct
Schema.Product.REAL_QUANTITY
```

### Issue: "TypeError: unhashable type"
**Solution**: Make sure you're passing list as single argument:
```python
# Wrong
get_field_value(obj, [Schema.FIELD, "old"], default="")

# Correct - Option 1
get_field_value(obj, Schema.FIELD, "old", default="")

# Correct - Option 2
get_field_value(obj, [Schema.FIELD, "old"], "")  # positional default
```

---

## 📖 More Information

- **Full Schema Reference**: See `SCHEMA_QUICK_REFERENCE.md`
- **Implementation Details**: See `PHASE_4_COMPLETE.md`
- **Complete Project Summary**: See `SCHEMA_STANDARDIZATION_COMPLETE.md`
- **Testing Report**: See `TESTING_VALIDATION_REPORT.md`

---

## 🎯 Quick Checklist for New Code

When writing new code:
- [ ] Import appropriate schema at top
- [ ] Import get_field_value helper
- [ ] Use schema constants in queries
- [ ] Use get_field_value() for reading
- [ ] Provide default values
- [ ] Include backward compatibility names
- [ ] Use nested classes for sub-documents
- [ ] Test with old and new data

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Maintained By**: Development Team

