#!/usr/bin/env python3
"""
Module de gestion des mods ARK
Ajout, suppression, validation de mods.list
"""

import os
from typing import Dict, List, Tuple
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils import paths


class ModsManager:
    """Gestionnaire des mods ARK"""
    
    def read_mods_list(self) -> Dict[str, any]:
        """
        Lit le fichier mods.list
        
        Returns:
            Dict avec: success, mods (list of dict), error
        """
        if not os.path.exists(paths.MODS_LIST):
            return {
                "success": False,
                "mods": [],
                "error": f"Fichier mods.list introuvable: {paths.MODS_LIST}"
            }
        
        mods = []
        try:
            with open(paths.MODS_LIST, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Ignorer lignes vides et commentaires
                    if not line or line.startswith('#'):
                        continue
                    
                    # Format attendu: MOD_ID|MOD_NAME
                    if '|' not in line:
                        continue
                    
                    parts = line.split('|', 1)
                    if len(parts) == 2:
                        mod_id = parts[0].strip()
                        mod_name = parts[1].strip()
                        
                        if mod_id.isdigit():
                            mods.append({
                                "id": mod_id,
                                "name": mod_name,
                                "line": line_num
                            })
            
            return {
                "success": True,
                "mods": mods,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "mods": [],
                "error": str(e)
            }
    
    def write_mods_list(self, mods: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Écrit le fichier mods.list
        
        Args:
            mods: Liste de dict avec 'id' et 'name'
            
        Returns:
            Dict avec: success, message, error
        """
        try:
            with open(paths.MODS_LIST, 'w') as f:
                for mod in mods:
                    f.write(f"{mod['id']}|{mod['name']}\n")
            
            return {
                "success": True,
                "message": f"{len(mods)} mod(s) sauvegardé(s)",
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Échec de l'écriture du fichier",
                "error": str(e)
            }
    
    def add_mod(self, mod_id: str, mod_name: str) -> Dict[str, any]:
        """
        Ajoute un mod à la liste
        
        Args:
            mod_id: ID Steam Workshop du mod
            mod_name: Nom du mod
            
        Returns:
            Dict avec: success, message, error
        """
        # Validation
        if not mod_id.isdigit():
            return {
                "success": False,
                "message": "ID de mod invalide (doit être numérique)",
                "error": None
            }
        
        if not mod_name or not mod_name.strip():
            return {
                "success": False,
                "message": "Nom de mod invalide (ne peut pas être vide)",
                "error": None
            }
        
        # Lire la liste actuelle
        result = self.read_mods_list()
        if not result["success"]:
            return {
                "success": False,
                "message": "Impossible de lire mods.list",
                "error": result["error"]
            }
        
        mods = result["mods"]
        
        # Vérifier si le mod existe déjà
        for mod in mods:
            if mod["id"] == mod_id:
                return {
                    "success": False,
                    "message": f"Le mod {mod_id} existe déjà ({mod['name']})",
                    "error": None
                }
        
        # Ajouter le nouveau mod
        mods.append({"id": mod_id, "name": mod_name.strip()})
        
        # Sauvegarder
        write_result = self.write_mods_list(mods)
        
        if write_result["success"]:
            return {
                "success": True,
                "message": f"Mod ajouté: {mod_name} ({mod_id})",
                "error": None
            }
        else:
            return write_result
    
    def remove_mod(self, mod_id: str) -> Dict[str, any]:
        """
        Supprime un mod de la liste
        
        Args:
            mod_id: ID Steam Workshop du mod
            
        Returns:
            Dict avec: success, message, error
        """
        # Lire la liste actuelle
        result = self.read_mods_list()
        if not result["success"]:
            return {
                "success": False,
                "message": "Impossible de lire mods.list",
                "error": result["error"]
            }
        
        mods = result["mods"]
        
        # Trouver et supprimer le mod
        mod_found = None
        new_mods = []
        for mod in mods:
            if mod["id"] == mod_id:
                mod_found = mod
            else:
                new_mods.append(mod)
        
        if not mod_found:
            return {
                "success": False,
                "message": f"Mod {mod_id} introuvable dans la liste",
                "error": None
            }
        
        # Sauvegarder
        write_result = self.write_mods_list(new_mods)
        
        if write_result["success"]:
            return {
                "success": True,
                "message": f"Mod supprimé: {mod_found['name']} ({mod_id})",
                "error": None
            }
        else:
            return write_result
    
    def format_mods_list(self) -> str:
        """Retourne une liste formatée des mods"""
        result = self.read_mods_list()
        
        output = []
        output.append("═" * 60)
        output.append("  MODS WORKSHOP CONFIGURÉS")
        output.append("═" * 60)
        output.append("")
        
        if not result["success"]:
            output.append(f"❌ Erreur: {result['error']}")
            return "\n".join(output)
        
        mods = result["mods"]
        
        if not mods:
            output.append("ℹ️  Aucun mod configuré")
        else:
            output.append(f"Total: {len(mods)} mod(s)")
            output.append("")
            for idx, mod in enumerate(mods, 1):
                output.append(f"[{idx}] {mod['name']}")
                output.append(f"    ID: {mod['id']}")
                output.append("")
        
        output.append("═" * 60)
        
        return "\n".join(output)
    
    def check_installed_mods(self) -> Dict[str, any]:
        """
        Vérifie quels mods sont installés dans le workshop
        
        Returns:
            Dict avec: success, installed (list), missing (list), error
        """
        result = self.read_mods_list()
        if not result["success"]:
            return {
                "success": False,
                "installed": [],
                "missing": [],
                "error": result["error"]
            }
        
        installed = []
        missing = []
        
        for mod in result["mods"]:
            mod_path = os.path.join(paths.WORKSHOP_DIR, mod["id"])
            if os.path.exists(mod_path) and os.path.isdir(mod_path):
                installed.append(mod)
            else:
                missing.append(mod)
        
        return {
            "success": True,
            "installed": installed,
            "missing": missing,
            "error": None
        }
