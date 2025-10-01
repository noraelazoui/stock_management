# Résumé des Modifications - Type Formule

## 🎯 Problème Résolu
Les formules n'apparaissaient pas dans le combobox de l'interface de fabrication car le champ `type_formule` était manquant dans MongoDB.

## ✅ Solutions Implémentées

### 1. Script de Migration: `scripts/add_type_formule.py`
- **Fonction**: Ajoute le champ `type_formule` aux formules existantes
- **Logique**:
  - `type_formule: "simple"` → Formules Premix (uniquement des matières/additifs)
  - `type_formule: "mixte"` → Formules Usine (contient au moins une formule)

**Usage**:
```bash
python3 scripts/add_type_formule.py
```

### 2. Mise à jour de `scripts/insert_demo_data.py`
- **Modification**: Ajout du champ `type_formule` lors de l'insertion des formules
- **Formules insérées**:
  - PREMIX1: `type_formule: "simple"`
  - PREMIX2: `type_formule: "simple"`
  - PRODFIN1: `type_formule: "mixte"`

**Usage**:
```bash
python3 scripts/insert_demo_data.py
```

### 3. Script de Test: `test_combobox_data.py`
- **Fonction**: Vérifie que les formules sont correctement récupérées pour les combobox
- **Tests effectués**:
  - Récupération des formules Premix (simple)
  - Récupération des formules Usine (mixte)
  - Sélection d'un code et récupération des optimisations

**Usage**:
```bash
python3 test_combobox_data.py
```

## 📊 Résultats

### Structure MongoDB (Formules)
```json
{
  "code": "PREMIX1",
  "type": "formule",
  "type_formule": "simple",  // ← NOUVEAU CHAMP
  "optim": "1",
  "recette_code": "R001",
  "designation": "Premix 1",
  "composantes": [...]
}
```

### Comportement de l'Interface
- **Radio "Premix"** → Affiche: PREMIX1, PREMIX2
- **Radio "Usine"** → Affiche: PRODFIN1

## 🔍 Distinction des Types

| Type Formule | Description | Composantes | Exemples |
|--------------|-------------|-------------|----------|
| **simple** | Premix | Uniquement matières/additifs (type: "simple") | PREMIX1, PREMIX2 |
| **mixte** | Usine | Contient au moins une formule (type: "formule") | PRODFIN1 |

## 📝 Fichiers Modifiés

1. ✅ `/scripts/add_type_formule.py` (nouveau)
2. ✅ `/scripts/insert_demo_data.py` (modifié)
3. ✅ `/test_combobox_data.py` (nouveau)

## 🚀 Pour les Futures Formules

Lors de la création de nouvelles formules, assurez-vous d'ajouter le champ `type_formule`:
- `"type_formule": "simple"` si la formule ne contient que des matières/additifs
- `"type_formule": "mixte"` si la formule contient d'autres formules

## ✅ Vérification
Toutes les formules existantes ont été mises à jour et les tests confirment que le combobox fonctionne correctement!
