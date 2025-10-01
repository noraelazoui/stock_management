"""
Central schema definitions for all MongoDB collections.
All field names are in English without accents for database compatibility.

This file serves as the single source of truth for all field names
used throughout the application.
"""


class ArticleSchema:
    """Schema for articles collection"""
    
    # Main article fields
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
    
    # Valid values
    VALID_TYPES = ["matiere", "additif", "matiere premiere"]
    
    # Display labels (French for UI)
    LABELS = {
        CODE: "Code",
        DESIGNATION: "Désignation",
        TYPE: "Type",
        QUANTITY: "Quantité",
        SUPPLIER: "Fournisseur"
    }
    
    PRODUCT_LABELS = {
        Product.DEM: "DEM",
        Product.PRICE: "Prix",
        Product.QUANTITY: "Quantité",
        Product.BATCH: "Batch",
        Product.MANUFACTURING_DATE: "Date fabrication",
        Product.EXPIRATION_DATE: "Date expiration",
        Product.ALERT_MONTHS: "Alerte",
        Product.THRESHOLD: "Seuil"
    }
    
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


class CommandeSchema:
    """Schema for commandes collection"""
    
    # Main commande fields
    REF = "ref"
    RECEPTION_DATE = "reception_date"
    SUPPLIER = "supplier"
    STATUS = "status"
    PRODUCTS = "produits"
    ORDER_INFO = "infos_commande"
    ORDER_DETAIL = "infos_commande_detail"
    
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
    
    # Info commande sub-document fields
    class OrderInfo:
        STATUS = "status"
        REMARK = "remark"
        USER = "user"
    
    # Detail sub-document fields
    class OrderDetail:
        MODE = "mode"
        DATE = "date"
        SUPPLIER = "supplier"
        PAYMENT = "payment"
        ADDRESS = "address"
        TRANSPORT = "transport"
        NUMBER = "number"
    
    # Valid statuses
    VALID_STATUSES = ["Créé", "En attente", "Validée", "Annulée"]
    
    # Display labels
    LABELS = {
        REF: "Référence",
        RECEPTION_DATE: "Date réception",
        SUPPLIER: "Fournisseur",
        STATUS: "Statut"
    }
    
    PRODUCT_LABELS = {
        Product.CODE: "Code",
        Product.DESIGNATION: "Désignation",
        Product.DEM: "DEM",
        Product.QUANTITY: "Quantité",
        Product.REAL_QUANTITY: "Quantité réelle",
        Product.UNIT_PRICE: "Prix unitaire",
        Product.VAT: "TVA",
        Product.PRICE_WITH_VAT: "Prix TTC",
        Product.AMOUNT: "Montant",
        Product.REAL_AMOUNT: "Montant réel"
    }


class FormuleSchema:
    """Schema for formules collection"""
    
    # Main formule fields
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
    COMPONENTS = "composantes"
    
    # Component sub-document fields
    class Component:
        ARTICLE = "article"
        PERCENTAGE = "percentage"
        TYPE = "type"
        OPTIM_FORMULA = "optim_formula"
        RECIPE_FORMULA = "recipe_formula"
    
    # Valid values
    VALID_TYPES = ["formule"]
    VALID_FORMULA_TYPES = ["simple", "mixte"]
    VALID_COMPONENT_TYPES = ["simple", "formule"]
    
    # Display labels
    LABELS = {
        CODE: "Code",
        TYPE: "Type",
        FORMULA_TYPE: "Type de formule",
        OPTIM: "Optim",
        RECIPE_CODE: "Code recette",
        DESIGNATION: "Désignation",
        DESCRIPTION: "Description",
        CREATION_DATE: "Date création"
    }


