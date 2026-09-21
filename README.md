# Agent SEO Starter · par Mantra

Le squelette de l'Agent IA qui rédige les articles du blog de Mantra en 27 minutes au lieu de 8 heures. Version de démarrage, volontairement simple : de quoi lancer votre premier agent ce week-end, sans une ligne de code.

Dedans : le contexte à remplir, la procédure de rédaction, quatre scripts de contrôle et la grille d'éval qui décide si un article est publiable.

## La méthode des 3C

Ce dossier incarne la méthode enseignée chez Mantra :

| Brique | Où elle vit | Ce que c'est |
|---|---|---|
| **Contexte** | `brain/` | Ce que l'IA doit savoir avant de travailler : votre marque, votre cible, votre voix, vos règles SEO |
| **Compétence** | `skills/` | La procédure de travail qu'elle applique, étape par étape |
| **Contrôle** | `scripts/` et `evals/` | Ce qui se vérifie tout seul (structure, voix, faits), et les deux moments où VOUS validez : le brief avant rédaction, l'article avant publication |

Un agent sans contexte produit du générique. Un agent sans procédure improvise. Un agent sans contrôle publie vos erreurs. Les trois ensemble : un agent qui produit.

## Ce qu'il y a dedans

```
brain/                    le Contexte : 4 fichiers à remplir, 30 minutes
skills/                   la Compétence : la procédure de rédaction en 6 étapes
scripts/check_seo.py      le Contrôle : structure, mot-clé, méta, FAQ, maillage
scripts/check_voix.py                   tics d'IA, vos interdits, registre
scripts/check_faits.py                  chaque chiffre existe dans brain/
scripts/eval_article.py                 les trois d'un coup : note /100 et verdict
evals/grille-publication.md             la grille, et comment la rendre vôtre
articles/                 vos articles finis
```

## Prérequis

1. Un compte Claude (claude.ai). L'idéal : [Claude Code](https://claude.com/claude-code), qui lit directement ce dossier.
2. 30 minutes pour remplir votre contexte.
3. Python 3 pour les scripts de contrôle. Il est déjà installé sur macOS et Linux. Aucune bibliothèque à installer : les scripts n'utilisent que la bibliothèque standard.

Ça fonctionne aussi avec ChatGPT ou Gemini : copiez le contenu de `brain/` et du skill en début de conversation.

## Démarrage en 3 étapes

### 1. Remplissez votre Contexte (30 min)

Ouvrez les 4 fichiers de `brain/` et remplacez les gabarits par votre réalité :

- `brain/identite.md` : qui vous êtes, ce que vous vendez
- `brain/cible.md` : à qui vous parlez, ses problèmes réels
- `brain/voix.md` : comment vous écrivez (et ce que vous vous interdisez)
- `brain/regles-seo.md` : déjà pré-rempli, ajustez si besoin

Conseil : ne visez pas la perfection. Un contexte à 70 % rempli bat un contexte parfait jamais terminé. Vous l'enrichirez à chaque article.

### 2. Lancez votre première mission

Ouvrez Claude Code dans ce dossier et écrivez :

```
Rédige un article SEO sur [votre mot-clé]. Suis la procédure du skill redaction-article-seo.
```

L'agent lit votre contexte, applique la procédure, et s'arrête au premier point de contrôle : le brief.

### 3. Gardez le Contrôle

L'agent vous soumet un brief (angle, titre, structure). Vous validez ou corrigez. Il rédige. Puis il passe l'article à l'éval avant même de vous le montrer :

```bash
python3 scripts/eval_article.py articles/mon-article.md
```

Trois contrôles tournent, chacun rend une note, et le verdict tombe : **PUBLIABLE**, ou la liste précise de ce qui ne va pas. Un seul chiffre inventé suffit à bloquer l'article, même noté 92/100. C'est voulu : la vitesse ne vaut rien si elle publie des erreurs à votre place.

Vous relisez ensuite le fond. C'est vous qui publiez, toujours.

**Essayez tout de suite**, sans rien avoir rempli :

```bash
python3 scripts/eval_article.py evals/exemple-article.md
```

L'éval commence par vous dire que votre contexte est vide. C'est exactement le point : un agent sans contexte ne peut rien contrôler. Remplissez `brain/`, relancez, et regardez les reproches disparaître un par un.

La grille, les poids et la barre de publication se règlent : tout est expliqué dans [`evals/grille-publication.md`](evals/grille-publication.md).

## Les limites de cette version

C'est un squelette de démarrage. Les contrôles fournis vérifient ce qui est vérifiable dans le texte : sa structure, sa voix, ses chiffres. Ils ne savent rien du monde extérieur.

La version complète que construisent nos élèves ajoute : l'analyse des concurrents en direct (SERP), la vérification des positions et du trafic réel (Search Console, GA4), la génération des visuels, la publication automatisée sur le CMS, et des agents pour les autres canaux (veille, reporting, campagnes).

Tout ça s'apprend en 6 semaines, accompagné : [les formations IA de Mantra](https://formations.mantra.work/?utm_source=github&utm_medium=starter-kit&utm_campaign=cours-agents-ia).

---

© 2026 École Mantra. Libre d'utilisation pour votre propre marketing. Revente ou redistribution interdites.
