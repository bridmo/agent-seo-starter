# Agent SEO Starter · par Mantra

Le squelette de l'Agent IA qui rédige les articles du blog de Mantra en 27 minutes au lieu de 8 heures. Version de démarrage, volontairement simple : de quoi lancer votre premier agent ce week-end, sans une ligne de code.

## La méthode des 3C

Ce dossier incarne la méthode enseignée chez Mantra :

| Brique | Où elle vit | Ce que c'est |
|---|---|---|
| **Contexte** | `brain/` | Ce que l'IA doit savoir avant de travailler : votre marque, votre cible, votre voix, vos règles SEO |
| **Compétence** | `skills/` | La procédure de travail qu'elle applique, étape par étape |
| **Contrôle** | les points de validation | Les moments où VOUS validez : le brief avant rédaction, l'article avant publication |

Un agent sans contexte produit du générique. Un agent sans procédure improvise. Un agent sans contrôle publie vos erreurs. Les trois ensemble : un agent qui produit.

## Prérequis

1. Un compte Claude (claude.ai). L'idéal : [Claude Code](https://claude.com/claude-code), qui lit directement ce dossier.
2. 30 minutes pour remplir votre contexte.

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

L'agent vous soumet un brief (angle, titre, structure). Vous validez ou corrigez. Il rédige. Vous relisez avant de publier. C'est vous qui publiez, toujours.

## Les limites de cette version

C'est un squelette de démarrage. La version complète que construisent nos élèves ajoute : l'analyse des concurrents en direct (SERP), les scripts de contrôle automatique de la voix et des faits, la génération des visuels, la publication automatisée sur le CMS, et des agents pour les autres canaux (veille, reporting, campagnes).

Tout ça s'apprend en 6 semaines, accompagné : [les formations IA de Mantra](https://formations.mantra.work/?utm_source=github&utm_medium=starter-kit&utm_campaign=cours-agents-ia).

---

© 2026 École Mantra. Libre d'utilisation pour votre propre marketing. Revente ou redistribution interdites.
