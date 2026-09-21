---
name: redaction-article-seo
description: Procédure de rédaction d'un article SEO à partir d'un mot-clé. Deux points de contrôle humain, une éval automatique avant soumission, zéro publication automatique. Déclencheurs : « rédige un article », « écris un article sur [mot-clé] », « article SEO ».
---

# Rédaction d'un article SEO — la procédure

Suivre les 6 étapes dans l'ordre. Les étapes 3 et 6 sont des points de contrôle : s'arrêter et attendre la validation humaine. L'étape 5 est automatique et ne se saute pas.

## Étape 1 — Charger le contexte

Lire les 4 fichiers de `brain/`. Reformuler en 3 lignes : pour qui on écrit, avec quelle voix, ce qu'on a le droit de citer. Si un gabarit n'est pas rempli, s'arrêter et demander.

## Étape 2 — Analyser l'intention

Pour le mot-clé demandé :
1. Qu'est-ce que la personne qui tape ça veut vraiment obtenir ? (tutoriel, comparatif, définition, prix...)
2. Quelle douleur de `brain/cible.md` ce mot-clé touche-t-il ?
3. Quel angle personne d'autre ne peut prendre, grâce aux preuves de `brain/identite.md` ?

## Étape 3 — Proposer le brief 🔒 CONTRÔLE

Soumettre un brief court et attendre la validation :

- **Mot-clé** et intention retenue
- **3 propositions de titre** (60 caractères max, mot-clé au début)
- **Slug**
- **Structure H2** : chaque H2 = une sous-question du lecteur
- **L'angle** en une phrase, et la preuve principale qui le porte

Ne pas rédiger tant que le brief n'est pas validé.

## Étape 4 — Rédiger

Une fois le brief validé :
1. Rédiger section par section, en appliquant `brain/voix.md` et `brain/regles-seo.md`.
2. Chaque affirmation importante porte une preuve autorisée (jamais de chiffre inventé).
3. Terminer par la FAQ (3 à 5 vraies questions) et la meta description (155 caractères max).
4. Enregistrer dans `articles/[slug].md`, avec cet en-tête exact : c'est lui que lisent les contrôles.

```
---
mot_cle: le mot-clé principal
titre: la balise title, 60 caractères max
meta: la meta description, 155 caractères max
slug: le-slug-de-l-article
---

# Le H1

Le corps de l'article.
```

## Étape 5 — Passer l'éval

Avant de montrer quoi que ce soit :

```bash
python3 scripts/eval_article.py articles/[slug].md
```

Trois contrôles tournent : la structure SEO, la voix, et les faits. Chaque point bloquant (`✗`) se corrige, puis on relance. On ne passe à l'étape 6 qu'avec le verdict **PUBLIABLE**.

Un cas mérite d'être traité à part : un chiffre signalé comme absent de `brain/` n'est pas forcément faux. Soit il est inventé et il saute, soit il est vrai et il manque à votre contexte — auquel cas on l'ajoute à `brain/identite.md`, ce qui le rend disponible pour tous les articles suivants. C'est ainsi que le contexte s'enrichit.

Pour ne lancer qu'un contrôle : `check_seo.py`, `check_voix.py` ou `check_faits.py`, même usage.

## Étape 6 — Soumettre pour relecture 🔒 CONTRÔLE

Présenter l'article avec un mini rapport de 3 lignes : le mot-clé, l'angle, les preuves utilisées. Joindre la note de l'éval. Signaler toute phrase dont la véracité mérite vérification. La publication est faite par l'humain, jamais par l'agent.

L'éval constate, elle ne juge pas le fond : un article peut afficher 98/100 et rater son angle. Elle vous fait gagner la relecture mécanique, pas la relecture éditoriale.
