"""Lecture d'un article et du contexte brain/. Utilisé par les trois contrôles.

Aucune dépendance : Python 3.8+ suffit. Rien à installer.
"""
import os
import re
import unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def normalise(texte):
    """Minuscules, sans accents, espaces normalisés. Pour comparer sans se faire
    piéger par « clé » / « cle » ou par une espace insécable."""
    texte = texte.replace(" ", " ").replace(" ", " ")
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texte).strip().lower()


class Article:
    """Un article = un en-tête optionnel entre --- et un corps en markdown."""

    def __init__(self, chemin):
        self.chemin = chemin
        with open(chemin, encoding="utf-8") as f:
            brut = f.read()
        self.entete, self.corps, self.decalage = self._decouper(brut)
        self.lignes = self.corps.split("\n")

    @staticmethod
    def _decouper(brut):
        if brut.startswith("---"):
            fin = brut.find("\n---", 3)
            if fin != -1:
                bloc = brut[3:fin]
                corps = brut[fin + 4:].lstrip("\n")
                entete = {}
                for ligne in bloc.split("\n"):
                    if ":" in ligne:
                        cle, _, valeur = ligne.partition(":")
                        entete[cle.strip().lower()] = valeur.strip()
                return entete, corps, brut[:fin].count("\n") + 2
        return {}, brut, 0

    def champ(self, nom):
        return self.entete.get(nom, "")

    @property
    def mot_cle(self):
        return self.champ("mot_cle")

    @property
    def titre(self):
        return self.champ("titre") or (self.h1[0] if self.h1 else "")

    @property
    def meta(self):
        return self.champ("meta")

    @property
    def slug(self):
        return self.champ("slug") or os.path.splitext(os.path.basename(self.chemin))[0]

    @property
    def h1(self):
        return [m.group(1).strip() for m in re.finditer(r"^#\s+(.+)$", self.corps, re.M)]

    @property
    def h2(self):
        return [m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", self.corps, re.M)]

    @property
    def paragraphes(self):
        """(numéro de ligne dans le fichier, texte) pour chaque paragraphe de prose."""
        out = []
        courant, depart = [], None
        for i, ligne in enumerate(self.lignes):
            nu = ligne.strip()
            structurel = (
                not nu
                or nu.startswith(("#", ">", "-", "*", "|", "```"))
                or re.match(r"^\d+[.)]\s", nu)
            )
            if structurel:
                if courant:
                    out.append((depart + self.decalage + 1, " ".join(courant)))
                    courant, depart = [], None
            else:
                if depart is None:
                    depart = i
                courant.append(nu)
        if courant:
            out.append((depart + self.decalage + 1, " ".join(courant)))
        return out

    @property
    def texte_prose(self):
        return " ".join(t for _, t in self.paragraphes)

    @property
    def nb_mots(self):
        return len(re.findall(r"\b\w+\b", self.corps))

    @property
    def liens(self):
        return re.findall(r"\[[^\]]*\]\(([^)]+)\)", self.corps)

    def numero_ligne(self, motif, depuis=0):
        for i, ligne in enumerate(self.lignes[depuis:], start=depuis):
            if motif in ligne:
                return i + self.decalage + 1
        return None


def phrases(texte):
    morceaux = re.split(r"(?<=[.!?…])\s+", texte.strip())
    return [p for p in morceaux if p.strip()]


def lire_brain(racine=RACINE):
    """Renvoie {nom_fichier: contenu} pour brain/*.md."""
    dossier = os.path.join(racine, "brain")
    fichiers = {}
    if os.path.isdir(dossier):
        for nom in sorted(os.listdir(dossier)):
            if nom.endswith(".md"):
                with open(os.path.join(dossier, nom), encoding="utf-8") as f:
                    fichiers[nom] = f.read()
    return fichiers


def gabarits_non_remplis(contenu):
    """Les gabarits du kit sont entre crochets. Tant qu'ils y sont, le contexte
    n'est pas rempli et l'agent travaille à l'aveugle."""
    return re.findall(r"\[([^\]\n]{3,80})\]", contenu)


class Constat:
    """Un point relevé par un contrôle."""

    BLOQUANT = "bloquant"
    ALERTE = "alerte"

    def __init__(self, niveau, regle, message, ligne=None):
        self.niveau, self.regle, self.message, self.ligne = niveau, regle, message, ligne

    def __str__(self):
        marque = "✗" if self.niveau == self.BLOQUANT else "!"
        ou = " (ligne %d)" % self.ligne if self.ligne else ""
        return "  %s [%s] %s%s" % (marque, self.regle, self.message, ou)

    def dict(self):
        return {"niveau": self.niveau, "regle": self.regle,
                "message": self.message, "ligne": self.ligne}


def afficher(titre, constats, note=None):
    print("\n%s" % titre)
    print("-" * len(titre))
    if not constats:
        print("  ✓ rien à signaler")
    for c in constats:
        print(c)
    if note is not None:
        print("  → %d/100" % note)
    return constats
