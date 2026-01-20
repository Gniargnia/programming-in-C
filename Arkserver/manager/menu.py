#!/usr/bin/env python3
"""
Menu principal de gestion du serveur ARK
Orchestrateur Python pour les scripts Bash système
"""

import sys
import os
from typing import Optional, Callable, Dict, List

# Ajouter le chemin du module au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import paths
from modules.server import ServerManager
from modules.backups import BackupManager
from modules.updates import UpdateManager
from modules.diagnostics import DiagnosticsManager
from modules.config.maps import MapsManager
from modules.config.mods import ModsManager
from modules.config.settings import SettingsManager


class ArkServerMenu:
    """Menu interactif de gestion du serveur ARK"""
    
    def __init__(self):
        """Initialise le menu principal"""
        self.running = True
        self.menu_stack: List[str] = ["main"]  # Stack pour navigation sous-menus
        
        # Initialiser les gestionnaires de modules
        self.server_manager = ServerManager()
        self.backup_manager = BackupManager()
        self.update_manager = UpdateManager()
        self.diagnostics_manager = DiagnosticsManager()
        
        # Gestionnaires de configuration
        self.maps_manager = MapsManager()
        self.mods_manager = ModsManager()
        self.settings_manager = SettingsManager()
        
    def clear_screen(self) -> None:
        """Efface l'écran du terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title: str) -> None:
        """Affiche l'en-tête du menu"""
        self.clear_screen()
        print("=" * 60)
        print(f"  ARK SERVER MANAGER - {title}")
        print("=" * 60)
        print()
    
    def print_menu(self, title: str, options: Dict[str, str]) -> None:
        """
        Affiche un menu avec options numérotées
        
        Args:
            title: Titre du menu
            options: Dict {clé: description}
        """
        self.print_header(title)
        
        for key, description in options.items():
            print(f"  [{key}] {description}")
        
        print()
    
    def get_choice(self, valid_choices: List[str]) -> str:
        """
        Demande un choix à l'utilisateur
        
        Args:
            valid_choices: Liste des choix valides
            
        Returns:
            Le choix saisi (validé)
        """
        while True:
            choice = input("Choix: ").strip().lower()
            if choice in valid_choices:
                return choice
            print(f"❌ Choix invalide. Options: {', '.join(valid_choices)}")
    
    def pause(self, message: str = "Appuyez sur Entrée pour continuer...") -> None:
        """Pause avec message"""
        print()
        input(message)
    
    # ========================================================================
    # Menu Principal
    # ========================================================================
    
    def menu_main(self) -> None:
        """Menu principal"""
        options = {
            "1": "Gestion du serveur (start/stop/status/restart)",
            "2": "Backups (fast/daily/boot/prestop/restore)",
            "3": "Mises à jour (ARK + mods)",
            "4": "Configuration (maps/settings/mods)",
            "5": "Diagnostics (logs/monitoring/resources)",
            "q": "Quitter"
        }
        
        self.print_menu("MENU PRINCIPAL", options)
        choice = self.get_choice(list(options.keys()))
        
        if choice == "1":
            self.menu_stack.append("server")
            self.menu_server()
        elif choice == "2":
            self.menu_stack.append("backups")
            self.menu_backups()
        elif choice == "3":
            self.menu_stack.append("updates")
            self.menu_updates()
        elif choice == "4":
            self.menu_stack.append("config")
            self.menu_config()
        elif choice == "5":
            self.menu_stack.append("diagnostics")
            self.menu_diagnostics()
        elif choice == "q":
            self.running = False
    
    # ========================================================================
    # Sous-menus (stubs pour l'instant)
    # ========================================================================
    
    def menu_server(self) -> None:
        """Menu gestion serveur"""
        options = {
            "1": "Démarrer le serveur",
            "2": "Arrêter le serveur",
            "3": "Redémarrer le serveur",
            "4": "Statut du serveur",
            "b": "Retour"
        }
        
        self.print_menu("GESTION DU SERVEUR", options)
        choice = self.get_choice(list(options.keys()))
        
        if choice == "1":
            print("🚀 Démarrage du serveur en cours...")
            print()
            result = self.server_manager.start()
            
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
                if result["error"]:
                    print(f"   Erreur: {result['error']}")
            
            self.pause()
            
        elif choice == "2":
            print("🛑 Arrêt du serveur en cours...")
            confirm = input("⚠️  Confirmer l'arrêt du serveur ? (o/N): ").strip().lower()
            
            if confirm == "o":
                print()
                result = self.server_manager.stop(graceful=True)
                
                if result["success"]:
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ {result['message']}")
                    if result["error"]:
                        print(f"   Erreur: {result['error']}")
            else:
                print("❌ Arrêt annulé")
            
            self.pause()
            
        elif choice == "3":
            print("🔄 Redémarrage du serveur...")
            confirm = input("⚠️  Confirmer le redémarrage ? (o/N): ").strip().lower()
            
            if confirm == "o":
                print()
                result = self.server_manager.restart(graceful=True)
                
                if result["success"]:
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ {result['message']}")
                    if result["error"]:
                        print(f"   Erreur: {result['error']}")
            else:
                print("❌ Redémarrage annulé")
            
            self.pause()
            
        elif choice == "4":
            print()
            status_text = self.server_manager.get_detailed_status()
            print(status_text)
            self.pause()
            
        elif choice == "b":
            self.menu_stack.pop()
            return
    
    def menu_backups(self) -> None:
        """Menu gestion backups"""
        options = {
            "1": "Backup rapide (fast)",
            "2": "Backup complet (daily)",
            "3": "Résumé des backups",
            "4": "Détails d'un type de backup",
            "b": "Retour"
        }
        
        self.print_menu("GESTION DES BACKUPS", options)
        choice = self.get_choice(list(options.keys()))
        
        if choice == "1":
            print("")
            result = self.backup_manager.create_backup("fast")
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
                if result["error"]:
                    print(f"   Erreur: {result['error']}")
            self.pause()
            
        elif choice == "2":
            print("")
            result = self.backup_manager.create_backup("daily")
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
                if result["error"]:
                    print(f"   Erreur: {result['error']}")
            self.pause()
            
        elif choice == "3":
            print("")
            summary = self.backup_manager.get_backups_summary()
            print(summary)
            self.pause()
            
        elif choice == "4":
            print("")
            print("Types disponibles: fast, daily, boot, prestop")
            btype = input("Type de backup: ").strip().lower()
            if btype in ["fast", "daily", "boot", "prestop"]:
                print("")
                details = self.backup_manager.get_detailed_list(btype, limit=15)
                print(details)
            else:
                print("❌ Type invalide")
            self.pause()
            
        elif choice == "b":
            self.menu_stack.pop()
            return
    
    def menu_updates(self) -> None:
        """Menu mises à jour"""
        options = {
            "1": "Vérifier mises à jour ARK",
            "2": "Mettre à jour ARK",
            "3": "Mettre à jour les mods",
            "4": "Mise à jour complète (ARK + mods)",
            "b": "Retour"
        }
        
        self.print_menu("MISES À JOUR", options)
        choice = self.get_choice(list(options.keys()))
        
        if choice == "1":
            print("")
            result = self.update_manager.check_ark_update()
            if result["update_available"]:
                print(f"📦 {result['message']}")
            else:
                print(f"✅ {result['message']}")
            if result["error"]:
                print(f"⚠️  {result['error']}")
            self.pause()
            
        elif choice == "2":
            print("")
            confirm = input("⚠️  Mettre à jour ARK ? (o/N): ").strip().lower()
            if confirm == "o":
                print("")
                result = self.update_manager.update_ark()
                if result["success"]:
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ {result['message']}")
                    if result["error"]:
                        print(f"   Erreur: {result['error']}")
            else:
                print("❌ Mise à jour annulée")
            self.pause()
            
        elif choice == "3":
            print("")
            result = self.update_manager.update_mods()
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
            if result["error"]:
                print(f"⚠️  {result['error']}")
            self.pause()
            
        elif choice == "4":
            print("")
            confirm = input("⚠️  Mise à jour complète ARK + mods ? (o/N): ").strip().lower()
            if confirm == "o":
                print("")
                result = self.update_manager.full_update()
                print("")
                if result["success"]:
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ {result['message']}")
                    for error in result["errors"]:
                        print(f"   • {error}")
            else:
                print("❌ Mise à jour annulée")
            self.pause()
            
        elif choice == "b":
            self.menu_stack.pop()
            return
    
    def menu_config(self) -> None:
        """Menu configuration"""
        options = {
            "1": "Changer de carte",
            "2": "Modifier paramètres serveur",
            "3": "Gérer les mods (ajouter/supprimer)",
            "4": "Afficher configuration actuelle",
            "b": "Retour"
        }
        
        self.print_menu("CONFIGURATION", options)
        choice = self.get_choice(list(options.keys()))
        
        if choice == "1":
            self._submenu_change_map()
            
        elif choice == "2":
            self._submenu_edit_settings()
            
        elif choice == "3":
            self._submenu_manage_mods()
            
        elif choice == "4":
            self._submenu_show_config()
            
        elif choice == "b":
            self.menu_stack.pop()
            return
    
    def _submenu_change_map(self) -> None:
        """Sous-menu changement de carte"""
        print("")
        display = self.maps_manager.format_maps_list()
        print(display)
        print("")
        
        available_maps = self.maps_manager.get_all_map_names()
        
        if not available_maps:
            print("❌ Aucune carte disponible")
            self.pause()
            return
        
        print("Entrez le nom exact de la carte (ex: TheIsland, Ragnarok)")
        print("ou 'q' pour annuler")
        map_name = input("\nCarte: ").strip()
        
        if map_name.lower() == 'q':
            return
        
        if map_name not in available_maps:
            print(f"\n❌ Carte invalide ou non installée: {map_name}")
            self.pause()
            return
        
        print("")
        confirm = input(f"⚠️  Changer la carte pour {map_name} ? (o/N): ").strip().lower()
        
        if confirm == 'o':
            result = self.maps_manager.set_map(map_name)
            print("")
            if result["success"]:
                print(f"✅ {result['message']}")
                print("⚠️  Redémarrez le serveur pour appliquer les changements")
            else:
                print(f"❌ {result['message']}")
                if result["error"]:
                    print(f"   Erreur: {result['error']}")
        else:
            print("\n❌ Changement annulé")
        
        self.pause()
    
    def _submenu_edit_settings(self) -> None:
        """Sous-menu édition des paramètres"""
        print("")
        display = self.settings_manager.format_common_settings()
        print(display)
        print("")
        
        print("Entrez le nom du paramètre à modifier (ex: ServerPassword)")
        print("ou 'q' pour annuler")
        key = input("\nParamètre: ").strip()
        
        if key.lower() == 'q':
            return
        
        # Déterminer la section
        section = None
        for sect, keys in self.settings_manager.COMMON_SETTINGS.items():
            if key in keys:
                section = sect
                break
        
        if not section:
            print("\n❌ Paramètre non reconnu dans la liste courante")
            print("Pour des paramètres avancés, modifiez GameUserSettings.ini manuellement")
            self.pause()
            return
        
        print(f"\nValeur actuelle: {self.settings_manager.get_setting(section, key)}")
        new_value = input("Nouvelle valeur: ").strip()
        
        if not new_value:
            print("\n❌ Valeur vide, annulation")
            self.pause()
            return
        
        print("")
        confirm = input(f"⚠️  Modifier {key} = {new_value} ? (o/N): ").strip().lower()
        
        if confirm == 'o':
            result = self.settings_manager.set_setting(section, key, new_value)
            print("")
            if result["success"]:
                print(f"✅ {result['message']}")
                print("⚠️  Redémarrez le serveur pour appliquer les changements")
            else:
                print(f"❌ {result['message']}")
                if result["error"]:
                    print(f"   Erreur: {result['error']}")
        else:
            print("\n❌ Modification annulée")
        
        self.pause()
    
    def _submenu_manage_mods(self) -> None:
        """Sous-menu gestion des mods"""
        while True:
            print("")
            display = self.mods_manager.format_mods_list()
            print(display)
            print("")
            
            print("[1] Ajouter un mod")
            print("[2] Supprimer un mod")
            print("[3] Vérifier mods installés")
            print("[b] Retour")
            print("")
            
            choice = input("Choix: ").strip().lower()
            
            if choice == "1":
                print("")
                print("Entrez l'ID Steam Workshop du mod (numérique)")
                mod_id = input("ID: ").strip()
                
                if not mod_id.isdigit():
                    print("\n❌ ID invalide")
                    self.pause()
                    continue
                
                mod_name = input("Nom du mod: ").strip()
                
                if not mod_name:
                    print("\n❌ Nom vide")
                    self.pause()
                    continue
                
                result = self.mods_manager.add_mod(mod_id, mod_name)
                print("")
                if result["success"]:
                    print(f"✅ {result['message']}")
                    print("⚠️  Exécutez 'Mettre à jour les mods' pour télécharger le mod")
                else:
                    print(f"❌ {result['message']}")
                
                self.pause()
                
            elif choice == "2":
                print("")
                mod_id = input("ID du mod à supprimer: ").strip()
                
                if not mod_id.isdigit():
                    print("\n❌ ID invalide")
                    self.pause()
                    continue
                
                result = self.mods_manager.remove_mod(mod_id)
                print("")
                if result["success"]:
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ {result['message']}")
                
                self.pause()
                
            elif choice == "3":
                print("")
                result = self.mods_manager.check_installed_mods()
                if result["success"]:
                    print(f"✅ Mods installés: {len(result['installed'])}")
                    for mod in result['installed']:
                        print(f"   • {mod['name']} ({mod['id']})")
                    
                    if result['missing']:
                        print(f"\n⚠️  Mods manquants: {len(result['missing'])}")
                        for mod in result['missing']:
                            print(f"   • {mod['name']} ({mod['id']})")
                        print("\n💡 Utilisez 'Mettre à jour les mods' pour les installer")
                else:
                    print(f"❌ Erreur: {result['error']}")
                
                self.pause()
                
            elif choice == "b":
                break
    
    def _submenu_show_config(self) -> None:
        """Affiche la configuration complète"""
        print("")
        
        # Carte actuelle
        map_result = self.maps_manager.get_current_map()
        print("═" * 60)
        print("  CONFIGURATION ACTUELLE")
        print("═" * 60)
        print("")
        
        if map_result["success"]:
            print(f"🗺️  Carte: {map_result['map_name']}")
        else:
            print(f"🗺️  Carte: (erreur)")
        
        print("")
        
        # Mods
        mods_result = self.mods_manager.read_mods_list()
        if mods_result["success"]:
            print(f"🔧 Mods: {len(mods_result['mods'])}")
            for mod in mods_result['mods']:
                print(f"   • {mod['name']} ({mod['id']})")
        else:
            print("🔧 Mods: (erreur)")
        
        print("")
        
        # Paramètres clés
        session_name = self.settings_manager.get_setting("SessionSettings", "SessionName")
        max_players = self.settings_manager.get_setting("ServerSettings", "MaxPlayers")
        server_pass = self.settings_manager.get_setting("ServerSettings", "ServerPassword")
        
        print(f"⚙️  Nom du serveur: {session_name or '(non défini)'}")
        print(f"👥 Joueurs max: {max_players or '(non défini)'}")
        print(f"🔒 Mot de passe: {'(défini)' if server_pass else '(aucun)'}")
        
        print("")
        print("═" * 60)
        
        self.pause()
    
    def menu_diagnostics(self) -> None:
        """Menu diagnostics"""
        options = {
            "1": "Afficher les logs",
            "2": "Monitorer ressources système",
            "3": "Vérifier intégrité serveur",
            "4": "Informations système",
            "b": "Retour"
        }
        
        self.print_menu("DIAGNOSTICS", options)
        choice = self.get_choice(list(options.keys()))
        
        if choice == "1":
            print("")
            print("Types de logs: core, backup, mods, update")
            log_type = input("Type de log: ").strip().lower()
            if log_type in ["core", "backup", "mods", "update"]:
                lines = input("Nombre de lignes (défaut 50): ").strip()
                lines = int(lines) if lines.isdigit() else 50
                print("")
                result = self.diagnostics_manager.get_log(log_type, lines)
                if result["success"]:
                    print(f"═══ LOG {log_type.upper()} (dernières {lines} lignes) ═══")
                    print(result["content"])
                else:
                    print(f"❌ {result['error']}")
            else:
                print("❌ Type de log invalide")
            self.pause()
            
        elif choice == "2":
            print("")
            display = self.diagnostics_manager.format_resources_display()
            print(display)
            self.pause()
            
        elif choice == "3":
            print("")
            result = self.diagnostics_manager.check_integrity()
            print("═" * 60)
            print("  VÉRIFICATION INTÉGRITÉ SERVEUR")
            print("═" * 60)
            print("")
            for check in result["checks"]:
                print(f"{check['status']} - {check['name']}")
            print("")
            print("═" * 60)
            self.pause()
            
        elif choice == "4":
            print("")
            display = self.diagnostics_manager.format_system_info_display()
            print(display)
            self.pause()
            
        elif choice == "b":
            self.menu_stack.pop()
            return
    
    # ========================================================================
    # Boucle principale
    # ========================================================================
    
    def run(self) -> None:
        """Lance la boucle principale du menu"""
        while self.running:
            current_menu = self.menu_stack[-1]
            
            if current_menu == "main":
                self.menu_main()
            elif current_menu == "server":
                self.menu_server()
            elif current_menu == "backups":
                self.menu_backups()
            elif current_menu == "updates":
                self.menu_updates()
            elif current_menu == "config":
                self.menu_config()
            elif current_menu == "diagnostics":
                self.menu_diagnostics()
            else:
                # Sécurité : retour menu principal si menu inconnu
                self.menu_stack = ["main"]
        
        # Message de sortie
        self.clear_screen()
        print("👋 ARK Server Manager fermé. À bientôt!")


def menu():
    """Point d'entrée du programme"""
    try:
        ark_menu = ArkServerMenu()
        ark_menu.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERREUR FATALE: {e}")
        sys.exit(1)


if __name__ == "__main__":
    menu()
