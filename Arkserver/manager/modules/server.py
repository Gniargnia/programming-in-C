#!/usr/bin/env python3
"""
Module de gestion du serveur ARK
Interface Python vers les scripts Bash système (ark-core.sh, ark-stop.sh)
"""

import subprocess
import time
from typing import Dict, Optional, Tuple
import sys
import os

# Import du module paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import paths


class ServerManager:
    """Gestionnaire du serveur ARK"""
    
    def __init__(self):
        """Initialise le gestionnaire"""
        self.service_name = "ark-core.service"
    
    def _run_command(self, command: list, timeout: int = 30) -> Tuple[int, str, str]:
        """
        Exécute une commande et retourne le résultat
        
        Args:
            command: Liste des arguments de la commande
            timeout: Timeout en secondes
            
        Returns:
            Tuple (returncode, stdout, stderr)
        """
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
    
    def get_status(self) -> Dict[str, any]:
        """
        Récupère le statut du serveur
        
        Returns:
            Dict avec: running (bool), pid (int|None), uptime (str|None), error (str|None)
        """
        # Méthode 1: Via systemctl (si service existe)
        returncode, stdout, stderr = self._run_command([
            "systemctl", "is-active", self.service_name
        ])
        
        is_active = (returncode == 0 and stdout.strip() == "active")
        
        # Méthode 2: Via ps pour trouver le processus ShooterGameServer
        returncode_ps, stdout_ps, _ = self._run_command([
            "pgrep", "-f", "ShooterGameServer"
        ])
        
        pid = None
        if returncode_ps == 0 and stdout_ps.strip():
            try:
                pid = int(stdout_ps.strip().split('\n')[0])
            except (ValueError, IndexError):
                pid = None
        
        # Récupérer uptime si actif
        uptime = None
        if is_active:
            returncode_uptime, stdout_uptime, _ = self._run_command([
                "systemctl", "show", self.service_name, "--property=ActiveEnterTimestamp"
            ])
            if returncode_uptime == 0:
                uptime = stdout_uptime.strip()
        
        return {
            "running": is_active or (pid is not None),
            "pid": pid,
            "uptime": uptime,
            "service_active": is_active,
            "error": None if (is_active or pid) else "Serveur arrêté"
        }
    
    def start(self) -> Dict[str, any]:
        """
        Démarre le serveur via systemctl ou script direct
        
        Returns:
            Dict avec: success (bool), message (str), error (str|None)
        """
        # Vérifier si déjà actif
        status = self.get_status()
        if status["running"]:
            return {
                "success": False,
                "message": "Le serveur est déjà en cours d'exécution",
                "error": None
            }
        
        # Tenter démarrage via systemctl
        returncode, stdout, stderr = self._run_command([
            "sudo", "systemctl", "start", self.service_name
        ], timeout=60)
        
        if returncode == 0:
            # Attendre quelques secondes et vérifier
            time.sleep(3)
            status = self.get_status()
            
            if status["running"]:
                return {
                    "success": True,
                    "message": f"Serveur démarré avec succès (PID: {status['pid']})",
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "message": "Le serveur n'a pas démarré correctement",
                    "error": "Service lancé mais processus non trouvé"
                }
        else:
            # Échec systemctl, essayer script direct
            if os.path.exists(paths.SCRIPT_CORE):
                returncode_script, stdout_script, stderr_script = self._run_command([
                    "bash", paths.SCRIPT_CORE
                ], timeout=60)
                
                if returncode_script == 0:
                    return {
                        "success": True,
                        "message": "Serveur démarré via script direct",
                        "error": None
                    }
                else:
                    return {
                        "success": False,
                        "message": "Échec du démarrage",
                        "error": stderr_script or "Erreur script"
                    }
            else:
                return {
                    "success": False,
                    "message": "Impossible de démarrer le serveur",
                    "error": f"systemctl: {stderr}, script introuvable: {paths.SCRIPT_CORE}"
                }
    
    def stop(self, graceful: bool = True) -> Dict[str, any]:
        """
        Arrête le serveur
        
        Args:
            graceful: Si True, arrêt propre avec backup (ark-stop.sh)
            
        Returns:
            Dict avec: success (bool), message (str), error (str|None)
        """
        # Vérifier si actif
        status = self.get_status()
        if not status["running"]:
            return {
                "success": False,
                "message": "Le serveur est déjà arrêté",
                "error": None
            }
        
        if graceful and os.path.exists(paths.SCRIPT_STOP):
            # Arrêt propre via script
            print("⏳ Arrêt propre du serveur (backup + stop)...")
            returncode, stdout, stderr = self._run_command([
                "bash", paths.SCRIPT_STOP
            ], timeout=120)
            
            if returncode == 0:
                return {
                    "success": True,
                    "message": "Serveur arrêté proprement (avec backup)",
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "message": "Erreur lors de l'arrêt propre",
                    "error": stderr
                }
        else:
            # Arrêt via systemctl
            returncode, stdout, stderr = self._run_command([
                "sudo", "systemctl", "stop", self.service_name
            ], timeout=60)
            
            if returncode == 0:
                return {
                    "success": True,
                    "message": "Serveur arrêté via systemctl",
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "message": "Échec de l'arrêt",
                    "error": stderr
                }
    
    def restart(self, graceful: bool = True) -> Dict[str, any]:
        """
        Redémarre le serveur
        
        Args:
            graceful: Si True, arrêt propre avant redémarrage
            
        Returns:
            Dict avec: success (bool), message (str), error (str|None)
        """
        # Arrêter le serveur
        stop_result = self.stop(graceful=graceful)
        
        if not stop_result["success"] and stop_result["message"] != "Le serveur est déjà arrêté":
            return {
                "success": False,
                "message": "Échec de l'arrêt lors du redémarrage",
                "error": stop_result["error"]
            }
        
        # Attendre que le processus soit complètement arrêté
        print("⏳ Attente de l'arrêt complet...")
        for i in range(10):
            time.sleep(2)
            status = self.get_status()
            if not status["running"]:
                break
        
        # Démarrer le serveur
        start_result = self.start()
        
        if start_result["success"]:
            return {
                "success": True,
                "message": "Serveur redémarré avec succès",
                "error": None
            }
        else:
            return {
                "success": False,
                "message": "Serveur arrêté mais échec du redémarrage",
                "error": start_result["error"]
            }
    
    def get_detailed_status(self) -> str:
        """
        Retourne un statut détaillé formaté pour affichage
        
        Returns:
            Chaîne formatée avec les infos du serveur
        """
        status = self.get_status()
        
        output = []
        output.append("═" * 60)
        output.append("  STATUT DU SERVEUR ARK")
        output.append("═" * 60)
        output.append("")
        
        if status["running"]:
            output.append("✅ État: EN LIGNE")
            if status["pid"]:
                output.append(f"🔢 PID: {status['pid']}")
            if status["service_active"]:
                output.append(f"⚙️  Service: {self.service_name} (actif)")
            if status["uptime"]:
                output.append(f"⏱️  Uptime: {status['uptime']}")
        else:
            output.append("❌ État: HORS LIGNE")
            if status["error"]:
                output.append(f"ℹ️  Info: {status['error']}")
        
        output.append("")
        output.append("═" * 60)
        
        return "\n".join(output)
