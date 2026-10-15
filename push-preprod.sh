#!/usr/bin/env bash
#
# Envoie le CODE du thème sur la préprod, sans jamais toucher aux fichiers
# que l'éditeur Shopify écrit.
#
# Pourquoi : le customizer enregistre ses réglages dans templates/*.json,
# config/settings_data.json et sections/*-group.json, sur la boutique. Un
# `shopify theme push` nu renvoie les copies locales de ces fichiers et
# écrase donc tout ce qui a été réglé dans l'éditeur depuis le dernier pull.
#
# Usage :
#   ./push-preprod.sh                      # tout le code
#   ./push-preprod.sh sections/footer.liquid   # un fichier précis

set -euo pipefail

STORE="0nz0p1-61.myshopify.com"
THEME="198076137856"   # Preprod de irizee — jamais le thème live

cd "$(dirname "$0")/theme"

if [ $# -gt 0 ]; then
  ONLY=()
  for f in "$@"; do ONLY+=(--only "$f"); done
  shopify theme push --store="$STORE" --theme="$THEME" "${ONLY[@]}"
else
  shopify theme push --store="$STORE" --theme="$THEME" \
    --ignore "templates/*.json" \
    --ignore "config/settings_data.json" \
    --ignore "sections/*-group.json"
fi
