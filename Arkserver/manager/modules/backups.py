#!/usr/bin/env python3
"""
Module de gestion des backups ARK
Interface Python vers ark-backup.sh
"""

import subprocess
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import paths


class BackupManager:
    """Gestionnaire des backups ARK"""
    
    def __init__(self):
        """Initialise le gestionnaire de backups"""
        self.backup_types = {
            "fast": paths.BACKUP_FAST_DIR,
            "daily": paths.BACKUP_DAILY_DIR,
            "boot": paths.BACKUP_BOOT_DIR,
            "prestop": paths.BACKUP_PRESTOP_DIR
        }
    
    def _run_command(self, command: list, timeout: int = 300) -> Tuple[int, str, str]:
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
    
    def create_backup(self, backup_type: str) -> Dict[str, any]:
        """
        Crée un backup
        
        Args:
            backup_type: Type de backup (fast, daily, boot, prestop)
            
        Returns:
            Dict avec success, message, error
        """
        if backup_type not in self.backup_types:
            return {
                "success": False,
                "message": f"Type de backup invalide: {backup_type}",
                "error": "Types valides: fast, daily, boot, prestop"
            }
        
        if not os.path.exists(paths.SCRIPT_BACKUP):
            return {
                "success": False,
                "message": "Script de backup introuvable",
                "error": f"Fichier manquant: {paths.SCRIPT_BACKUP}"
            }
        
        print(f"⏳ Création du backup {backup_type}...")
        
        returncode, stdout, stderr = self._run_command([
            "bash", paths.SCRIPT_BACKUP, backup_type
        ], timeout=600)
        
        if returncode == 0:
            return {
                "success": True,
                "message": f"Backup {backup_type} créé avec succès",
                "error": None
            }
        else:
            return {
                "success": False,
                "message": f"Échec de la création du backup {backup_type}",
                "error": stderr or "Erreur inconnue"
            }
    
    def list_backups(self, backup_type: Optional[str] = None) -> Dict[str, any]:
        """
        Liste les backups disponibles
        
        Args:
            backup_type: Type de backup à lister (None = tous)
            
        Returns:
            Dict avec success, backups (dict), error
        """
        backups_info = {}
        
        types_to_check = [backup_type] if backup_type else self.backup_types.keys()
        
        for btype in types_to_check:
            if btype not in self.backup_types:
                continue
            
            backup_dir = self.backup_types[btype]
            
            if not os.path.exists(backup_dir):
                backups_info[btype] = {
                    "count": 0,
                    "files": [],
                    "total_size": 0,
                    "error": "Dossier inexistant"
                }
                continue
            
            try:
                files = []
                total_size = 0
                
                for entry in os.scandir(backup_dir):
                    if entry.is_file():
                        stat = entry.stat()
                        files.append({
                            "name": entry.name,
                            "size": stat.st_size,
                            "mtime": datetime.fromtimestamp(stat.st_mtime),
                            "path": entry.path
                        })
                        total_size += stat.st_size
                
                # Trier par date (plus récent en premier)
                files.sort(key=lambda x: x["mtime"], reverse=True)
                
                backups_info[btype] = {
                    "count": len(files),
                    "files": files,
                    "total_size": total_size,
                    "error": None
                }
                
            except Exception as e:
                backups_info[btype] = {
                    "count": 0,
                    "files": [],
                    "total_size": 0,
                    "error": str(e)
                }
        
        return {
            "success": True,
            "backups": backups_info,
            "error": None
        }
    
    def format_size(self, size_bytes: int) -> str:
        """Formate une taille en octets en format lisible"""
        for unit in ['o', 'Ko', 'Mo', 'Go', 'To']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} Po"
    
    def get_backups_summary(self) -> str:
        """Retourne un résumé formaté des backups"""
        result = self.list_backups()
        
        if not result["success"]:
            return f"❌ Erreur: {result['error']}"
        
        output = []
        output.append("═" * 60)
        output.append("  RÉSUMÉ DES BACKUPS")
        output.append("═" * 60)
        output.append("")
        
        for btype, info in result["backups"].items():
            output.append(f"📦 {btype.upper()}")
            output.append(f"   Nombre: {info['count']}")
            output.append(f"   Taille totale: {self.format_size(info['total_size'])}")
            
            if info['error']:
                output.append(f"   ⚠️  Erreur: {info['error']}")
            elif info['count'] > 0:
                latest = info['files'][0]
                output.append(f"   Plus récent: {latest['name']}")
                output.append(f"   Date: {latest['mtime'].strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                output.append("   (Aucun backup)")
            
            output.append("")
        
        output.append("═" * 60)
        return "\n".join(output)
    
    def get_detailed_list(self, backup_type: str, limit: int = 10) -> str:
        """Retourne une liste détaillée des backups d'un type"""
        result = self.list_backups(backup_type)
        
        if not result["success"]:
            return f"❌ Erreur: {result['error']}"
        
        info = result["backups"].get(backup_type)
        if not info:
            return f"❌ Type de backup invalide: {backup_type}"
        
        output = []
        output.append("═" * 60)
        output.append(f"  BACKUPS {backup_type.upper()}")
        output.append("═" * 60)
        output.append("")
        
        if info['error']:
            output.append(f"⚠️  Erreur: {info['error']}")
        elif info['count'] == 0:
            output.append("ℹ️  Aucun backup disponible")
        else:
            output.append(f"Total: {info['count']} backup(s) - {self.format_size(info['total_size'])}")
            output.append("")
            
            for idx, file_info in enumerate(info['files'][:limit], 1):
                output.append(f"[{idx}] {file_info['name']}")
                output.append(f"    Taille: {self.format_size(file_info['size'])}")
                output.append(f"    Date: {file_info['mtime'].strftime('%Y-%m-%d %H:%M:%S')}")
                output.append("")
            
            if info['count'] > limit:
                output.append(f"... et {info['count'] - limit} autre(s)")
        
        output.append("═" * 60)
        return "\n".join(output)
