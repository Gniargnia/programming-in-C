#!/usr/bin/env bash
# /home/arkserver/arkserver/core/ark-mods.sh
# Gestion complète des mods ARK: installation, update, validation, nettoyage
# Codes de sortie:
# 0 = succès (tous les mods OK)
# 1 = avertissement (certains mods en erreur mais non-bloquant)
# 2 = erreur critique (configuration invalide, SteamCMD absent)

set -euo pipefail

ARK_DIR="/home/arkserver/arkserver"
CONFIG_DIR="$ARK_DIR/config"
MOD_FILE="$CONFIG_DIR/mods.list"
LOG_DIR="$ARK_DIR/logs"
MODS_LOG="$LOG_DIR/mods.log"

# Chemins Steam
WORKSHOP_DIR="/home/arkserver/Steam/steamapps/workshop/content/346110"
STEAMCMD="/home/arkserver/steamcmd/steamcmd.sh"
STEAMCMD_TIMEOUT="timeout 300s"

mkdir -p "$LOG_DIR" "$CONFIG_DIR"
exec > >(tee -a "$MODS_LOG") 2>&1

echo "[$(date +'%F %T')] [Mods] Démarrage script mods (mode=${1:-none})"

# Variables de statut
ERROR_COUNT=0
WARNING_COUNT=0
INSTALLED_COUNT=0
UPDATED_COUNT=0
CLEANED_COUNT=0

# --------------------------------------------------------------------
#  Validations préliminaires
# --------------------------------------------------------------------

# Vérifier SteamCMD
if [[ ! -x "$STEAMCMD" ]]; then
    echo "[$(date +'%F %T')] [Mods] ERREUR: SteamCMD introuvable: $STEAMCMD"
    exit 2
fi

# Vérifier workshop directory
if [[ ! -d "$WORKSHOP_DIR" ]]; then
    echo "[$(date +'%F %T')] [Mods] AVERTISSEMENT: dossier workshop absent, création: $WORKSHOP_DIR"
    mkdir -p "$WORKSHOP_DIR"
fi

# Vérifier fichier mods.list
if [[ ! -f "$MOD_FILE" ]]; then
    echo "[$(date +'%F %T')] [Mods] ERREUR: fichier mods.list introuvable: $MOD_FILE"
    exit 2
fi

# Valider format mods.list
if ! grep -qE '^[0-9]+\|' "$MOD_FILE" 2>/dev/null; then
    echo "[$(date +'%F %T')] [Mods] AVERTISSEMENT: mods.list vide ou format invalide (attendu: MOD_ID|MOD_NAME)."
fi

# --------------------------------------------------------------------
#  Fonction : installation automatique d'un mod manquant
# --------------------------------------------------------------------
install_mod() {
    local MOD_ID="$1"
    local MOD_NAME="$2"
    local MOD_PATH="$WORKSHOP_DIR/$MOD_ID"

    echo "[$(date +'%F %T')] [Mods] Installation mod: $MOD_NAME ($MOD_ID)"

    if ! $STEAMCMD_TIMEOUT "$STEAMCMD" +login anonymous +workshop_download_item 346110 "$MOD_ID" validate +quit >> "$MODS_LOG" 2>&1; then
        echo "[$(date +'%F %T')] [Mods] ERREUR: échec SteamCMD pour mod $MOD_ID"
        ((ERROR_COUNT++))
        return 1
    fi

    # Vérification après installation
    if [[ ! -d "$MOD_PATH" ]]; then
        echo "[$(date +'%F %T')] [Mods] ERREUR: dossier mod absent après installation: $MOD_NAME ($MOD_ID)"
        ((ERROR_COUNT++))
        return 1
    fi

    # Vérifier mod.info
    if [[ ! -f "$MOD_PATH/mod.info" ]] || [[ ! -s "$MOD_PATH/mod.info" ]]; then
        echo "[$(date +'%F %T')] [Mods] AVERTISSEMENT: mod.info invalide pour $MOD_NAME ($MOD_ID)"
        ((WARNING_COUNT++))
    fi

    echo "[$(date +'%F %T')] [Mods] Mod installé avec succès: $MOD_NAME ($MOD_ID)"
    ((INSTALLED_COUNT++))
    return 0
}