class FabricationSchema:
    """Schema for fabrications collection"""
    
    # Main fabrication fields
    ID = "_id"
    CODE = "code"
    OPTIM = "optim"
    RECIPE_CODE = "recipe_code"
    COMPONENTS_COUNT = "nb_composantes"
    QUANTITY_TO_PRODUCE = "quantite_a_fabriquer"
    PRODUCTION_DATE = "date_fabrication"
    LOT = "lot"
    FORMULA_PRICE = "prix_formule"
    DETAIL_FABRICATION = "detail-fabrication"
    
    # Detail sub-document fields
    class Detail:
        ARTICLE = "article"
        DEM = "dem"
        STOCK_QUANTITY = "quantite_stock"
        PRICE = "price"
        PERCENTAGE = "percentage"
        PRODUCED_QUANTITY = "quantite_fabrique"
        TOTAL_PRICE = "prix_total"
        FABRICATION_ID = "fabrication_id"
        LOT = "lot"
        OPTIM_FORMULA = "optim_formule"
        RECIPE_FORMULA = "recette_formule"
        # Legacy fields (keep for backward compatibility)
        OPTIM = "optim"
        RECIPE = "recette"
    
    # Display labels
    LABELS = {
        CODE: "Code",
        OPTIM: "Optim",
        RECIPE_CODE: "Code recette",
        COMPONENTS_COUNT: "Nb composantes",
        QUANTITY_TO_PRODUCE: "Quantité à fabriquer",
        PRODUCTION_DATE: "Date fabrication",
        LOT: "Lot",
        FORMULA_PRICE: "Prix formule"
    }
    
    DETAIL_LABELS = {
        Detail.ARTICLE: "Article",
        Detail.DEM: "DEM",
        Detail.STOCK_QUANTITY: "Stock",
        Detail.PRICE: "Prix",
        Detail.PERCENTAGE: "Pourcentage",
        Detail.PRODUCED_QUANTITY: "Quantité fabriquée",
        Detail.TOTAL_PRICE: "Prix total",
        Detail.LOT: "Lot",
        Detail.OPTIM_FORMULA: "Optim Formule",
        Detail.RECIPE_FORMULA: "Recette Formule"
    }


class SupplierSchema:
    """Schema for fournisseurs collection"""
    
    # Main supplier fields
    NAME = "name"
    PHONE = "phone"
    EMAIL = "email"
    CREATION_DATE = "creation_date"
    
    # Display labels
    LABELS = {
        NAME: "Nom",
        PHONE: "Téléphone",
        EMAIL: "Email",
        CREATION_DATE: "Date création"
    }
    
    @classmethod
    def create_empty(cls):
        """Create empty supplier with default values"""
        return {
            cls.NAME: "",
            cls.PHONE: "",
            cls.EMAIL: "",
            cls.CREATION_DATE: ""
        }


# Helper functions for backward compatibility
def get_field_value(obj, *args, **kwargs):
    """
    Get field value trying multiple field names (case-insensitive fallback).
    Tries exact match first, then case-insensitive search.
    
    Args:
        obj: Dictionary object to search
        *args: Field names to try, or a list of field names, optionally followed by default value
        **kwargs: Optional 'default' keyword argument
    
    Usage:
        price = get_field_value(product, Schema.PRICE, "Prix", "price", default=0)
        # OR
        price = get_field_value(product, [Schema.PRICE, "Prix"], default=0)
        # OR
        price = get_field_value(product, [Schema.PRICE, "Prix"], 0)  # positional default
    """
    # Extract default value (can be positional or keyword)
    default = kwargs.get('default', None)
    field_names = args
    
    # Handle: get_field_value(obj, [list], default)
    if len(args) >= 2 and isinstance(args[0], (list, tuple)) and not isinstance(args[1], (list, tuple)):
        field_names = args[0]
        default = args[1] if len(args) > 1 else default
    # Handle: get_field_value(obj, [list])
    elif len(args) == 1 and isinstance(args[0], (list, tuple)):
        field_names = args[0]
    # Handle: get_field_value(obj, field1, field2, ...)
    # field_names is already set to args
    
    for field_name in field_names:
        if isinstance(field_name, (list, tuple)):
            continue  # Skip if somehow a list got in
        if field_name in obj:
            return obj[field_name]
    
    # Case-insensitive fallback
    for field_name in field_names:
        if isinstance(field_name, (list, tuple)):
            continue
        field_lower = str(field_name).lower()
        for key in obj.keys():
            if str(key).lower() == field_lower:
                return obj[key]
    
    return default


def normalize_to_schema(obj, schema_mapping):
    """
    Normalize object field names to match schema.
    
    Args:
        obj: Dictionary to normalize
        schema_mapping: Dict mapping schema field names to possible old names
        
    Example:
        mapping = {
            ArticleSchema.Product.PRICE: ["Prix", "price", "PRICE"],
            ArticleSchema.Product.QUANTITY: ["Quantité", "quantite", "QUANTITE"]
        }
        normalized = normalize_to_schema(product, mapping)
    """
    normalized = {}
    for standard_name, possible_names in schema_mapping.items():
        value = get_field_value(obj, *possible_names)
        if value is not None:
            normalized[standard_name] = value
    
    # Copy any fields not in mapping
    for key, value in obj.items():
        if key not in normalized.values() and key not in [name for names in schema_mapping.values() for name in names]:
            normalized[key] = value
    
    return normalized
