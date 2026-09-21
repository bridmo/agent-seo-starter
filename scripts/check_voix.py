#!/usr/bin/env python3
"""Contrôle de voix : l'article sonne-t-il comme vous, ou comme une IA ?

    python3 scripts/check_voix.py articles/mon-article.md

Trois choses vérifiées : les tics d'IA connus, les interdits que VOUS avez
écrits dans brain/voix.md, et le registre (tutoiement / vouvoiement) déclaré.
Code de sortie 1 s'il reste un point bloquant.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _article import (Article, Constat, afficher, gabarits_non_remplis,  # noqa: E402
                      lire_brain, normalise)

# Les formules qui trahissent un texte non relu. Complétez la liste : chaque
# ajout est une correction que vous ne referez plus jamais à la main.
TICS_IA = [
    "dans un monde en constante evolution",
    "il est important de noter",
    "il convient de souligner",
    "force est de constater",
    "a l'ere du numerique",
    "plongeons dans",
    "dans cet article, nous allons explorer",
    "en conclusion,",
    "n'hesitez pas a",
    "revolutionnaire",
    "incontournable",
    "game changer",
    "veritable mine d'or",
    "sans plus attendre",
    "la cle du succes",
    "de nombreux avantages",
]

# Signature typographique d'un texte généré : le cadratin.
CADRATIN = "—"


def _interdits_du_projet(brain):
    """Les puces de « Les interdits d'écriture » dans brain/voix.md.
    Les gabarits entre crochets sont ignorés : ce ne sont pas des règles."""
    voix = brain.get("voix.md", "")
    bloc = voix.split("## Les interdits")
    if len(bloc) < 2:
        return []
    out = []
    for ligne in bloc[1].split("\n"):
        nu = ligne.strip()
        if nu.startswith(("-", "*")):
            nu = nu.lstrip("-* ").strip()
            nu = re.sub(r"\[[^\]]*\]", "", nu).strip(" \t:;.")
            guillemets = re.findall(r"[«\"]\s*([^»\"]{3,60})\s*[»\"]", nu)
            out.extend(guillemets if guillemets else ([nu] if len(nu) > 6 else []))
    return out


def _registre_declare(brain):
    voix = normalise(brain.get("voix.md", ""))
    m = re.search(r"registre\s*:\*{0,2}\s*([^\n]+)", voix)
    if not m:
        return None
    valeur = m.group(1)
    if "[" in valeur:
        return None
    if "vouvoiement" in valeur:
        return "vouvoiement"
    if "tutoiement" in valeur:
        return "tutoiement"
    return None


def run(chemin):
    a = Article(chemin)
    brain = lire_brain()
    c = []

    # Le contexte doit être rempli : sinon l'article ne peut pas sonner comme vous.
    for nom, contenu in brain.items():
        restants = gabarits_non_remplis(contenu)
        if restants:
            c.append(Constat(Constat.BLOQUANT, "Contexte",
                             "brain/%s : %d gabarit(s) non rempli(s), à commencer par « %s »"
                             % (nom, len(restants), restants[0][:40])))

    corps_norm = normalise(a.corps)

    for tic in TICS_IA:
        if tic in corps_norm:
            c.append(Constat(Constat.BLOQUANT, "Tic IA", "formule d'IA : « %s »" % tic,
                             a.numero_ligne(tic.split(",")[0][:20])))

    deja_vus = {normalise(t) for t in TICS_IA if t in corps_norm}
    for interdit in _interdits_du_projet(brain):
        interdit_norm = normalise(interdit)
        if any(interdit_norm in t or t in interdit_norm for t in deja_vus):
            continue  # déjà signalé comme tic d'IA, on ne le compte pas deux fois
        if interdit_norm in corps_norm:
            c.append(Constat(Constat.BLOQUANT, "Interdit",
                             "interdit de brain/voix.md : « %s »" % interdit,
                             a.numero_ligne(interdit[:20])))

    if CADRATIN in a.corps:
        n = a.corps.count(CADRATIN)
        c.append(Constat(Constat.ALERTE, "Typo",
                         "%d cadratin(s) « — » : signature d'un texte généré, préférez deux phrases" % n,
                         a.numero_ligne(CADRATIN)))

    registre = _registre_declare(brain)
    if registre:
        vous = len(re.findall(r"\b(vous|votre|vos)\b", corps_norm))
        tu = len(re.findall(r"\b(tu|ton|ta|tes|toi)\b", corps_norm))
        if registre == "vouvoiement" and tu > vous * 0.2:
            c.append(Constat(Constat.BLOQUANT, "Registre",
                             "vouvoiement déclaré, mais %d marques de tutoiement" % tu))
        if registre == "tutoiement" and vous > tu * 0.2:
            c.append(Constat(Constat.BLOQUANT, "Registre",
                             "tutoiement déclaré, mais %d marques de vouvoiement" % vous))
    else:
        c.append(Constat(Constat.ALERTE, "Registre",
                         "registre non déclaré dans brain/voix.md : contrôle impossible"))

    # Longueur de phrase : la voix se perd dans les phrases fleuves.
    for ligne, texte in a.paragraphes:
        for p in re.split(r"(?<=[.!?…])\s+", texte):
            mots = len(re.findall(r"\b\w+\b", p))
            if mots > 40:
                c.append(Constat(Constat.ALERTE, "Rythme",
                                 "phrase de %d mots : coupez-la en deux" % mots, ligne))
    return c


def note(constats):
    penalite = sum(15 if x.niveau == Constat.BLOQUANT else 5 for x in constats)
    return max(0, 100 - penalite)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    if not os.path.isfile(sys.argv[1]):
        print("Fichier introuvable : %s" % sys.argv[1])
        sys.exit(2)
    constats = run(sys.argv[1])
    afficher("Contrôle de voix — vos mots, pas ceux de l'IA", constats, note(constats))
    sys.exit(1 if any(x.niveau == Constat.BLOQUANT for x in constats) else 0)
