#!/usr/bin/env python3
"""
Chemins centralisés pour le serveur ARK
Tous les chemins absolus de la VM sont définis ici
"""

# Racines principales
ARK_ROOT = "/home/arkserver/arkserver"
STEAM_ROOT = "/home/arkserver/Steam"
STEAMCMD_ROOT = "/home/arkserver/steamcmd"

# Dossiers ARK
CORE_DIR = f"{ARK_ROOT}/core"
CONFIG_DIR = f"{ARK_ROOT}/config"
BACKUP_DIR = f"{ARK_ROOT}/backups"
LOGS_DIR = f"{ARK_ROOT}/logs"
SHOOTER_GAME_DIR = f"{ARK_ROOT}/ShooterGame"
SAVED_DIR = f"{SHOOTER_GAME_DIR}/Saved"
CONTENT_DIR = f"{SHOOTER_GAME_DIR}/Content"
MODS_DIR = f"{CONTENT_DIR}/Mods"

# Chemins officiels ARK
ARK_CONFIG_DIR = f"{SAVED_DIR}/Config/LinuxServer"
ARK_BINARIES_DIR = f"{SHOOTER_GAME_DIR}/Binaries/Linux"
ARK_SERVER_BIN = f"{ARK_BINARIES_DIR}/ShooterGameServer"

# Workshop Steam
WORKSHOP_DIR = f"{STEAM_ROOT}/steamapps/workshop/content/346110"
STEAMCMD = f"{STEAMCMD_ROOT}/steamcmd.sh"

# Scripts core (bash)
SCRIPT_CORE = f"{CORE_DIR}/ark-core.sh"
SCRIPT_STOP = f"{CORE_DIR}/ark-stop.sh"
SCRIPT_MODS = f"{CORE_DIR}/ark-mods.sh"
SCRIPT_UPDATE = f"{CORE_DIR}/ark-update-check.sh"
SCRIPT_BACKUP = f"{CORE_DIR}/ark-backup.sh"

# Fichiers de configuration
MODS_LIST = f"{CONFIG_DIR}/mods.list"
SETTINGS_CONF = f"{CONFIG_DIR}/settings.conf"
CURRENT_MAP_FILE = f"{CONFIG_DIR}/current_map"
GAME_USER_SETTINGS_INI = f"{ARK_CONFIG_DIR}/GameUserSettings.ini"
GAME_INI = f"{ARK_CONFIG_DIR}/Game.ini"

# Fichiers de logs
CORE_LOG = f"{LOGS_DIR}/core.log"
BACKUP_LOG = f"{LOGS_DIR}/backup.log"
MODS_LOG = f"{LOGS_DIR}/mods.log"
UPDATE_LOG = f"{LOGS_DIR}/update-check.log"

# Dossiers de backup par type
BACKUP_FAST_DIR = f"{BACKUP_DIR}/fast"
BACKUP_DAILY_DIR = f"{BACKUP_DIR}/daily"
BACKUP_BOOT_DIR = f"{BACKUP_DIR}/boot"
BACKUP_PRESTOP_DIR = f"{BACKUP_DIR}/prestop"

# App IDs Steam
ARK_APP_ID = "376030"
ARK_WORKSHOP_ID = "346110"
