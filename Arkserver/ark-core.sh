#!/usr/bin/env bash
# /home/arkserver/arkserver/core/ark-core.sh
# Core minimal : check update une seule fois, si OK -> start ARK; si update -> exit 1

set -euo pipefail

ARK_ROOT="/home/arkserver/arkserver"
ARK_BIN="${ARK_ROOT}/ShooterGame/Binaries/Linux/ShooterGameServer"
CORE_DIR="${ARK_ROOT}/core"
CONFIG_DIR="${ARK_ROOT}/config"
CURRENT_MAP_FILE="${CONFIG_DIR}/current_map"
LOG_DIR="${ARK_ROOT}/logs"
CORE_LOG="${LOG_DIR}/core.log"
UPDATE_CHECK="${CORE_DIR}/ark-update-check.sh"
MODS_CHECK="${CORE_DIR}/ark-mods.sh"

mkdir -p "$LOG_DIR" "$CONFIG_DIR" "$CORE_DIR"

# log both to console and file
exec > >(tee -a "$CORE_LOG") 2>&1

echo "[$(date +'%F %T')] [Core] démarrage du script core."

# sanity checks
if [ ! -x "$ARK_BIN" ]; then
    echo "[$(date +'%F %T')] [Core] ERREUR: binaire ARK introuvable: $ARK_BIN"
    exit 2
fi

if [ ! -f "$CURRENT_MAP_FILE" ]; then
    echo "[$(date +'%F %T')] [Core] current_map absent. Création par défaut 'TheIsland'."
    echo "TheIsland" > "$CURRENT_MAP_FILE"
fi

MAP_NAME=$(tr -d '[:space:]' < "$CURRENT_MAP_FILE")

# Validation filesystem de la map
MAP_DIR1="${ARK_ROOT}/ShooterGame/Content/Maps/${MAP_NAME}"
MAP_DIR2="${ARK_ROOT}/ShooterGame/Content/Maps/${MAP_NAME}SubMaps"

if [ ! -d "$MAP_DIR1" ] && [ ! -d "$MAP_DIR2" ]; then
    echo "[$(date +'%F %T')] [Core] ERREUR: dossier de map introuvable pour '${MAP_NAME}'."
    echo "[$(date +'%F %T')] [Core] Map non valide. Le serveur ne sera pas lancé."
    exit 2
fi


# one-shot update check
echo "[$(date +'%F %T')] [Core] Vérification de mise à jour (one-shot)..."
if [ -x "$UPDATE_CHECK" ]; then
    "$UPDATE_CHECK"
    CHECK_RC=$?
else
    echo "[$(date +'%F %T')] [Core] update-check introuvable, on considère OK."
    CHECK_RC=0
fi

if [ "$CHECK_RC" -ne 0 ]; then
    echo "[$(date +'%F %T')] [Core] Mise à jour détectée. Le serveur NE SERA PAS lancé. (exit $CHECK_RC)"
    exit 1
fi

# one-shot mods check
echo "[$(date +'%F %T')] [Core] Vérification des mods (one-shot)..."
if [ -x "$MODS_CHECK" ]; then
    "$MODS_CHECK" --check
    MODS_RC=$?
else
    echo "[$(date +'%F %T')] [Core] ark-mods.sh introuvable, on considère OK."
    MODS_RC=0
fi

if [ "$MODS_RC" -eq 2 ]; then
    echo "[$(date +'%F %T')] [Core] Erreur critique mods détectée. Le serveur NE SERA PAS lancé. (exit $MODS_RC)"
    exit 2
elif [ "$MODS_RC" -eq 1 ]; then
    echo "[$(date +'%F %T')] [Core] Avertissement mods détecté, mais on continue le démarrage."
fi

# protection anti-double-instance (strict)
if pgrep -f "/ShooterGame/Binaries/Linux/ShooterGameServer" >/dev/null; then
    echo "[$(date +'%F %T')] [Core] ARK déjà en cours d'exécution. Arrêt."
    exit 0
fi

