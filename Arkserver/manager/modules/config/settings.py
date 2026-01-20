#!/usr/bin/env python3
"""
Module de gestion des paramètres ARK
Édition de GameUserSettings.ini avec le parser INI spécialisé
"""

import sys
import os
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils import paths
from utils.ini_parser import ArkINIParser


class SettingsManager:
    """Gestionnaire des paramètres ARK (GameUserSettings.ini)"""
    
    # Paramètres couramment modifiés avec descriptions
    COMMON_SETTINGS = {
        "ServerSettings": {
            "ServerPassword": "Mot de passe du serveur",
            "ServerAdminPassword": "Mot de passe admin",
            "MaxPlayers": "Nombre maximum de joueurs",
            "DifficultyOffset": "Difficulté (0.0 à 1.0)",
            "XPMultiplier": "Multiplicateur d'XP",
            "TamingSpeedMultiplier": "Vitesse d'apprivoisement",
            "HarvestAmountMultiplier": "Multiplicateur de récolte",
            "RCONPort": "Port RCON",
        },
        "SessionSettings": {
            "SessionName": "Nom du serveur (affiché dans la liste)",
        }
    }
    
    def __init__(self):
        """Initialise le gestionnaire"""
        self.parser = ArkINIParser(paths.GAME_USER_SETTINGS_INI)
    
    def get_setting(self, section: str, key: str) -> Optional[str]:
        """
        Récupère une valeur de paramètre
        
        Args:
            section: Section du INI
            key: Clé du paramètre
            
        Returns:
            Valeur ou None si introuvable
        """
        self.parser.read()
        return self.parser.get_value(section, key)
    
    def set_setting(self, section: str, key: str, value: str) -> Dict[str, any]:
        """
        Modifie un paramètre
        
        Args:
            section: Section du INI
            key: Clé du paramètre
            value: Nouvelle valeur
            
        Returns:
            Dict avec: success, message, error
        """
        try:
            self.parser.read()
            
            if not self.parser.set_value(section, key, value):
                return {
                    "success": False,
                    "message": f"Impossible de modifier {key} dans [{section}]",
                    "error": "Section introuvable"
                }
            
            self.parser.write()
            
            return {
                "success": True,
                "message": f"Paramètre modifié: {key} = {value}",
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Échec de la modification",
                "error": str(e)
            }
    
    def get_common_settings(self) -> Dict[str, any]:
        """
        Récupère les valeurs des paramètres couramment modifiés
        
        Returns:
            Dict avec: success, settings (dict), error
        """
        self.parser.read()
        
        settings = {}
        
        for section, keys in self.COMMON_SETTINGS.items():
            settings[section] = {}
            for key, description in keys.items():
                value = self.parser.get_value(section, key)
                settings[section][key] = {
                    "value": value if value else "(non défini)",
                    "description": description
                }
        
        return {
            "success": True,
            "settings": settings,
            "error": None
        }
    
    def format_common_settings(self) -> str:
        """Retourne un affichage formaté des paramètres courants"""
        result = self.get_common_settings()
        
        output = []
        output.append("═" * 60)
        output.append("  PARAMÈTRES ARK COURANTS")
        output.append("═" * 60)
        output.append("")
        
        if not result["success"]:
            output.append(f"❌ Erreur: {result['error']}")
            return "\n".join(output)
        
        settings = result["settings"]
        
        for section, keys in settings.items():
            output.append(f"[{section}]")
            output.append("")
            for key, info in keys.items():
                output.append(f"  {key}")
                output.append(f"    Valeur: {info['value']}")
                output.append(f"    Description: {info['description']}")
                output.append("")
        
        output.append("═" * 60)
        
        return "\n".join(output)
    
    def backup_settings(self) -> Dict[str, any]:
        """
        Crée une sauvegarde du fichier GameUserSettings.ini
        
        Returns:
            Dict avec: success, backup_path, error
        """
        import shutil
        from datetime import datetime
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{paths.GAME_USER_SETTINGS_INI}.backup_{timestamp}"
            
            shutil.copy2(paths.GAME_USER_SETTINGS_INI, backup_path)
            
            return {
                "success": True,
                "backup_path": backup_path,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "backup_path": None,
                "error": str(e)
            }
    
    def validate_settings(self) -> Dict[str, any]:
        """
        Valide la configuration (vérifie les paramètres critiques)
        
        Returns:
            Dict avec: success, warnings (list), errors (list)
        """
        self.parser.read()
        
        warnings = []
        errors = []
        
        # Vérifier mot de passe admin
        admin_pass = self.parser.get_value("ServerSettings", "ServerAdminPassword")
        if not admin_pass or admin_pass == "":
            warnings.append("Mot de passe admin non défini")
        elif admin_pass in ["admin", "password", "123456"]:
            warnings.append("Mot de passe admin faible détecté")
        
        # Vérifier port RCON
        rcon_port = self.parser.get_value("ServerSettings", "RCONPort")
        if rcon_port:
            try:
                port = int(rcon_port)
                if port < 1024 or port > 65535:
                    errors.append(f"Port RCON invalide: {port} (doit être entre 1024 et 65535)")
            except ValueError:
                errors.append(f"Port RCON invalide: {rcon_port} (doit être numérique)")
        
        # Vérifier multiplicateurs
        multipliers = ["XPMultiplier", "TamingSpeedMultiplier", "HarvestAmountMultiplier"]
        for mult in multipliers:
            value = self.parser.get_value("ServerSettings", mult)
            if value:
                try:
                    float_val = float(value)
                    if float_val <= 0:
                        warnings.append(f"{mult} est négatif ou nul")
                except ValueError:
                    errors.append(f"{mult} invalide: {value}")
        
        return {
            "success": len(errors) == 0,
            "warnings": warnings,
            "errors": errors
        }
