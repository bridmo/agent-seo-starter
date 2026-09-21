#!/usr/bin/env python3
"""Contrôle SEO : l'article respecte-t-il les règles de brain/regles-seo.md ?

    python3 scripts/check_seo.py articles/mon-article.md

Code de sortie 1 s'il reste un point bloquant.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _article import Article, Constat, afficher, normalise, phrases  # noqa: E402

AMORCES_MOLLES = ["de nos jours", "a l'heure actuelle", "dans un monde", "aujourd'hui plus que jamais"]


def run(chemin):
    a = Article(chemin)
    c = []
    mc = normalise(a.mot_cle)

    # R1 — un article, un mot-clé, présent partout où il compte
    if not mc:
        c.append(Constat(Constat.BLOQUANT, "R1", "aucun mot-clé déclaré (en-tête « mot_cle: »)"))
    else:
        cibles = {
            "du titre": a.titre,
            "du H1": a.h1[0] if a.h1 else "",
            "de la meta description": a.meta,
            "du slug": a.slug.replace("-", " "),
        }
        prem = phrases(a.texte_prose)
        cibles["de la première phrase"] = prem[0] if prem else ""
        for ou, valeur in cibles.items():
            if mc not in normalise(valeur):
                c.append(Constat(Constat.BLOQUANT, "R1", "mot-clé « %s » absent %s" % (a.mot_cle, ou)))

    # R3 — un seul H1, des H2 qui découpent
    if len(a.h1) == 0:
        c.append(Constat(Constat.BLOQUANT, "R3", "aucun H1"))
    elif len(a.h1) > 1:
        c.append(Constat(Constat.BLOQUANT, "R3", "%d H1 au lieu d'un seul" % len(a.h1),
                         a.numero_ligne("# " + a.h1[1])))
    if len(a.h2) < 3:
        c.append(Constat(Constat.ALERTE, "R3", "seulement %d H2 : le plan est trop plat" % len(a.h2)))

    # R3 — paragraphes courts
    for ligne, texte in a.paragraphes:
        n = len(phrases(texte))
        if n > 4:
            c.append(Constat(Constat.ALERTE, "R3", "paragraphe de %d phrases (4 maximum)" % n, ligne))

    # R4 — l'intro entre dans le sujet
    p = a.paragraphes
    if p:
        ligne, intro = p[0]
        if len(phrases(intro)) > 3:
            c.append(Constat(Constat.ALERTE, "R4", "intro de %d phrases (3 maximum)" % len(phrases(intro)), ligne))
        for amorce in AMORCES_MOLLES:
            if normalise(intro).startswith(amorce):
                c.append(Constat(Constat.BLOQUANT, "R4", "l'intro démarre par une amorce creuse", ligne))
                break

    # R2 — longueur
    if a.nb_mots < 600:
        c.append(Constat(Constat.ALERTE, "R2", "%d mots : court face à des guides de page 1" % a.nb_mots))

    # R7 — la FAQ
    titres = [normalise(t) for t in a.h2]
    if not any("faq" in t or "questions" in t for t in titres):
        c.append(Constat(Constat.BLOQUANT, "R7", "pas de FAQ en fin d'article"))
    else:
        depart = a.corps.lower().find("faq")
        questions = len(re.findall(r"^###\s+.+\?", a.corps[depart:], re.M)) or \
            len(re.findall(r"^\*\*.+\?\*\*", a.corps[depart:], re.M))
        if questions and not 3 <= questions <= 5:
            c.append(Constat(Constat.ALERTE, "R7", "%d questions dans la FAQ (viser 3 à 5)" % questions))

    # R8 / R9 — les méta
    if a.titre and len(a.titre) > 60:
        c.append(Constat(Constat.BLOQUANT, "R8", "titre de %d caractères (60 maximum)" % len(a.titre)))
    if not a.meta:
        c.append(Constat(Constat.BLOQUANT, "R9", "aucune meta description (en-tête « meta: »)"))
    elif len(a.meta) > 155:
        c.append(Constat(Constat.BLOQUANT, "R9", "meta de %d caractères (155 maximum)" % len(a.meta)))

    # R10 — le maillage
    internes = [l for l in a.liens if not l.startswith(("http://", "https://", "mailto:"))
                or "://" not in l]
    if not 2 <= len(internes) <= 4:
        c.append(Constat(Constat.ALERTE, "R10", "%d lien(s) interne(s) : viser 2 à 4" % len(internes)))

    return c


def note(constats):
    penalite = sum(12 if x.niveau == Constat.BLOQUANT else 4 for x in constats)
    return max(0, 100 - penalite)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    if not os.path.isfile(sys.argv[1]):
        print("Fichier introuvable : %s" % sys.argv[1])
        sys.exit(2)
    constats = run(sys.argv[1])
    afficher("Contrôle SEO — structure et méta", constats, note(constats))
    sys.exit(1 if any(x.niveau == Constat.BLOQUANT for x in constats) else 0)