# start ARK
echo "[$(date +'%F %T')] [Core] Version OK. Lancement de ARK (map=${MAP_NAME})..."
cd "$(dirname "$ARK_BIN")" || true

# Charger settings.conf
SETTINGS="${CONFIG_DIR}/settings.conf"
if [ -f "$SETTINGS" ]; then
    # shellcheck disable=SC1090
    source "$SETTINGS"
else
    echo "[$(date +'%F %T')] [Core] settings.conf absent, utilisation des valeurs par défaut."
fi

# Valeurs par défaut si non définies
: "${SESSION_NAME:=MyServer}"
: "${GAME_PORT:=7777}"
: "${QUERY_PORT:=27015}"
: "${RCON_ENABLED:=false}"
: "${MAX_PLAYERS:=10}"
: "${EXTRA_FLAGS:=}"
: "${SERVER_PASSWORD:=}"
: "${SERVER_ADMIN_PASSWORD:=}"

# Générer -mods= depuis mods.list
MODS_FLAG=""
if [ -f "$MOD_FILE" ]; then
    # Extraire les IDs des mods (format: ID|NAME)
    MOD_IDS=$(grep -v '^#' "$MOD_FILE" | grep -v '^$' | cut -d'|' -f1 | tr '\n' ',' | sed 's/,$//')
    
    if [ -n "$MOD_IDS" ]; then
        MODS_FLAG="-mods=${MOD_IDS}"
        echo "[$(date +'%F %T')] [Core] Mods détectés: ${MOD_IDS}"
    else
        echo "[$(date +'%F %T')] [Core] Aucun mod configuré dans mods.list"
    fi
else
    echo "[$(date +'%F %T')] [Core] mods.list absent, aucun mod ne sera chargé"
fi

# Échapper le SessionName
SESSION_NAME_ESCAPED=$(printf '%q' "$SESSION_NAME")

# Construire les arguments ARK
ARK_ARGS="${MAP_NAME}?SessionName=${SESSION_NAME_ESCAPED}&MaxPlayers=${MAX_PLAYERS}&Port=${GAME_PORT}&QueryPort=${QUERY_PORT}"

# RCON si activé
if [ "$RCON_ENABLED" = "true" ] || [ "$RCON_ENABLED" = "1" ]; then
    if [ -z "${RCON_PORT:-}" ]; then
        echo "[$(date +'%F %T')] [Core] AVERTISSEMENT: RCON activé mais RCON_PORT non défini, RCON ignoré."
    elif [ -z "${RCON_PASSWORD:-}" ]; then
        echo "[$(date +'%F %T')] [Core] AVERTISSEMENT: RCON activé mais RCON_PASSWORD non défini, RCON ignoré."
    else
        ARK_ARGS="${ARK_ARGS}&RCONEnabled=true&RCONPort=${RCON_PORT}&RCONPassword=${RCON_PASSWORD}"
    fi
fi

# Mot de passe joueur
if [ -n "${SERVER_PASSWORD}" ]; then
    ARK_ARGS="${ARK_ARGS}&ServerPassword=${SERVER_PASSWORD}"
fi

# Mot de passe admin
if [ -n "${SERVER_ADMIN_PASSWORD}" ]; then
    ARK_ARGS="${ARK_ARGS}&ServerAdminPassword=${SERVER_ADMIN_PASSWORD}"
fi

# Version "safe" pour les logs (mot de passe masqué)
ARK_ARGS_SAFE=$(echo "$ARK_ARGS" \
    | sed -E 's/RCONPassword=[^&]+/RCONPassword=***/' \
    | sed -E 's/ServerPassword=[^&]+/ServerPassword=***/' \
    | sed -E 's/ServerAdminPassword=[^&]+/ServerAdminPassword=***/'
)

echo "[$(date +'%F %T')] [Core] Lancement ARK avec arguments: $ARK_ARGS_SAFE $MODS_FLAG $EXTRA_FLAGS"

# Lancer ARK avec les vrais arguments
exec "$ARK_BIN" $ARK_ARGS -server -log $MODS_FLAG $EXTRA_FLAGS