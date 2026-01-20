#!/usr/bin/env bash
# /home/arkserver/arkserver/core/ark-update-check.sh
# Check non-intrusif pour ARK (app id 376030)
# Retour:
# 0 = OK (ou fallback OK)
# 1 = update disponible
# 2 = erreur critique

set -euo pipefail

ARK_ROOT="/home/arkserver/arkserver"
LOG_DIR="${ARK_ROOT}/logs"
UPDATE_LOG="${LOG_DIR}/update-check.log"
STEAMCMD="/home/arkserver/steamcmd/steamcmd.sh"
APPID="376030"
LOCAL_ACF="${ARK_ROOT}/steamapps/appmanifest_${APPID}.acf"
TMP_OUT=$(mktemp /tmp/ark_appinfo_${APPID}_XXXXXX.txt)
TIMEOUT_CMD="timeout 15s"

mkdir -p "$LOG_DIR"
exec > >(tee -a "$UPDATE_LOG") 2>&1

# Nettoyage en cas de sortie
trap 'rm -f "$TMP_OUT" 2>/dev/null || true' EXIT

echo "[$(date +'%F %T')] [UpdateCheck] Vérification de mise à jour ARK..."

# Fonction : génération sortie JSON
output_json() {
    local STATUS="$1"
    local LOCAL="${2:-unknown}"
    local REMOTE="${3:-unknown}"
    printf '{"status":"%s","local_build":"%s","remote_build":"%s"}\n' "$STATUS" "$LOCAL" "$REMOTE"
}

# 1) steamcmd présent ?
if [ ! -x "$STEAMCMD" ]; then
    echo "[$(date +'%F %T')] [UpdateCheck] steamcmd non trouvé à $STEAMCMD, fallback: considérer OK."
    output_json "ok" "unknown" "unknown"
    exit 0
fi

# 2) interroger Steam (timeout)
echo "[$(date +'%F %T')] [UpdateCheck] Interrogation de Steam pour AppID $APPID..."
if ! $TIMEOUT_CMD "$STEAMCMD" +login anonymous +app_info_print "$APPID" +quit > "$TMP_OUT" 2>/dev/null; then
    STEAM_RC=$?
    echo "[$(date +'%F %T')] [UpdateCheck] Échec interrogation Steam (RC=$STEAM_RC). Fallback: considérer OK."
    output_json "ok" "unknown" "unknown"
    exit 0
fi

# 3) Parse buildid distant (robuste avec awk)
REMOTE_BUILD=$(awk '/^\s*"buildid"\s*"[0-9]+"/ {gsub(/[^0-9]/,"",$2); print $2; exit}' "$TMP_OUT")

# Validation du buildid distant
if [ -z "$REMOTE_BUILD" ]; then
    echo "[$(date +'%F %T')] [UpdateCheck] Impossible d'extraire buildid distant. Fallback: considérer OK."
    output_json "ok" "unknown" "unknown"
    exit 0
fi

if ! [[ "$REMOTE_BUILD" =~ ^[0-9]+$ ]]; then
    echo "[$(date +'%F %T')] [UpdateCheck] buildid distant invalide: '$REMOTE_BUILD'. Fallback: considérer OK."
    output_json "ok" "unknown" "$REMOTE_BUILD"
    exit 0
fi

# 4) Parse buildid local
if [ -f "$LOCAL_ACF" ]; then
    LOCAL_BUILD=$(awk '/^\s*"buildid"\s*"[0-9]+"/ {gsub(/[^0-9]/,"",$2); print $2; exit}' "$LOCAL_ACF")
else
    LOCAL_BUILD=""
fi

echo "[$(date +'%F %T')] [UpdateCheck] remote_build=${REMOTE_BUILD} local_build=${LOCAL_BUILD:-<none>}"

# Validation du buildid local
if [ -z "$LOCAL_BUILD" ]; then
    echo "[$(date +'%F %T')] [UpdateCheck] appmanifest local absent ou buildid non trouvé. Considéré OK."
    output_json "ok" "unknown" "$REMOTE_BUILD"
    exit 0
fi

if ! [[ "$LOCAL_BUILD" =~ ^[0-9]+$ ]]; then
    echo "[$(date +'%F %T')] [UpdateCheck] buildid local invalide: '$LOCAL_BUILD'. Erreur critique."
    output_json "error" "$LOCAL_BUILD" "$REMOTE_BUILD"
    exit 2
fi

# 5) Comparaison
if [ "$REMOTE_BUILD" != "$LOCAL_BUILD" ]; then
    echo "[$(date +'%F %T')] [UpdateCheck] Mise à jour disponible (remote=$REMOTE_BUILD != local=$LOCAL_BUILD)."
    output_json "update_available" "$LOCAL_BUILD" "$REMOTE_BUILD"
    exit 1
else
    echo "[$(date +'%F %T')] [UpdateCheck] Version OK (build=$LOCAL_BUILD)."
    output_json "ok" "$LOCAL_BUILD" "$REMOTE_BUILD"
    exit 0
fi