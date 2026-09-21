#!/usr/bin/env python3
"""L'éval : la note de l'article, et le verdict avant publication.

    python3 scripts/eval_article.py articles/mon-article.md
    python3 scripts/eval_article.py articles/            # tout le dossier
    python3 scripts/eval_article.py articles/mon-article.md --json

Agrège les trois contrôles selon la grille de evals/grille-publication.md.
Code de sortie 1 si l'article ne passe pas la barre.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_faits  # noqa: E402
import check_seo  # noqa: E402
import check_voix  # noqa: E402
from _article import Constat, afficher  # noqa: E402

# Ce qui compte, et combien. Changez les poids : c'est votre grille, pas la nôtre.
CONTROLES = [
    ("SEO", check_seo, 40, "Contrôle SEO — structure et méta"),
    ("Voix", check_voix, 30, "Contrôle de voix — vos mots, pas ceux de l'IA"),
    ("Faits", check_faits, 30, "Contrôle des faits — zéro chiffre inventé"),
]

SEUIL = 80  # en dessous, on ne publie pas


def evaluer(chemin, silencieux=False):
    total, detail, bloquants = 0, {}, []
    for nom, module, poids, titre in CONTROLES:
        constats = module.run(chemin)
        note = module.note(constats)
        total += note * poids / 100.0
        detail[nom] = {"note": note, "poids": poids,
                       "constats": [x.dict() for x in constats]}
        bloquants += [x for x in constats if x.niveau == Constat.BLOQUANT]
        if not silencieux:
            afficher(titre, constats, note)
    return round(total), detail, bloquants


def verdict(note, bloquants):
    if bloquants:
        return "NE PAS PUBLIER", "%d point(s) bloquant(s) à corriger" % len(bloquants)
    if note < SEUIL:
        return "NE PAS PUBLIER", "%d/100, sous la barre de %d" % (note, SEUIL)
    return "PUBLIABLE", "%d/100, relecture humaine avant mise en ligne" % note


def _articles(cible):
    if os.path.isdir(cible):
        return sorted(os.path.join(cible, n) for n in os.listdir(cible) if n.endswith(".md"))
    return [cible]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    en_json = "--json" in sys.argv
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)

    if not os.path.exists(args[0]):
        print("Fichier introuvable : %s" % args[0])
        print("Attendu : un article .md, ou un dossier (par exemple articles/).")
        sys.exit(2)

    chemins = _articles(args[0])
    if not chemins:
        print("Aucun article à évaluer dans %s" % args[0])
        sys.exit(2)

    echec = False
    resultats = []
    for chemin in chemins:
        if not en_json:
            print("\n" + "=" * 62)
            print("ÉVAL · %s" % os.path.basename(chemin))
            print("=" * 62)
        note, detail, bloquants = evaluer(chemin, silencieux=en_json)
        etat, raison = verdict(note, bloquants)
        echec = echec or etat != "PUBLIABLE"
        resultats.append({"article": chemin, "note": note, "verdict": etat,
                          "raison": raison, "detail": detail})
        if not en_json:
            print("\n" + "-" * 62)
            print("VERDICT : %s — %s" % (etat, raison))
            print("-" * 62)

    if en_json:
        print(json.dumps(resultats if len(resultats) > 1 else resultats[0],
                         ensure_ascii=False, indent=2))
    sys.exit(1 if echec else 0)
