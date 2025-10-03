# 🚀 LANCER L'APPLICATION / START APPLICATION

**Date**: 2 octobre 2025  
**Status**: ✅ PRÊT À UTILISER / READY TO USE

---

## ⚡ Démarrage Rapide / Quick Start

```bash
cd /home/najib/Documents/stock_management
python3 main.py
```

---

## ✅ Ce Qui Fonctionne / What Works

### Dashboard avec Alertes / Dashboard with Alerts:
- 📊 **Stock Article** - Graphiques colorés (bar + pie charts)
- 📦 **Stock Fabrication** - Détails des fabrications avec filtres
- 📋 **Inventaire de Stock** - Vue détaillée avec DEMs
- ⚠️ **Alertes Stock** - Surveillance en temps réel:
  - 🔴 Stock Bas (3 alertes actives)
  - ⏰ Expiration (3 alertes actives)

### Autres Fonctionnalités / Other Features:
- 📝 Articles
- 👥 Fournisseurs  
- 🧪 Formules
- 📦 Commandes
- 🏭 Fabrications

---

## 🧪 Tester Avant de Lancer / Test Before Running

```bash
python3 test_app_startup.py
```

Cela vérifie que tout fonctionne sans crash.  
This verifies everything works without crashes.

---

## 🔧 Si Problème / If Issues

### 1. Test des Composants / Component Test:
```bash
python3 test_crash_fix.py
```

### 2. Vérifier MongoDB / Check MongoDB:
```bash
sudo systemctl status mongod
# Ou / Or:
mongo --eval "db.version()"
```

### 3. Environnement Virtuel / Virtual Environment:
```bash
source venv/bin/activate
python3 main.py
```

### 4. Réinstaller Matplotlib / Reinstall Matplotlib:
```bash
pip3 install --upgrade --force-reinstall matplotlib
```

---

## 📊 Alertes de Test / Test Alerts

L'application a des alertes de démonstration:  
The application has demonstration alerts:

**Stock Bas / Low Stock**:
- DEM002: 2/10 (20%) - CRITIQUE
- DEM001: 5/10 (50%) - ATTENTION  
- DEM003: 7/10 (70%) - ATTENTION

**Expiration**:
- DEM005: EXPIRÉ (depuis 11 jours)
- DEM004: CRITIQUE (29 jours restants)
- DEM006: ATTENTION (59 jours restants)

---

## 📝 Fonctionnalités Principales / Main Features

### Dashboard:
1. **Filtres** - Date, DEM, Lot
2. **Graphiques** - Visualisation colorée
3. **Alertes** - Code couleur par criticité
4. **Rafraîchir** - Données en temps réel

### Navigation:
- Onglets en haut / Tabs at top
- Sous-onglets dans Dashboard  
- Boutons "Actualiser" partout

---

## ⚙️ Configuration

### Seuils d'Alerte / Alert Thresholds:
- **Stock Bas**: Configuré par article (défaut: 10)
- **Expiration**: Configuré par article (défaut: 3 mois)

### Modifier dans Article View / Modify in Article View:
- "Seuil alerte quantité"
- "Alerte expiration (mois)"

---

## 📚 Documentation

| Fichier / File | Description |
|----------------|-------------|
| `SEGFAULT_FIX_COMPLETE.md` | 🔧 Solution complète du crash |
| `ALERT_SYSTEM_COMPLETE.md` | ⚠️ Système d'alertes |
| `DASHBOARD_ENHANCEMENT_COMPLETE.md` | 📊 Améliorations dashboard |
| `CRASH_FIX.md` | 🐛 Détails techniques du fix |

---

## 🎯 Résolution de Problèmes / Troubleshooting

### Problème: Application se ferme immédiatement
**Solution**: Vérifier la sortie d'erreur:
```bash
python3 main.py 2>&1 | tee error.log
```

### Problème: Graphiques ne s'affichent pas
**Solution**: Backend matplotlib:
```bash
python3 -c "import matplotlib; print(matplotlib.get_backend())"
# Doit afficher: TkAgg
```

### Problème: Erreur MongoDB
**Solution**: Démarrer MongoDB:
```bash
sudo systemctl start mongod
```

### Problème: Module manquant
**Solution**: Installer dépendances:
```bash
pip3 install -r requirements.txt
```

---

## ✅ Vérifications / Checks

Avant de lancer, vérifier que:  
Before running, check that:

- [x] MongoDB est démarré / is running
- [x] Python 3.10+ installé / installed
- [x] Dépendances installées / dependencies installed
- [x] Pas d'erreurs dans test_app_startup.py

---

## 🎊 Status

**Application**: 🟢 STABLE ET FONCTIONNELLE  
**Tests**: ✅ 8/8 PASSÉS  
**Alertes**: ✅ 6 ACTIVES (démonstration)  
**Production**: 🟢 PRÊT

---

**Dernière MAJ**: 2 octobre 2025  
**Version**: 1.0.0 (Stable)  
**Status**: Production Ready 🚀
