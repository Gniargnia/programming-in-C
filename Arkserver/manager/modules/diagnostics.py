#!/usr/bin/env python3
"""
Module de diagnostics et monitoring ARK
Logs, ressources système, vérifications
"""

import subprocess
import os
from typing import Dict, Tuple, Optional
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import paths


class DiagnosticsManager:
    """Gestionnaire des diagnostics et monitoring"""
    
    def _run_command(self, command: list, timeout: int = 30) -> Tuple[int, str, str]:
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
    
    def get_log(self, log_type: str, lines: int = 50) -> Dict[str, any]:
        """
        Récupère les dernières lignes d'un log
        
        Args:
            log_type: Type de log (core, backup, mods, update)
            lines: Nombre de lignes à afficher
            
        Returns:
            Dict avec: success, content, error
        """
        log_files = {
            "core": paths.CORE_LOG,
            "backup": paths.BACKUP_LOG,
            "mods": paths.MODS_LOG,
            "update": paths.UPDATE_LOG
        }
        
        if log_type not in log_files:
            return {
                "success": False,
                "content": "",
                "error": f"Type de log invalide. Options: {', '.join(log_files.keys())}"
            }
        
        log_path = log_files[log_type]
        
        if not os.path.exists(log_path):
            return {
                "success": False,
                "content": "",
                "error": f"Fichier de log introuvable: {log_path}"
            }
        
        returncode, stdout, stderr = self._run_command([
            "tail", "-n", str(lines), log_path
        ])
        
        if returncode == 0:
            return {
                "success": True,
                "content": stdout,
                "error": None
            }
        else:
            return {
                "success": False,
                "content": "",
                "error": stderr or "Erreur lecture log"
            }
    
    def get_system_resources(self) -> Dict[str, any]:
        """
        Récupère les ressources système (CPU, RAM, Disque)
        
        Returns:
            Dict avec: cpu, ram, disk, error
        """
        resources = {}
        
        # CPU usage
        returncode, stdout, _ = self._run_command([
            "bash", "-c",
            "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'"
        ])
        if returncode == 0:
            try:
                resources["cpu"] = float(stdout.strip())
            except ValueError:
                resources["cpu"] = None
        
        # RAM usage
        returncode, stdout, _ = self._run_command([
            "free", "-m"
        ])
        if returncode == 0:
            lines = stdout.strip().split('\n')
            if len(lines) >= 2:
                mem_line = lines[1].split()
                if len(mem_line) >= 3:
                    try:
                        total_ram = int(mem_line[1])
                        used_ram = int(mem_line[2])
                        resources["ram"] = {
                            "total": total_ram,
                            "used": used_ram,
                            "percent": (used_ram / total_ram * 100) if total_ram > 0 else 0
                        }
                    except (ValueError, IndexError):
                        resources["ram"] = None
        
        # Disk usage (partition du serveur ARK)
        returncode, stdout, _ = self._run_command([
            "df", "-h", paths.ARK_ROOT
        ])
        if returncode == 0:
            lines = stdout.strip().split('\n')
            if len(lines) >= 2:
                disk_line = lines[1].split()
                if len(disk_line) >= 5:
                    resources["disk"] = {
                        "total": disk_line[1],
                        "used": disk_line[2],
                        "available": disk_line[3],
                        "percent": disk_line[4]
                    }
        
        return {
            "success": True,
            "resources": resources,
            "error": None
        }
    
    def get_server_info(self) -> Dict[str, any]:
        """
        Récupère les informations système
        
        Returns:
            Dict avec: hostname, uptime, kernel, error
        """
        info = {}
        
        # Hostname
        returncode, stdout, _ = self._run_command(["hostname"])
        if returncode == 0:
            info["hostname"] = stdout.strip()
        
        # Uptime
        returncode, stdout, _ = self._run_command(["uptime", "-p"])
        if returncode == 0:
            info["uptime"] = stdout.strip()
        
        # Kernel
        returncode, stdout, _ = self._run_command(["uname", "-r"])
        if returncode == 0:
            info["kernel"] = stdout.strip()
        
        # OS
        returncode, stdout, _ = self._run_command(["lsb_release", "-d"])
        if returncode == 0:
            info["os"] = stdout.strip().replace("Description:", "").strip()
        
        return {
            "success": True,
            "info": info,
            "error": None
        }
    
    def format_resources_display(self) -> str:
        """Retourne un affichage formaté des ressources"""
        result = self.get_system_resources()
        
        output = []
        output.append("═" * 60)
        output.append("  RESSOURCES SYSTÈME")
        output.append("═" * 60)
        output.append("")
        
        if not result["success"]:
            output.append(f"❌ Erreur: {result['error']}")
            return "\n".join(output)
        
        res = result["resources"]
        
        # CPU
        if "cpu" in res and res["cpu"] is not None:
            cpu_percent = res["cpu"]
            cpu_bar = self._create_bar(cpu_percent)
            output.append(f"🖥️  CPU: {cpu_percent:.1f}% {cpu_bar}")
        
        # RAM
        if "ram" in res and res["ram"]:
            ram = res["ram"]
            ram_bar = self._create_bar(ram["percent"])
            output.append(f"💾 RAM: {ram['used']}Mo / {ram['total']}Mo ({ram['percent']:.1f}%) {ram_bar}")
        
        # Disk
        if "disk" in res and res["disk"]:
            disk = res["disk"]
            output.append(f"💿 Disque: {disk['used']} / {disk['total']} ({disk['percent']}) - Libre: {disk['available']}")
        
        output.append("")
        output.append("═" * 60)
        return "\n".join(output)
    
    def format_system_info_display(self) -> str:
        """Retourne un affichage formaté des infos système"""
        result = self.get_server_info()
        
        output = []
        output.append("═" * 60)
        output.append("  INFORMATIONS SYSTÈME")
        output.append("═" * 60)
        output.append("")
        
        if not result["success"]:
            output.append(f"❌ Erreur: {result['error']}")
            return "\n".join(output)
        
        info = result["info"]
        
        if "hostname" in info:
            output.append(f"🖥️  Hostname: {info['hostname']}")
        
        if "os" in info:
            output.append(f"🐧 OS: {info['os']}")
        
        if "kernel" in info:
            output.append(f"⚙️  Kernel: {info['kernel']}")
        
        if "uptime" in info:
            output.append(f"⏱️  Uptime: {info['uptime']}")
        
        output.append("")
        output.append("═" * 60)
        return "\n".join(output)
    
    def _create_bar(self, percent: float, width: int = 20) -> str:
        """Crée une barre de progression ASCII"""
        filled = int(width * percent / 100)
        empty = width - filled
        return "[" + "█" * filled + "░" * empty + "]"
    
    def check_integrity(self) -> Dict[str, any]:
        """
        Vérifie l'intégrité du serveur ARK
        
        Returns:
            Dict avec: success, checks (list), error
        """
        checks = []
        
        # Vérifier binaire serveur
        if os.path.exists(paths.ARK_SERVER_BIN) and os.access(paths.ARK_SERVER_BIN, os.X_OK):
            checks.append({"name": "Binaire serveur", "status": "✅ OK"})
        else:
            checks.append({"name": "Binaire serveur", "status": "❌ Manquant ou non exécutable"})
        
        # Vérifier SteamCMD
        if os.path.exists(paths.STEAMCMD) and os.access(paths.STEAMCMD, os.X_OK):
            checks.append({"name": "SteamCMD", "status": "✅ OK"})
        else:
            checks.append({"name": "SteamCMD", "status": "❌ Manquant ou non exécutable"})
        
        # Vérifier scripts core
        scripts = {
            "ark-core.sh": paths.SCRIPT_CORE,
            "ark-stop.sh": paths.SCRIPT_STOP,
            "ark-backup.sh": paths.SCRIPT_BACKUP,
            "ark-mods.sh": paths.SCRIPT_MODS,
            "ark-update-check.sh": paths.SCRIPT_UPDATE
        }
        
        for name, path in scripts.items():
            if os.path.exists(path) and os.access(path, os.X_OK):
                checks.append({"name": name, "status": "✅ OK"})
            else:
                checks.append({"name": name, "status": "❌ Manquant ou non exécutable"})
        
        # Vérifier dossiers critiques
        dirs = {
            "ShooterGame/Saved": paths.SAVED_DIR,
            "ShooterGame/Config": paths.ARK_CONFIG_DIR,
            "Backups": paths.BACKUP_DIR,
            "Logs": paths.LOGS_DIR
        }
        
        for name, path in dirs.items():
            if os.path.exists(path) and os.path.isdir(path):
                checks.append({"name": f"Dossier {name}", "status": "✅ OK"})
            else:
                checks.append({"name": f"Dossier {name}", "status": "❌ Manquant"})
        
        return {
            "success": True,
            "checks": checks,
            "error": None
        }
