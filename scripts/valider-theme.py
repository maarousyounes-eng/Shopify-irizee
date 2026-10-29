#!/usr/bin/env python3
"""
Validations du thème que `shopify theme check` ne fait pas.

Chacune de ces règles correspond à une erreur réellement rencontrée sur le
projet. Shopify rejette silencieusement un fichier dont le schéma est
invalide : aucun message, le fichier n'arrive simplement jamais sur la
boutique. C'est ce qui a fait tomber la page d'accueil en 404 le 15/10/2026.

Sortie : 0 si tout passe, 1 sinon.
"""

import json
import os
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
erreurs = []
controles = 0


def sans_entete(texte):
    """Les fichiers JSON de Shopify commencent par un commentaire /* ... */."""
    return re.sub(r"^\s*/\*.*?\*/\s*", "", texte, flags=re.S)


def charger_json(chemin):
    return json.loads(sans_entete(chemin.read_text(encoding="utf-8")))


def schema_de(chemin):
    """Extrait le bloc {% schema %} d'une section ou d'un block."""
    texte = chemin.read_text(encoding="utf-8")
    m = re.search(r"{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}", texte, re.S)
    return (json.loads(m.group(1)), texte) if m else (None, texte)


def parcourir(obj):
    """Tous les dictionnaires de réglage d'une structure imbriquée."""
    if isinstance(obj, dict):
        if "type" in obj:
            yield obj
        for v in obj.values():
            yield from parcourir(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from parcourir(v)


# ---------------------------------------------------------------- 1. JSON valide
def controle_json_valide():
    global controles
    for chemin in sorted(RACINE.glob("**/*.json")):
        if any(p in chemin.parts for p in ("node_modules", ".git", "docs", "scripts")):
            continue
        controles += 1
        try:
            charger_json(chemin)
        except Exception as e:
            erreurs.append(f"{chemin.relative_to(RACINE)} : JSON invalide — {e}")


# -------------------------------------------------------------- 2. Schémas valides
def fichiers_a_schema():
    for dossier in ("sections", "blocks", "snippets"):
        yield from sorted((RACINE / dossier).glob("*.liquid")) if (RACINE / dossier).is_dir() else []


def controle_schemas():
    global controles
    for chemin in fichiers_a_schema():
        texte = chemin.read_text(encoding="utf-8")
        if "schema" not in texte:
            continue
        controles += 1
        try:
            schema_de(chemin)
        except Exception as e:
            erreurs.append(f"{chemin.relative_to(RACINE)} : schéma invalide — {e}")


# ------------------------------------------- 3. Les range : 101 crans au maximum
def controle_range():
    """
    Shopify impose (max - min) / step <= 101. Au-delà, il rejette le schéma ET
    le fichier entier, sans aucun message. theme check ne détecte pas cette
    règle. C'est la panne du 15/10/2026 : un button_radius en 0–999 pas de 1.
    """
    global controles
    sources = list(fichiers_a_schema()) + [RACINE / "config" / "settings_schema.json"]
    for chemin in sources:
        if not chemin.exists():
            continue
        try:
            if chemin.suffix == ".liquid":
                schema, _ = schema_de(chemin)
                if schema is None:
                    continue
            else:
                schema = charger_json(chemin)
        except Exception:
            continue  # déjà signalé par les contrôles précédents
        for reglage in parcourir(schema):
            if reglage.get("type") != "range":
                continue
            controles += 1
            try:
                crans = (reglage["max"] - reglage["min"]) / reglage["step"]
            except (KeyError, ZeroDivisionError, TypeError):
                erreurs.append(
                    f"{chemin.relative_to(RACINE)} : range « {reglage.get('id')} » "
                    f"incomplet (min, max et step sont obligatoires)"
                )
                continue
            if crans > 101:
                erreurs.append(
                    f"{chemin.relative_to(RACINE)} : range « {reglage['id']} » déclare "
                    f"{crans:.0f} crans ({reglage['min']}–{reglage['max']}, pas de "
                    f"{reglage['step']}). Shopify en autorise 101 au maximum et "
                    f"rejettera le fichier entier."
                )


# ------------------------- 3 bis. Longueur des noms de section et de bloc
def controle_longueur_noms():
    """
    Shopify limite à 25 caractères le `name` d'une section, d'un bloc ou d'un
    préréglage, et rejette le fichier entier au-delà. Rencontré le 19/10/2026 :
    « Jauge de livraison offerte », 26 caractères, a suffi à faire disparaître
    toute la section et à rendre la fiche produit vide.
    """
    global controles
    MAX = 25
    for chemin in fichiers_a_schema():
        try:
            schema, _ = schema_de(chemin)
        except Exception:
            continue
        if schema is None:
            continue
        a_verifier = [("section", schema.get("name"))]
        a_verifier += [("bloc", b.get("name")) for b in schema.get("blocks") or []]
        a_verifier += [("préréglage", p.get("name")) for p in schema.get("presets") or []]
        for genre, nom in a_verifier:
            # Un nom préfixé « t: » est une clé de traduction, résolue par
            # Shopify depuis les fichiers de locale : la limite porte sur le
            # texte résolu, pas sur la clé.
            if not nom or nom.startswith("t:"):
                continue
            controles += 1
            if len(nom) > MAX:
                erreurs.append(
                    f"{chemin.relative_to(RACINE)} : nom de {genre} « {nom} » fait "
                    f"{len(nom)} caractères. Shopify en autorise {MAX} et rejettera "
                    f"le fichier entier."
                )


# ------------------------- 3 ter. Valeurs par défaut vides
def controle_default_vide():
    """
    Un `default` à la chaîne vide rend le schéma invalide et Shopify refuse le
    fichier entier : « setting with id=... default ne peut pas être vide ».
    Rencontré le 29/10/2026 sur iz-catalogue.liquid, qui ne montait plus sur la
    boutique sans que rien ne le dise. Un réglage sans `default` est valide :
    c'est la bonne façon d'avoir un champ vide au départ.
    """
    global controles
    sources = list(fichiers_a_schema()) + [RACINE / "config" / "settings_schema.json"]
    for chemin in sources:
        if not chemin.exists():
            continue
        try:
            if chemin.suffix == ".liquid":
                schema, _ = schema_de(chemin)
                if schema is None:
                    continue
            else:
                schema = charger_json(chemin)
        except Exception:
            continue
        for reglage in parcourir(schema):
            if "default" not in reglage:
                continue
            controles += 1
            if reglage["default"] == "":
                erreurs.append(
                    f"{chemin.relative_to(RACINE)} : le réglage "
                    f"« {reglage.get('id')} » a un default vide. Shopify "
                    f"rejettera le fichier entier : retirer la ligne default."
                )



# ------------------------------- 4. Réglages utilisés mais absents du schéma
def controle_reglages_declares():
    global controles
    for chemin in fichiers_a_schema():
        try:
            schema, texte = schema_de(chemin)
        except Exception:
            continue
        if schema is None:
            continue
        declares = {r["id"] for r in parcourir(schema) if r.get("id") and r.get("type") != "header"}
        utilises = set(re.findall(r"section\.settings\.(\w+)", texte))
        manquants = sorted(utilises - declares)
        controles += 1
        for m in manquants:
            erreurs.append(
                f"{chemin.relative_to(RACINE)} : « section.settings.{m} » est utilisé "
                f"dans le code mais absent du schéma — il rendra une valeur vide."
            )


# ------------------- 5. Valeurs des templates conformes aux schémas de section
def controle_valeurs_templates():
    global controles
    schemas = {}
    for chemin in (RACINE / "sections").glob("*.liquid"):
        try:
            schema, _ = schema_de(chemin)
        except Exception:
            continue
        if schema:
            schemas[chemin.stem] = schema

    for chemin in sorted((RACINE / "templates").glob("*.json")):
        try:
            data = charger_json(chemin)
        except Exception:
            continue
        for sid, section in (data.get("sections") or {}).items():
            schema = schemas.get(section.get("type"))
            if not schema:
                continue
            defs = {r["id"]: r for r in (schema.get("settings") or []) if r.get("id")}
            for cle, valeur in (section.get("settings") or {}).items():
                d = defs.get(cle)
                if d is None:
                    continue  # réglage retiré du schéma : Shopify l'ignore sans casser
                controles += 1
                if d.get("type") == "range" and isinstance(valeur, (int, float)):
                    if not (d["min"] <= valeur <= d["max"]):
                        erreurs.append(
                            f"{chemin.relative_to(RACINE)} : {sid}.{cle} = {valeur}, "
                            f"hors des bornes du schéma ({d['min']}–{d['max']})."
                        )
                elif d.get("type") == "select":
                    options = [str(o.get("value")) for o in (d.get("options") or [])]
                    if options and str(valeur) not in options:
                        erreurs.append(
                            f"{chemin.relative_to(RACINE)} : {sid}.{cle} = {valeur!r}, "
                            f"absent des options déclarées ({', '.join(options)})."
                        )


# --------------------------- 6. Identifiants dupliqués dans une même portée
def controle_doublons():
    global controles
    for chemin in fichiers_a_schema():
        try:
            schema, _ = schema_de(chemin)
        except Exception:
            continue
        if schema is None:
            continue
        portees = {"section": schema.get("settings") or []}
        for bloc in schema.get("blocks") or []:
            portees[f"bloc « {bloc.get('type')} »"] = bloc.get("settings") or []
        for nom, reglages in portees.items():
            controles += 1
            vus = {}
            for r in reglages:
                if not r.get("id"):
                    continue
                vus[r["id"]] = vus.get(r["id"], 0) + 1
            for ident, n in vus.items():
                if n > 1:
                    erreurs.append(
                        f"{chemin.relative_to(RACINE)} : « {ident} » est déclaré "
                        f"{n} fois dans la portée {nom}."
                    )


def main():
    for controle in (
        controle_json_valide,
        controle_schemas,
        controle_range,
        controle_longueur_noms,
        controle_default_vide,
        controle_reglages_declares,
        controle_valeurs_templates,
        controle_doublons,
    ):
        controle()

    print(f"{controles} contrôles exécutés sur le thème.\n")
    if erreurs:
        print(f"{len(erreurs)} problème(s) :\n")
        for e in erreurs:
            print(f"  ✗ {e}")
        print("\nShopify rejette un fichier au schéma invalide sans aucun message :")
        print("le fichier n'arrive jamais sur la boutique. Corriger avant de fusionner.")
        return 1
    print("✓ aucun problème détecté.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
