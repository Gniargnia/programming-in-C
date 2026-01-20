#!/usr/bin/env python3
"""
Module de gestion des mises à jour ARK
Interface Python vers ark-update-check.sh et ark-mods.sh
"""

import subprocess
import json
from typing import Dict, Tuple
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import paths


class UpdateManager:
    """Gestionnaire des mises à jour ARK et mods"""
    
    def _run_command(self, command: list, timeout: int = 600) -> Tuple[int, str, str]:
        """Exécute une commande avec timeout"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", f"Timeout après {timeout}s"
        except Exception as e:
            return -2, "", str(e)
    
    def check_ark_update(self) -> Dict[str, any]:
        """
        Vérifie si une mise à jour ARK est disponible
        
        Returns:
            Dict avec: update_available (bool), message, error
        """
        if not os.path.exists(paths.SCRIPT_UPDATE):
            return {
                "update_available": False,
                "message": "Script de vérification introuvable",
                "error": f"Fichier manquant: {paths.SCRIPT_UPDATE}"
            }
        
        print("🔍 Vérification des mises à jour ARK...")
        
        returncode, stdout, stderr = self._run_command([
            "bash", paths.SCRIPT_UPDATE
        ], timeout=120)
        
        # Le script retourne 0 si pas de MAJ, 1 si MAJ disponible, 2 si erreur
        if returncode == 0:
            return {
                "update_available": False,
                "message": "ARK est à jour",
                "error": None
            }
        elif returncode == 1:
            return {
                "update_available": True,
                "message": "Une mise à jour ARK est disponible",
                "error": None
            }
        else:
            return {
                "update_available": False,
                "message": "Erreur lors de la vérification",
                "error": stderr or "Erreur inconnue"
            }
    
    def update_ark(self) -> Dict[str, any]:
        """
        Met à jour le serveur ARK
        
        Returns:
            Dict avec: success (bool), message, error
        """
        print("⏳ Mise à jour ARK en cours (peut prendre plusieurs minutes)...")
        
        # Utiliser SteamCMD pour mettre à jour
        if not os.path.exists(paths.STEAMCMD):
            return {
                "success": False,
                "message": "SteamCMD introuvable",
                "error": f"Fichier manquant: {paths.STEAMCMD}"
            }
        
        returncode, stdout, stderr = self._run_command([
            paths.STEAMCMD,
            "+force_install_dir", paths.ARK_ROOT,
            "+login", "anonymous",
            "+app_update", paths.ARK_APP_ID, "validate",
            "+quit"
        ], timeout=1800)  # 30 minutes max
        
        if returncode == 0:
            return {
                "success": True,
                "message": "Mise à jour ARK terminée avec succès",
                "error": None
            }
        else:
            return {
                "success": False,
                "message": "Échec de la mise à jour ARK",
                "error": stderr or "Erreur SteamCMD"
            }
    
    def update_mods(self) -> Dict[str, any]:
        """
        Met à jour les mods via ark-mods.sh
        
        Returns:
            Dict avec: success (bool), message, error
        """
        if not os.path.exists(paths.SCRIPT_MODS):
            return {
                "success": False,
                "message": "Script de gestion des mods introuvable",
                "error": f"Fichier manquant: {paths.SCRIPT_MODS}"
            }
        
        print("⏳ Mise à jour des mods en cours...")
        
        returncode, stdout, stderr = self._run_command([
            "bash", paths.SCRIPT_MODS, "update"
        ], timeout=900)  # 15 minutes max
        
        # Le script retourne 0 si OK, 1 si warnings, 2 si erreur critique
        if returncode == 0:
            return {
                "success": True,
                "message": "Tous les mods ont été mis à jour avec succès",
                "error": None
            }
        elif returncode == 1:
            return {
                "success": True,
                "message": "Mods mis à jour avec des avertissements (voir logs)",
                "error": "Certains mods ont généré des warnings"
            }
        else:
            return {
                "success": False,
                "message": "Échec de la mise à jour des mods",
                "error": stderr or "Erreur critique"
            }
    
    def full_update(self) -> Dict[str, any]:
        """
        Effectue une mise à jour complète (ARK + mods)
        
        Returns:
            Dict avec: success (bool), message, errors (list)
        """
        errors = []
        
        # 1. Vérifier ARK
        print("=" * 60)
        print("ÉTAPE 1/3: Vérification ARK")
        print("=" * 60)
        check_result = self.check_ark_update()
        
        if check_result["error"]:
            errors.append(f"Vérification ARK: {check_result['error']}")
        
        # 2. Mettre à jour ARK si nécessaire
        if check_result["update_available"]:
            print("\n" + "=" * 60)
            print("ÉTAPE 2/3: Mise à jour ARK")
            print("=" * 60)
            update_result = self.update_ark()
            
            if not update_result["success"]:
                errors.append(f"MAJ ARK: {update_result['error']}")
        else:
            print("\n✅ ARK déjà à jour, étape 2 ignorée")
        
        # 3. Mettre à jour les mods
        print("\n" + "=" * 60)
        print("ÉTAPE 3/3: Mise à jour des mods")
        print("=" * 60)
        mods_result = self.update_mods()
        
        if not mods_result["success"]:
            errors.append(f"MAJ Mods: {mods_result['error']}")
        elif mods_result["error"]:
            # Warnings
            errors.append(f"MAJ Mods (warning): {mods_result['error']}")
        
        # Résumé
        if len(errors) == 0:
            return {
                "success": True,
                "message": "Mise à jour complète réussie (ARK + mods)",
                "errors": []
            }
        else:
            return {
                "success": False,
                "message": f"Mise à jour terminée avec {len(errors)} erreur(s)",
                "errors": errors
            }