# --------------------------------------------------------------------
#  Fonction : validation des mods
# --------------------------------------------------------------------
validate_mods() {
    echo "[$(date +'%F %T')] [Mods] Validation des mods listés..."
    
    # Détecter les doublons
    local DUPLICATES=$(grep -E '^[0-9]+\|' "$MOD_FILE" | cut -d'|' -f1 | sort | uniq -d)
    if [[ -n "$DUPLICATES" ]]; then
        echo "[$(date +'%F %T')] [Mods] AVERTISSEMENT: mods dupliqués détectés:"
        echo "$DUPLICATES" | while read -r DUP_ID; do
            echo "[$(date +'%F %T')] [Mods]   - Mod ID: $DUP_ID"
            ((WARNING_COUNT++))
        done
    fi

    while IFS="|" read -r MOD_ID MOD_NAME; do
        # Ignorer lignes vides ou commentaires
        [[ -z "$MOD_ID" ]] && continue
        [[ "$MOD_ID" =~ ^# ]] && continue
        
        # Valider format MOD_ID (que des chiffres)
        if ! [[ "$MOD_ID" =~ ^[0-9]+$ ]]; then
            echo "[$(date +'%F %T')] [Mods] ERREUR: MOD_ID invalide: '$MOD_ID'"
            ((ERROR_COUNT++))
            continue
        fi

        MOD_PATH="$WORKSHOP_DIR/$MOD_ID"

        # Si le mod n'existe pas → installation automatique
        if [[ ! -d "$MOD_PATH" ]]; then
            install_mod "$MOD_ID" "$MOD_NAME" || continue
        else
            # Vérification fichier mod.info
            if [[ ! -f "$MOD_PATH/mod.info" ]]; then
                echo "[$(date +'%F %T')] [Mods] ERREUR: mod.info manquant: $MOD_NAME ($MOD_ID)"
                ((ERROR_COUNT++))
                continue
            fi

            # Vérification taille > 0
            if [[ ! -s "$MOD_PATH/mod.info" ]]; then
                echo "[$(date +'%F %T')] [Mods] ERREUR: mod.info vide: $MOD_NAME ($MOD_ID)"
                ((ERROR_COUNT++))
                continue
            fi

            echo "[$(date +'%F %T')] [Mods] Mod valide: $MOD_NAME ($MOD_ID)"
        fi

    done < "$MOD_FILE"

    echo "[$(date +'%F %T')] [Mods] Validation terminée."
    return 0
}

# --------------------------------------------------------------------
#  Fonction : update des mods via SteamCMD
# --------------------------------------------------------------------
update_mods() {
    echo "[$(date +'%F %T')] [Mods] Mise à jour des mods..."
    
    while IFS="|" read -r MOD_ID MOD_NAME; do
        [[ -z "$MOD_ID" ]] && continue
        [[ "$MOD_ID" =~ ^# ]] && continue
        [[ ! "$MOD_ID" =~ ^[0-9]+$ ]] && continue

        echo "[$(date +'%F %T')] [Mods] Mise à jour: $MOD_NAME ($MOD_ID)"

        if ! $STEAMCMD_TIMEOUT "$STEAMCMD" +login anonymous +workshop_download_item 346110 "$MOD_ID" validate +quit >> "$MODS_LOG" 2>&1; then
            echo "[$(date +'%F %T')] [Mods] ERREUR: échec mise à jour: $MOD_NAME ($MOD_ID)"
            ((ERROR_COUNT++))
            continue
        fi

        echo "[$(date +'%F %T')] [Mods] Mod mis à jour: $MOD_NAME ($MOD_ID)"
        ((UPDATED_COUNT++))

    done < "$MOD_FILE"

    echo "[$(date +'%F %T')] [Mods] Mise à jour terminée ($UPDATED_COUNT mods mis à jour)."
    return 0
}

# --------------------------------------------------------------------
#  Fonction : nettoyage des mods non listés
# --------------------------------------------------------------------
clean_orphaned_mods() {
    echo "[$(date +'%F %T')] [Mods] Recherche de mods orphelins..."
    
    if [[ ! -d "$WORKSHOP_DIR" ]]; then
        echo "[$(date +'%F %T')] [Mods] Aucun dossier workshop à nettoyer."
        return 0
    fi

    # Récupérer les IDs listés
    local LISTED_MODS=$(grep -E '^[0-9]+\|' "$MOD_FILE" | cut -d'|' -f1 | sort -u)
    
    # Parcourir les mods installés
    for MOD_DIR in "$WORKSHOP_DIR"/*; do
        [[ ! -d "$MOD_DIR" ]] && continue
        
        local MOD_ID=$(basename "$MOD_DIR")
        [[ ! "$MOD_ID" =~ ^[0-9]+$ ]] && continue
        
        # Vérifier si listé
        if ! echo "$LISTED_MODS" | grep -qx "$MOD_ID"; then
            echo "[$(date +'%F %T')] [Mods] Suppression mod orphelin: $MOD_ID"
            rm -rf "$MOD_DIR"
            ((CLEANED_COUNT++))
        fi
    done
    
    if [[ $CLEANED_COUNT -gt 0 ]]; then
        echo "[$(date +'%F %T')] [Mods] $CLEANED_COUNT mod(s) orphelin(s) supprimé(s)."
    else
        echo "[$(date +'%F %T')] [Mods] Aucun mod orphelin détecté."
    fi
    
    return 0
}

# --------------------------------------------------------------------
#  Fonction : génération sortie JSON
# --------------------------------------------------------------------
output_json() {
    local STATUS="$1"
    printf '{"status":"%s","errors":%d,"warnings":%d,"installed":%d,"updated":%d,"cleaned":%d}\n' \
        "$STATUS" "$ERROR_COUNT" "$WARNING_COUNT" "$INSTALLED_COUNT" "$UPDATED_COUNT" "$CLEANED_COUNT"
}

# --------------------------------------------------------------------
#  Mode : --check
# --------------------------------------------------------------------
if [[ "${1:-}" == "--check" ]]; then
    validate_mods
    
    if [[ $ERROR_COUNT -gt 0 ]]; then
        echo "[$(date +'%F %T')] [Mods] Validation terminée avec $ERROR_COUNT erreur(s), $WARNING_COUNT avertissement(s)."
        output_json "error"
        exit 1
    elif [[ $WARNING_COUNT -gt 0 ]]; then
        echo "[$(date +'%F %T')] [Mods] Validation terminée avec $WARNING_COUNT avertissement(s)."
        output_json "warning"
        exit 0
    else
        echo "[$(date +'%F %T')] [Mods] Validation réussie."
        output_json "ok"
        exit 0
    fi
fi

# --------------------------------------------------------------------
#  Mode : --update
# --------------------------------------------------------------------
if [[ "${1:-}" == "--update" ]]; then
    update_mods
    
    if [[ $ERROR_COUNT -gt 0 ]]; then
        echo "[$(date +'%F %T')] [Mods] Mise à jour terminée avec $ERROR_COUNT erreur(s)."
        output_json "error"
        exit 1
    else
        echo "[$(date +'%F %T')] [Mods] Mise à jour réussie ($UPDATED_COUNT mod(s))."
        output_json "ok"
        exit 0
    fi
fi

# --------------------------------------------------------------------
#  Mode : --full (update + validation + nettoyage)
# --------------------------------------------------------------------
if [[ "${1:-}" == "--full" ]]; then
    update_mods
    validate_mods
    clean_orphaned_mods
    
    if [[ $ERROR_COUNT -gt 0 ]]; then
        echo "[$(date +'%F %T')] [Mods] Opération terminée avec $ERROR_COUNT erreur(s), $WARNING_COUNT avertissement(s)."
        output_json "error"
        exit 1
    elif [[ $WARNING_COUNT -gt 0 ]]; then
        echo "[$(date +'%F %T')] [Mods] Opération terminée avec $WARNING_COUNT avertissement(s)."
        output_json "warning"
        exit 0
    else
        echo "[$(date +'%F %T')] [Mods] Opération réussie."
        output_json "ok"
        exit 0
    fi
fi

# --------------------------------------------------------------------
#  Mode : --clean (nettoyage seul)
# --------------------------------------------------------------------
if [[ "${1:-}" == "--clean" ]]; then
    clean_orphaned_mods
    
    echo "[$(date +'%F %T')] [Mods] Nettoyage terminé ($CLEANED_COUNT mod(s) supprimé(s))."
    output_json "ok"
    exit 0
fi

# --------------------------------------------------------------------
#  Usage
# --------------------------------------------------------------------
echo "[$(date +'%F %T')] [Mods] ERREUR: mode invalide ou manquant."
echo "Usage: $0 {--check|--update|--full|--clean}"
exit 2
