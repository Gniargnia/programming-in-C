# Guide de déploiement - ARK Server Manager

## 📦 Déploiement sur la VM

### Prérequis
- Accès SSH à la VM : `arkserver@gagnongaming`
- Python 3.8+ installé
- Structure ARK déjà en place

### Structure cible sur la VM
```
/home/arkserver/arkserver/
├── core/                  ← Scripts bash (déjà présents)
├── manager/              ← À déployer (Python)
├── config/               ← Configurations (déjà présent)
└── ShooterGame/          ← Serveur ARK (déjà présent)
```

## 🚀 Méthode 1 : Déploiement manuel via SCP

### Depuis votre machine locale

```bash
# 1. Compresser le dossier manager
cd /chemin/vers/repo/Arkserver
tar -czf manager.tar.gz manager/

# 2. Copier sur la VM
scp manager.tar.gz arkserver@gagnongaming:/tmp/

# 3. Se connecter à la VM
ssh arkserver@gagnongaming

# 4. Décompresser dans le bon emplacement
cd /home/arkserver/arkserver
tar -xzf /tmp/manager.tar.gz
rm /tmp/manager.tar.gz

# 5. Vérifier les permissions
chmod +x manager/menu.py

# 6. Tester
python3 manager/menu.py
```

## 🚀 Méthode 2 : Déploiement via Git (recommandé)

### Sur la VM

```bash
# 1. Cloner ou mettre à jour le repo
cd /home/arkserver
git clone https://github.com/Gniargnia/programming-in-C.git repo

# OU si déjà cloné
cd /home/arkserver/repo
git pull

# 2. Copier le manager
cp -r /home/arkserver/repo/Arkserver/manager /home/arkserver/arkserver/

# 3. Mettre à jour les scripts bash si nécessaire
cp /home/arkserver/repo/Arkserver/ark-*.sh /home/arkserver/arkserver/core/
chmod +x /home/arkserver/arkserver/core/*.sh

# 4. Mettre à jour les fichiers de config
cp /home/arkserver/repo/Arkserver/*.conf /home/arkserver/arkserver/config/
cp /home/arkserver/repo/Arkserver/mods.list /home/arkserver/arkserver/config/
cp /home/arkserver/repo/Arkserver/current_map /home/arkserver/arkserver/config/

# 5. Tester
python3 /home/arkserver/arkserver/manager/menu.py
```

## 🔧 Script de déploiement automatique

Créer `/home/arkserver/deploy.sh` :

```bash
#!/bin/bash
# Script de déploiement automatique

set -e

REPO_DIR="/home/arkserver/repo"
ARK_DIR="/home/arkserver/arkserver"

echo "=== Déploiement ARK Manager ==="

# 1. Mettre à jour le repo
if [ -d "$REPO_DIR" ]; then
    echo "Mise à jour du repo..."
    cd "$REPO_DIR"
    git pull
else
    echo "Clonage du repo..."
    cd /home/arkserver
    git clone https://github.com/Gniargnia/programming-in-C.git repo
    cd "$REPO_DIR"
fi

# 2. Déployer le manager Python
echo "Déploiement du manager Python..."
rm -rf "$ARK_DIR/manager"
cp -r "$REPO_DIR/Arkserver/manager" "$ARK_DIR/"
chmod +x "$ARK_DIR/manager/menu.py"

# 3. Mettre à jour les scripts bash
echo "Mise à jour des scripts bash..."
for script in ark-core.sh ark-stop.sh ark-backup.sh ark-mods.sh ark-update-check.sh; do
    if [ -f "$REPO_DIR/Arkserver/$script" ]; then
        cp "$REPO_DIR/Arkserver/$script" "$ARK_DIR/core/"
        chmod +x "$ARK_DIR/core/$script"
        echo "  ✓ $script"
    fi
done

# 4. Vérifier la structure
echo "Vérification de la structure..."
python3 -c "
import sys
sys.path.insert(0, '$ARK_DIR/manager')
from utils import paths
from modules.server import ServerManager
from modules.backups import BackupManager
from modules.updates import UpdateManager
from modules.diagnostics import DiagnosticsManager
from modules.config.maps import MapsManager
from modules.config.mods import ModsManager
from modules.config.settings import SettingsManager
print('✅ Tous les modules Python importés avec succès!')
"

echo ""
echo "=== Déploiement terminé ! ==="
echo ""
echo "Pour lancer le menu :"
echo "  python3 $ARK_DIR/manager/menu.py"
echo ""
```

Rendre exécutable :
```bash
chmod +x /home/arkserver/deploy.sh
```

Utilisation :
```bash
/home/arkserver/deploy.sh
```

## ✅ Vérifications post-déploiement

### 1. Tester les imports
```bash
python3 -c "
import sys
sys.path.insert(0, '/home/arkserver/arkserver/manager')
from modules.server import ServerManager
print('✅ Import OK')
"
```

### 2. Vérifier les chemins
```bash
python3 -c "
import sys
sys.path.insert(0, '/home/arkserver/arkserver/manager')
from utils import paths
print(f'ARK_ROOT: {paths.ARK_ROOT}')
print(f'SCRIPT_CORE: {paths.SCRIPT_CORE}')
print(f'MODS_LIST: {paths.MODS_LIST}')
"
```

### 3. Tester le menu
```bash
python3 /home/arkserver/arkserver/manager/menu.py
```

## 🐛 Dépannage

### Erreur : "ModuleNotFoundError"
```bash
# Vérifier la structure
ls -la /home/arkserver/arkserver/manager/
ls -la /home/arkserver/arkserver/manager/modules/
ls -la /home/arkserver/arkserver/manager/utils/
```

### Erreur : "Permission denied"
```bash
chmod +x /home/arkserver/arkserver/manager/menu.py
chmod +x /home/arkserver/arkserver/core/*.sh
```

### Erreur : "File not found"
```bash
# Vérifier les chemins absolus
cd /home/arkserver/arkserver
find . -name "*.py" -o -name "*.sh" | head -20
```

## 🔄 Mise à jour après modifications

```bash
# Simple : réexécuter le script de déploiement
/home/arkserver/deploy.sh

# Manuel : copier juste le manager
cd /home/arkserver/repo && git pull
cp -r /home/arkserver/repo/Arkserver/manager /home/arkserver/arkserver/
```

## 📝 Notes importantes

1. **Ne pas modifier directement sur la VM** - Toujours modifier dans le repo Git
2. **Redémarrer le serveur** après changement de carte ou mods
3. **Backup avant mise à jour** - Le menu propose cette option
4. **Logs disponibles** dans `/home/arkserver/arkserver/logs/`
