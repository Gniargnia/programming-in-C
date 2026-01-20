#!/usr/bin/env python3
"""
Module de gestion des cartes (maps) ARK
Changement de carte, liste des maps disponibles
"""

import os
from typing import Dict, List
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import paths


class MapsManager:
    """Gestionnaire des cartes ARK"""
    
    # Maps officielles disponibles (organisées par catégorie)
    OFFICIAL_MAPS = {
        "base": {
            "TheIsland": "The Island (carte de base)",
            "TheCenter": "The Center (gratuite)",
            "Ragnarok": "Ragnarok (gratuite)",
        },
        "dlc_paid": {
            "ScorchedEarth": "Scorched Earth (DLC payant)",
            "Aberration": "Aberration (DLC payant)",
            "Extinction": "Extinction (DLC payant)",
            "Genesis": "Genesis Part 1 (DLC payant)",
            "Genesis2": "Genesis Part 2 (DLC payant)",
        },
        "free_expansion": {
            "Valguero": "Valguero (gratuite)",
            "CrystalIsles": "Crystal Isles (gratuite)",
            "LostIsland": "Lost Island (gratuite)",
            "Fjordur": "Fjordur (gratuite)",
        }
    }
    
    def get_current_map(self) -> Dict[str, any]:
        """
        Récupère la carte actuellement configurée
        
        Returns:
            Dict avec: success, map_name, error
        """
        if not os.path.exists(paths.CURRENT_MAP_FILE):
            return {
                "success": False,
                "map_name": None,
                "error": f"Fichier current_map introuvable: {paths.CURRENT_MAP_FILE}"
            }
        
        try:
            with open(paths.CURRENT_MAP_FILE, 'r') as f:
                map_name = f.read().strip()
            
            return {
                "success": True,
                "map_name": map_name,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "map_name": None,
                "error": str(e)
            }
    
    def set_map(self, map_name: str) -> Dict[str, any]:
        """
        Change la carte configurée
        
        Args:
            map_name: Nom de la carte (ex: TheIsland, Ragnarok)
            
        Returns:
            Dict avec: success, message, error
        """
        # Valider que la carte existe
        if not self.is_valid_map(map_name):
            return {
                "success": False,
                "message": f"Carte invalide: {map_name}",
                "error": "Carte non reconnue ou non installée"
            }
        
        try:
            with open(paths.CURRENT_MAP_FILE, 'w') as f:
                f.write(map_name)
            
            return {
                "success": True,
                "message": f"Carte changée pour: {map_name}",
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Échec de l'écriture du fichier",
                "error": str(e)
            }
    
    def is_valid_map(self, map_name: str) -> bool:
        """
        Vérifie si une carte est valide (existe dans le système de fichiers)
        
        Args:
            map_name: Nom de la carte
            
        Returns:
            True si la carte existe, False sinon
        """
        # Vérifier dans Content/Maps/
        map_dir1 = os.path.join(paths.CONTENT_DIR, "Maps", map_name)
        # Vérifier dans Content/Maps/{MapName}SubMaps/
        map_dir2 = os.path.join(paths.CONTENT_DIR, "Maps", f"{map_name}SubMaps")
        # Vérifier directement dans Content/ (pour certaines maps)
        map_dir3 = os.path.join(paths.CONTENT_DIR, map_name)
        # Vérifier dans Content/Mods/ (maps communautaires intégrées)
        map_dir4 = os.path.join(paths.MODS_DIR, map_name)
        
        return (os.path.exists(map_dir1) or 
                os.path.exists(map_dir2) or 
                os.path.exists(map_dir3) or
                os.path.exists(map_dir4))
    
    def get_available_maps(self) -> Dict[str, any]:
        """
        Liste toutes les cartes disponibles (installées sur le serveur)
        
        Returns:
            Dict avec: success, maps (dict par catégorie), error
        """
        available = {
            "base": [],
            "dlc_paid": [],
            "free_expansion": []
        }
        
        # Vérifier chaque carte officielle
        for category, maps in self.OFFICIAL_MAPS.items():
            for map_name, description in maps.items():
                if self.is_valid_map(map_name):
                    available[category].append({
                        "name": map_name,
                        "description": description
                    })
        
        return {
            "success": True,
            "maps": available,
            "error": None
        }
    
    def format_maps_list(self) -> str:
        """Retourne une liste formatée des cartes disponibles"""
        result = self.get_available_maps()
        current_result = self.get_current_map()
        
        output = []
        output.append("═" * 60)
        output.append("  CARTES ARK DISPONIBLES")
        output.append("═" * 60)
        output.append("")
        
        if current_result["success"]:
            output.append(f"🗺️  Carte actuelle: {current_result['map_name']}")
            output.append("")
        
        if not result["success"]:
            output.append(f"❌ Erreur: {result['error']}")
            return "\n".join(output)
        
        maps = result["maps"]
        
        # Cartes de base
        if maps["base"]:
            output.append("📦 CARTES DE BASE")
            for map_info in maps["base"]:
                current = " ⭐" if current_result["success"] and current_result["map_name"] == map_info["name"] else ""
                output.append(f"   • {map_info['name']}{current}")
                output.append(f"     {map_info['description']}")
            output.append("")
        
        # DLC payants
        if maps["dlc_paid"]:
            output.append("💰 DLC PAYANTS")
            for map_info in maps["dlc_paid"]:
                current = " ⭐" if current_result["success"] and current_result["map_name"] == map_info["name"] else ""
                output.append(f"   • {map_info['name']}{current}")
                output.append(f"     {map_info['description']}")
            output.append("")
        
        # Extensions gratuites
        if maps["free_expansion"]:
            output.append("🆓 EXTENSIONS GRATUITES")
            for map_info in maps["free_expansion"]:
                current = " ⭐" if current_result["success"] and current_result["map_name"] == map_info["name"] else ""
                output.append(f"   • {map_info['name']}{current}")
                output.append(f"     {map_info['description']}")
            output.append("")
        
        output.append("⭐ = Carte actuellement configurée")
        output.append("")
        output.append("═" * 60)
        
        return "\n".join(output)
    
    def get_all_map_names(self) -> List[str]:
        """Retourne la liste de tous les noms de cartes disponibles"""
        result = self.get_available_maps()
        if not result["success"]:
            return []
        
        all_names = []
        for category_maps in result["maps"].values():
            for map_info in category_maps:
                all_names.append(map_info["name"])
        
        return all_names
