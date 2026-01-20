#!/usr/bin/env bash
# /home/arkserver/arkserver/core/ark-stop.sh
# Arrêt propre du serveur ARK

set -euo pipefail

ARK_ROOT="/home/arkserver/arkserver"
LOG_DIR="${ARK_ROOT}/logs"
STOP_LOG="${LOG_DIR}/stop.log"

mkdir -p "$LOG_DIR"

exec > >(tee -a "$STOP_LOG") 2>&1

echo "[$(date +'%F %T')] [Stop] Demande d'arrêt du serveur ARK."

# Fonction : génération sortie JSON
output_json() {
    local STATUS="$1"
    local METHOD="${2:-none}"
    local DURATION="${3:-0}"
    printf '{"status":"%s","method":"%s","duration":%d}\n' "$STATUS" "$METHOD" "$DURATION"
}

# Trouver le PID du serveur ARK
PID=$(pgrep -f "/ShooterGame/Binaries/Linux/ShooterGameServer" || true)

if [ -z "$PID" ]; then
    echo "[$(date +'%F %T')] [Stop] Aucun processus ARK trouvé. Rien à arrêter."
    output_json "ok" "none" "0"
    exit 0
fi

echo "[$(date +'%F %T')] [Stop] Processus ARK détecté (PID=$PID). Envoi du signal SIGINT..."

# SIGINT = arrêt propre Unreal Engine
START_TIME=$(date +%s)
kill -INT "$PID"

# Attendre jusqu'à 30 secondes
for i in {1..30}; do
    if ! kill -0 "$PID" 2>/dev/null; then
        ELAPSED=$(($(date +%s) - START_TIME))
        echo "[$(date +'%F %T')] [Stop] ARK s'est arrêté proprement en ${ELAPSED}s."
        output_json "ok" "graceful" "$ELAPSED"
        exit 0
    fi
    sleep 1
done

echo "[$(date +'%F %T')] [Stop] ARK ne s'est pas arrêté proprement après 30s. Envoi du SIGKILL..."
kill -9 "$PID" 2>/dev/null || true

# Vérifier que le processus est bien terminé
sleep 1
if kill -0 "$PID" 2>/dev/null; then
    echo "[$(date +'%F %T')] [Stop] ERREUR: le processus $PID existe toujours après SIGKILL."
    exit 2
fi

# Vérifier les processus orphelins
ORPHANS=$(pgrep -f "/ShooterGame/Binaries/Linux/ShooterGameServer" || true)
if [ -n "$ORPHANS" ]; then
    echo "[$(date +'%F %T')] [Stop] AVERTISSEMENT: processus orphelins détectés (PID: $ORPHANS). Nettoyage..."
    # shellcheck disable=SC2086
    kill -9 $ORPHANS 2>/dev/null || true
fi

ELAPSED=$(($(date +%s) - START_TIME))
echo "[$(date +'%F %T')] [Stop] Processus ARK tué de force en ${ELAPSED}s."
output_json "warning" "forced" "$ELAPSED"
exit 1