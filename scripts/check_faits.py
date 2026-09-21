#!/usr/bin/env python3
"""Contrôle des faits : chaque chiffre de l'article existe-t-il dans brain/ ?

    python3 scripts/check_faits.py articles/mon-article.md

C'est le garde-fou anti-invention. La règle 4 de CLAUDE.md dit « zéro
invention » : ce script la rend vérifiable au lieu de l'espérer.

Un chiffre qui ne vient pas de brain/ doit porter sa source dans la phrase,
sous la forme (source : ...). Sinon il est bloquant.
Code de sortie 1 s'il reste un point bloquant.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _article import Article, Constat, afficher, lire_brain  # noqa: E402

# Un chiffre = un pourcentage, un montant, une durée, ou tout nombre >= 10.
MOTIF = re.compile(
    r"(?<![\w/\-.])"
    r"(\d{1,3}(?:[   .]\d{3})+|\d+(?:[.,]\d+)?)"
    r"\s?(%|€|\$|euros?|k€|M€|millions?|milliards?|heures?|h\b|minutes?|min\b|jours?|semaines?|mois|ans?)?",
    re.I,
)

# Ce qui n'est pas une affirmation chiffrée : numérotation, ancres, versions.
LIGNE_IGNOREE = re.compile(r"^\s*(\d+[.)]\s|#{1,6}\s*\d|\||```)")


def _variantes(valeur):
    """« 1 850 000 » doit reconnaître « 1850000 », « 1.850.000 », « 1 850 000 »."""
    nu = re.sub(r"[   .,]", "", valeur)
    formes = {valeur, nu}
    if len(nu) > 3 and nu.isdigit():
        groupes = []
        reste = nu
        while len(reste) > 3:
            groupes.insert(0, reste[-3:])
            reste = reste[:-3]
        groupes.insert(0, reste)
        for sep in (" ", " ", " ", ".", ","):
            formes.add(sep.join(groupes))
    return formes


def run(chemin):
    a = Article(chemin)
    brain = lire_brain()
    reference = "\n".join(brain.values())
    reference_nu = re.sub(r"[   .,]", "", reference)
    c = []
    vus = set()

    dans_code = False
    for i, ligne in enumerate(a.lignes):
        if ligne.strip().startswith("```"):
            dans_code = not dans_code
            continue
        if dans_code or LIGNE_IGNOREE.match(ligne):
            continue
        ligne_sans_liens = re.sub(r"\([^)]*://[^)]*\)", "", ligne)
        porte_source = "source :" in ligne.lower() or "source:" in ligne.lower()

        for m in MOTIF.finditer(ligne_sans_liens):
            valeur, unite = m.group(1), (m.group(2) or "").strip()
            nu = re.sub(r"[   .,]", "", valeur)
            if not nu.isdigit():
                continue
            if not unite and int(nu) < 10:
                continue
            affiche = (valeur + (" " + unite if unite else "")).strip()
            if affiche in vus:
                continue
            vus.add(affiche)

            trouve = any(f in reference for f in _variantes(valeur)) or nu in reference_nu
            if trouve:
                continue
            niveau = Constat.ALERTE if porte_source else Constat.BLOQUANT
            detail = "source citée dans la phrase, à vérifier" if porte_source \
                else "absent de brain/ : inventé, ou à ajouter à votre contexte"
            c.append(Constat(niveau, "Fait", "« %s » %s" % (affiche, detail),
                             i + a.decalage + 1))

    if not vus:
        c.append(Constat(Constat.ALERTE, "Preuve",
                         "aucun chiffre dans l'article : la règle 6 demande une preuve par affirmation"))
    return c


def note(constats):
    penalite = sum(20 if x.niveau == Constat.BLOQUANT else 5 for x in constats)
    return max(0, 100 - penalite)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    if not os.path.isfile(sys.argv[1]):
        print("Fichier introuvable : %s" % sys.argv[1])
        sys.exit(2)
    constats = run(sys.argv[1])
    afficher("Contrôle des faits — zéro chiffre inventé", constats, note(constats))
    sys.exit(1 if any(x.niveau == Constat.BLOQUANT for x in constats) else 0)
