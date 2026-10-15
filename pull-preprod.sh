#!/usr/bin/env bash
#
# Récupère dans le dépôt les réglages faits dans l'éditeur Shopify.
#
# À lancer AVANT toute session de dev, et après chaque passage dans le
# customizer : c'est ce qui met les réglages sous git et évite de les
# perdre. Ne touche qu'aux fichiers JSON, jamais au code.

set -euo pipefail

STORE="0nz0p1-61.myshopify.com"
THEME="198076137856"   # Preprod de irizee

cd "$(dirname "$0")/theme"

shopify theme pull --store="$STORE" --theme="$THEME" \
  --only "templates/*.json" \
  --only "config/settings_data.json" \
  --only "sections/*-group.json"

cd ..
echo
echo "Réglages récupérés. Ce qui a changé depuis le dernier commit :"
git status --short -- theme/templates theme/config theme/sections || true
