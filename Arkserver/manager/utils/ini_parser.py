#!/usr/bin/env python3
"""
Parser INI spécialisé pour les fichiers de configuration ARK
Gère les particularités du format ARK (sections complexes, lignes longues, clés répétées)
"""

import re
from typing import Dict, List, Tuple, Optional


class ArkINIParser:
    """
    Parser conservateur pour les fichiers INI d'ARK
    Préserve la structure exacte du fichier, y compris les lignes complexes
    """
    
    def __init__(self, file_path: str):
        """
        Initialise le parser avec un fichier INI
        
        Args:
            file_path: Chemin absolu vers le fichier INI
        """
        self.file_path = file_path
        self.lines: List[str] = []
        self.sections: Dict[str, List[int]] = {}  # section_name -> [line_indices]
        
    def read(self) -> None:
        """
        Lit le fichier INI et construit l'index des sections
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.lines = f.readlines()
        except FileNotFoundError:
            self.lines = []
            return
            
        current_section = None
        
        for idx, line in enumerate(self.lines):
            # Détection de section : [SectionName]
            section_match = re.match(r'^\[(.+)\]', line.strip())
            if section_match:
                current_section = section_match.group(1)
                if current_section not in self.sections:
                    self.sections[current_section] = []
            elif current_section:
                # Ligne appartient à la section courante
                self.sections[current_section].append(idx)
    
    def get_value(self, section: str, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Récupère la valeur d'une clé dans une section
        
        Args:
            section: Nom de la section
            key: Nom de la clé
            default: Valeur par défaut si non trouvée
            
        Returns:
            La valeur de la clé ou default si non trouvée
        """
        if section not in self.sections:
            return default
            
        for line_idx in self.sections[section]:
            line = self.lines[line_idx].strip()
            
            # Ignore les lignes vides et commentaires
            if not line or line.startswith('#') or line.startswith(';'):
                continue
                
            # Parse key=value
            match = re.match(rf'^{re.escape(key)}=(.*)$', line)
            if match:
                return match.group(1)
                
        return default
    
    def set_value(self, section: str, key: str, value: str) -> bool:
        """
        Modifie la valeur d'une clé dans une section
        Si la clé n'existe pas, elle est ajoutée à la fin de la section
        
        Args:
            section: Nom de la section
            key: Nom de la clé
            value: Nouvelle valeur
            
        Returns:
            True si la modification a réussi, False sinon
        """
        # Si la section n'existe pas, on ne peut pas modifier
        if section not in self.sections:
            return False
            
        # Chercher la clé existante
        for line_idx in self.sections[section]:
            line = self.lines[line_idx].strip()
            
            if line.startswith(key + '='):
                # Modifier la ligne existante
                self.lines[line_idx] = f"{key}={value}\n"
                return True
        
        # Clé non trouvée : ajouter à la fin de la section
        if self.sections[section]:
            last_line_idx = self.sections[section][-1]
            # Insérer après la dernière ligne de la section
            self.lines.insert(last_line_idx + 1, f"{key}={value}\n")
            # Mettre à jour les indices de toutes les sections suivantes
            self._update_section_indices_after_insert(last_line_idx + 1)
        
        return True
    
    def add_section(self, section: str) -> bool:
        """
        Ajoute une nouvelle section au fichier
        
        Args:
            section: Nom de la section à ajouter
            
        Returns:
            True si ajoutée, False si elle existe déjà
        """
        if section in self.sections:
            return False
            
        # Ajouter la section à la fin du fichier
        self.lines.append(f"\n[{section}]\n")
        self.sections[section] = []
        
        return True
    
    def ensure_key(self, section: str, key: str, default_value: str) -> None:
        """
        S'assure qu'une clé existe dans une section, sinon la crée avec default_value
        
        Args:
            section: Nom de la section
            key: Nom de la clé
            default_value: Valeur par défaut
        """
        if section not in self.sections:
            self.add_section(section)
            
        if self.get_value(section, key) is None:
            self.set_value(section, key, default_value)
    
    def write(self) -> None:
        """
        Écrit les modifications dans le fichier INI
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)
    
    def _update_section_indices_after_insert(self, insert_idx: int) -> None:
        """
        Met à jour les indices de toutes les sections après une insertion de ligne
        
        Args:
            insert_idx: Index où la ligne a été insérée
        """
        for section_name, indices in self.sections.items():
            self.sections[section_name] = [
                idx + 1 if idx >= insert_idx else idx
                for idx in indices
            ]
    
    def get_all_values(self, section: str, key: str) -> List[str]:
        """
        Récupère toutes les valeurs d'une clé répétée (pour les arrays ARK)
        
        Args:
            section: Nom de la section
            key: Nom de la clé
            
        Returns:
            Liste des valeurs trouvées
        """
        values = []
        
        if section not in self.sections:
            return values
            
        for line_idx in self.sections[section]:
            line = self.lines[line_idx].strip()
            
            if not line or line.startswith('#') or line.startswith(';'):
                continue
                
            match = re.match(rf'^{re.escape(key)}=(.*)$', line)
            if match:
                values.append(match.group(1))
                
        return values


def read_simple_config(file_path: str) -> Dict[str, str]:
    """
    Lit un fichier de configuration simple (key=value sans sections)
    Utilisé pour settings.conf
    
    Args:
        file_path: Chemin vers le fichier
        
    Returns:
        Dictionnaire {key: value}
    """
    config = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Ignorer lignes vides et commentaires
                if not line or line.startswith('#'):
                    continue
                    
                # Parse key=value
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Retirer les quotes si présentes
                    value = value.strip().strip('"').strip("'")
                    config[key.strip()] = value
    except FileNotFoundError:
        pass
        
    return config


def write_simple_config(file_path: str, config: Dict[str, str], header: Optional[str] = None) -> None:
    """
    Écrit un fichier de configuration simple (key=value sans sections)
    
    Args:
        file_path: Chemin vers le fichier
        config: Dictionnaire {key: value}
        header: Commentaire d'en-tête optionnel
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        if header:
            f.write(f"# {header}\n\n")
            
        for key, value in config.items():
            # Ajouter des quotes si la valeur contient des espaces
            if ' ' in value:
                f.write(f'{key}="{value}"\n')
            else:
                f.write(f'{key}={value}\n')
