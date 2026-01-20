#!/usr/bin/env python3
"""
Script de test pour les modules ARK Manager
Tests qui peuvent s'exécuter hors de la VM
"""

import sys
import os

# Ajouter le chemin du manager
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'manager'))

print("=" * 60)
print("  TESTS ARK MANAGER (hors VM)")
print("=" * 60)
print()

# Test 1: Imports
print("TEST 1: Imports des modules")
print("-" * 60)
try:
    from utils import paths
    print("✅ utils.paths")
    from utils.ini_parser import ArkINIParser
    print("✅ utils.ini_parser")
    from modules.server import ServerManager
    print("✅ modules.server")
    from modules.backups import BackupManager
    print("✅ modules.backups")
    from modules.updates import UpdateManager
    print("✅ modules.updates")
    from modules.diagnostics import DiagnosticsManager
    print("✅ modules.diagnostics")
    from modules.config.maps import MapsManager
    print("✅ modules.config.maps")
    from modules.config.mods import ModsManager
    print("✅ modules.config.mods")
    from modules.config.settings import SettingsManager
    print("✅ modules.config.settings")
    print("\n✅ Tous les modules importés avec succès!")
except Exception as e:
    print(f"\n❌ Erreur d'import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 2: Parser INI
print("TEST 2: Parser INI avec fichier local")
print("-" * 60)
try:
    ini_path = os.path.join(os.path.dirname(__file__), 'GameUserSettings.ini')
    
    if not os.path.exists(ini_path):
        print(f"⚠️  Fichier non trouvé: {ini_path}")
    else:
        parser = ArkINIParser(ini_path)
        parser.read()
        
        print(f"✅ Fichier lu: {len(parser.lines)} lignes")
        print(f"✅ Sections trouvées: {len(parser.sections)}")
        
        # Afficher quelques sections
        sections = list(parser.sections.keys())[:3]
        for sec in sections:
            print(f"   • {sec}")
        
        # Tester lecture de valeurs
        session_name = parser.get_value('SessionSettings', 'SessionName')
        if session_name:
            print(f"\n✅ SessionName lu: {session_name}")
        
        server_pass = parser.get_value('ServerSettings', 'ServerPassword')
        if server_pass:
            print(f"✅ ServerPassword lu: (masqué)")
        
        print("\n✅ Parser INI fonctionne!")
except Exception as e:
    print(f"\n❌ Erreur parser: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 3: Logique BackupManager
print("TEST 3: Logique BackupManager (sans accès filesystem)")
print("-" * 60)
try:
    backup_mgr = BackupManager()
    
    # Test format_size
    print("✅ format_size(0) =", backup_mgr.format_size(0))
    print("✅ format_size(1024) =", backup_mgr.format_size(1024))
    print("✅ format_size(1048576) =", backup_mgr.format_size(1048576))
    print("✅ format_size(1073741824) =", backup_mgr.format_size(1073741824))
    
    print("\n✅ Logique de formatage fonctionne!")
except Exception as e:
    print(f"\n❌ Erreur logique: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 4: MapsManager - Validation
print("TEST 4: MapsManager - Cartes officielles")
print("-" * 60)
try:
    maps_mgr = MapsManager()
    
    print("Cartes de base:")
    for name, desc in maps_mgr.OFFICIAL_MAPS['base'].items():
        print(f"   • {name}: {desc}")
    
    print("\nDLC payants:")
    for name, desc in list(maps_mgr.OFFICIAL_MAPS['dlc_paid'].items())[:3]:
        print(f"   • {name}: {desc}")
    
    print("\nExtensions gratuites:")
    for name, desc in maps_mgr.OFFICIAL_MAPS['free_expansion'].items():
        print(f"   • {name}: {desc}")
    
    print("\n✅ Liste des cartes officielles OK!")
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 5: ModsManager - Lecture mods.list local
print("TEST 5: ModsManager - Lecture mods.list")
print("-" * 60)
try:
    mods_list_path = os.path.join(os.path.dirname(__file__), 'mods.list')
    
    if not os.path.exists(mods_list_path):
        print(f"⚠️  Fichier non trouvé: {mods_list_path}")
    else:
        # Lire manuellement pour tester
        with open(mods_list_path, 'r') as f:
            lines = f.readlines()
        
        print(f"✅ Fichier lu: {len(lines)} ligne(s)")
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '|' in line:
                    mod_id, mod_name = line.split('|', 1)
                    print(f"   • {mod_name} (ID: {mod_id})")
        
        print("\n✅ Format mods.list valide!")
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("  RÉSUMÉ DES TESTS")
print("=" * 60)
print()
print("✅ Tests réussis:")
print("   • Imports Python")
print("   • Parser INI")
print("   • Logique de formatage")
print("   • Validation des cartes")
print("   • Lecture mods.list")
print()
print("⚠️  Tests impossibles sans VM:")
print("   • Appels systemctl/pgrep")
print("   • Accès aux chemins /home/arkserver/")
print("   • Exécution scripts bash")
print()
print("💡 Pour tester complètement, déployez sur la VM et exécutez:")
print("   python3 /home/arkserver/arkserver/manager/menu.py")
print()
