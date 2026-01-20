#!/usr/bin/env bash
# /home/arkserver/arkserver/core/ark-backup.sh
# Script de backup modulaire pour ARK: Survival Evolved
# Types : fast | daily | boot | prestop
# Codes de sortie:
# 0 = backup réussi
# 1 = pas de backup (conditions non remplies)
# 2 = erreur critique

set -euo pipefail

ARK_DIR="/home/arkserver/arkserver"
SAVE_DIR="$ARK_DIR/ShooterGame/Saved"
BACKUP_DIR="$ARK_DIR/backups"
LOG_DIR="$ARK_DIR/logs"
BACKUP_LOG="$LOG_DIR/backup.log"

TIMESTAMP=$(date +"%Y%m%d-%H%M")
TYPE="$1"

mkdir -p "$LOG_DIR"
exec > >(tee -a "$BACKUP_LOG") 2>&1

echo "[$(date +'%F %T')] [Backup] Démarrage backup type=$TYPE"

# Fonction : génération sortie JSON
output_json() {
    local STATUS="$1"
    local BACKUP_TYPE="${2:-unknown}"
    local SIZE="${3:-0}"
    local COUNT="${4:-0}"
    printf '{"status":"%s","type":"%s","size":"%s","count":%d}\n' "$STATUS" "$BACKUP_TYPE" "$SIZE" "$COUNT"
}

# Vérification du paramètre
if [[ -z "$TYPE" ]]; then
    echo "[$(date +'%F %T')] [Backup] ERREUR: paramètre manquant."
    echo "[$(date +'%F %T')] [Backup] Usage: $0 {fast|daily|boot|prestop}"
    output_json "error" "none" "0" "0"
    exit 2
fi

# Validation du type avant traitement
case "$TYPE" in
    fast|daily|boot|prestop)
        ;;
    *)
        echo "[$(date +'%F %T')] [Backup] ERREUR: type invalide '$TYPE'."
        output_json "error" "$TYPE" "0" "0"
        exit 2
        ;;
esac

# Vérification du dossier Saved
if [[ ! -d "$SAVE_DIR" ]]; then
    echo "[$(date +'%F %T')] [Backup] ERREUR: dossier Saved introuvable: $SAVE_DIR"
    output_json "error" "$TYPE" "0" "0"
    exit 2
fi

# Sélection du dossier de destination
DEST="$BACKUP_DIR/$TYPE"
mkdir -p "$DEST"

# Vérification de l'espace disque (minimum 5GB requis)
AVAIL_KB=$(df -k "$DEST" | tail -n1 | awk '{print $4}')
AVAIL_GB=$((AVAIL_KB / 1024 / 1024))
if [[ $AVAIL_GB -lt 5 ]]; then
    echo "[$(date +'%F %T')] [Backup] ERREUR: espace disque insuffisant (${AVAIL_GB}GB disponible, 5GB minimum)."
    output_json "error" "$TYPE" "0" "0"
    exit 2
fi

echo "[$(date +'%F %T')] [Backup] Espace disque: ${AVAIL_GB}GB disponible."

# --------------------------------------------------------------------
#  Backup incrémental (fast)
# --------------------------------------------------------------------
if [[ "$TYPE" == "fast" ]]; then

    # Ne faire un backup fast que si le serveur tourne
    if ! systemctl is-active --quiet ark-core; then
        echo "[$(date +'%F %T')] [Backup] Serveur ARK arrêté → aucun backup fast."
        output_json "skipped" "fast" "0" "0"
        exit 1
    fi

    echo "[$(date +'%F %T')] [Backup] Exécution rsync incrémental..."
    
    # Si aucun backup précédent → backup complet
    if [[ ! -e "$DEST/latest" ]]; then
        if ! rsync -a "$SAVE_DIR/" "$DEST/$TIMESTAMP"; then
            echo "[$(date +'%F %T')] [Backup] ERREUR: échec rsync initial."
            output_json "error" "fast" "0" "0"
            exit 2
        fi
        echo "[$(date +'%F %T')] [Backup] Backup initial créé."
    else
        if ! rsync -a --delete --link-dest="$DEST/latest" "$SAVE_DIR/" "$DEST/$TIMESTAMP"; then
            echo "[$(date +'%F %T')] [Backup] ERREUR: échec rsync incrémental."
            output_json "error" "fast" "0" "0"
            exit 2
        fi
        echo "[$(date +'%F %T')] [Backup] Snapshot incrémental créé."
    fi

    rm -f "$DEST/latest"
    ln -s "$TIMESTAMP" "$DEST/latest"

    # Rotation: garder 200 snapshots
    cd "$DEST" || exit 2
    SNAPSHOTS=$(ls -1dt 20* 2>/dev/null | wc -l)
    if [[ $SNAPSHOTS -gt 200 ]]; then
        OLD_COUNT=$((SNAPSHOTS - 200))
        echo "[$(date +'%F %T')] [Backup] Rotation: suppression de $OLD_COUNT ancien(s) snapshot(s)."
        ls -1dt 20* | tail -n +201 | xargs -r rm -rf
    fi

    echo "[$(date +'%F %T')] [Backup] Backup fast terminé avec succès ($SNAPSHOTS snapshots total)."
    output_json "ok" "fast" "0" "$SNAPSHOTS"
    exit 0
fi

# --------------------------------------------------------------------
#  Backup complet (daily, boot, prestop)
# --------------------------------------------------------------------

# Ne faire un backup daily que si le serveur tourne
if [[ "$TYPE" == "daily" ]]; then
    if ! systemctl is-active --quiet ark-core; then
        echo "[$(date +'%F %T')] [Backup] Serveur ARK arrêté → aucun backup daily."
        output_json "skipped" "daily" "0" "0"
        exit 1
    fi
fi

ARCHIVE="$DEST/$TYPE-$TIMESTAMP.tar.gz"
echo "[$(date +'%F %T')] [Backup] Création archive: $ARCHIVE"

if ! tar -czf "$ARCHIVE" -C "$SAVE_DIR" .; then
    echo "[$(date +'%F %T')] [Backup] ERREUR: échec création archive tar."
    rm -f "$ARCHIVE" 2>/dev/null || true
    output_json "error" "$TYPE" "0" "0"
    exit 2
fi

ARCHIVE_SIZE=$(du -h "$ARCHIVE" | cut -f1)
echo "[$(date +'%F %T')] [Backup] Archive créée avec succès (taille: $ARCHIVE_SIZE)."

# Rotation selon le type
cd "$DEST" || exit 2
case "$TYPE" in
    daily)
        MAX_BACKUPS=30
        ;;
    boot|prestop)
        MAX_BACKUPS=10
        ;;
esac

BACKUP_COUNT=$(ls -1dt "$TYPE"-* 2>/dev/null | wc -l)
if [[ $BACKUP_COUNT -gt $MAX_BACKUPS ]]; then
    OLD_COUNT=$((BACKUP_COUNT - MAX_BACKUPS))
    echo "[$(date +'%F %T')] [Backup] Rotation: suppression de $OLD_COUNT ancienne(s) archive(s)."
    ls -1dt "$TYPE"-* | tail -n +$((MAX_BACKUPS + 1)) | xargs -r rm -f
fi

echo "[$(date +'%F %T')] [Backup] Backup $TYPE terminé avec succès ($BACKUP_COUNT archives total)."
output_json "ok" "$TYPE" "$ARCHIVE_SIZE" "$BACKUP_COUNT"
exit 0