#!/bin/bash
# Script de déploiement automatique ARK Manager
# À exécuter sur la VM : /home/arkserver/deploy.sh

set -e

REPO_DIR="/home/arkserver/repo"
ARK_DIR="/home/arkserver/arkserver"
REPO_URL="https://github.com/Gniargnia/programming-in-C.git"

echo "============================================================"
echo "  DÉPLOIEMENT ARK SERVER MANAGER"
echo "============================================================"
echo ""

# 1. Vérifier/Cloner le repo
if [ -d "$REPO_DIR" ]; then
    echo "📦 Mise à jour du repository..."
    cd "$REPO_DIR"
    git pull
else
    echo "📦 Clonage du repository..."
    cd /home/arkserver
    git clone "$REPO_URL" repo
    cd "$REPO_DIR"
fi

echo ""

# 2. Déployer le manager Python
echo "🐍 Déploiement du manager Python..."
if [ -d "$ARK_DIR/manager" ]; then
    echo "   Suppression de l'ancienne version..."
    rm -rf "$ARK_DIR/manager"
fi

cp -r "$REPO_DIR/Arkserver/manager" "$ARK_DIR/"
chmod +x "$ARK_DIR/manager/menu.py"
echo "   ✓ Manager Python copié"

echo ""

# 3. Mettre à jour les scripts bash
echo "📜 Mise à jour des scripts bash..."
SCRIPTS=("ark-core.sh" "ark-stop.sh" "ark-backup.sh" "ark-mods.sh" "ark-update-check.sh")

for script in "${SCRIPTS[@]}"; do
    if [ -f "$REPO_DIR/Arkserver/$script" ]; then
        cp "$REPO_DIR/Arkserver/$script" "$ARK_DIR/core/"
        chmod +x "$ARK_DIR/core/$script"
        echo "   ✓ $script"
    else
        echo "   ⚠ $script non trouvé (ignoré)"
    fi
done

echo ""

# 4. Mettre à jour les fichiers de configuration (si besoin)
echo "⚙️  Vérification des fichiers de configuration..."

# Ne pas écraser les configs existantes, juste vérifier
if [ ! -f "$ARK_DIR/config/current_map" ]; then
    if [ -f "$REPO_DIR/Arkserver/current_map" ]; then
        cp "$REPO_DIR/Arkserver/current_map" "$ARK_DIR/config/"
        echo "   ✓ current_map créé"
    fi
fi

if [ ! -f "$ARK_DIR/config/mods.list" ]; then
    if [ -f "$REPO_DIR/Arkserver/mods.list" ]; then
        cp "$REPO_DIR/Arkserver/mods.list" "$ARK_DIR/config/"
        echo "   ✓ mods.list créé"
    fi
fi

if [ ! -f "$ARK_DIR/config/settings.conf" ]; then
    if [ -f "$REPO_DIR/Arkserver/settings.conf" ]; then
        cp "$REPO_DIR/Arkserver/settings.conf" "$ARK_DIR/config/"
        echo "   ✓ settings.conf créé"
    fi
fi

echo "   ✓ Fichiers de configuration vérifiés"

echo ""

# 5. Vérifier Python et imports
echo "🔍 Vérification des modules Python..."

if ! python3 --version &>/dev/null; then
    echo "   ❌ Python 3 non trouvé!"
    exit 1
fi

python3 << 'PYTHON'
import sys
sys.path.insert(0, '/home/arkserver/arkserver/manager')

try:
    from utils import paths
    from modules.server import ServerManager
    from modules.backups import BackupManager
    from modules.updates import UpdateManager
    from modules.diagnostics import DiagnosticsManager
    from modules.config.maps import MapsManager
    from modules.config.mods import ModsManager
    from modules.config.settings import SettingsManager
    print("   ✓ Tous les modules Python importés avec succès!")
except Exception as e:
    print(f"   ❌ Erreur d'import: {e}")
    sys.exit(1)
PYTHON

echo ""

# 6. Résumé
echo "============================================================"
echo "  DÉPLOIEMENT TERMINÉ AVEC SUCCÈS!"
echo "============================================================"
echo ""
echo "📂 Structure déployée:"
echo "   /home/arkserver/arkserver/manager/     ← Menu Python"
echo "   /home/arkserver/arkserver/core/        ← Scripts bash"
echo "   /home/arkserver/arkserver/config/      ← Configurations"
echo ""
echo "🚀 Pour lancer le menu de gestion:"
echo "   python3 /home/arkserver/arkserver/manager/menu.py"
echo ""
echo "📚 Documentation:"
echo "   /home/arkserver/repo/Arkserver/DEPLOIEMENT.md"
echo "   /home/arkserver/repo/Arkserver/CONFIGURATION.md"
echo ""
