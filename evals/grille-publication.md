# La grille de publication

Un agent qui écrit vite ne vaut rien s'il faut tout relire. L'éval est le
troisième C — le Contrôle — rendu automatique : elle décide ce qui mérite
votre relecture et ce qui repart en correction sans vous déranger.

## La note

| Contrôle | Poids | Ce qu'il regarde | Script |
|---|---|---|---|
| **SEO** | 40 | Mot-clé placé, un seul H1, méta aux bonnes longueurs, FAQ, maillage, paragraphes courts | `scripts/check_seo.py` |
| **Voix** | 30 | Tics d'IA, vos interdits, registre respecté, phrases fleuves | `scripts/check_voix.py` |
| **Faits** | 30 | Chaque chiffre de l'article existe dans `brain/` | `scripts/check_faits.py` |

Note finale = moyenne pondérée. **Barre de publication : 80/100, et zéro
point bloquant.**

## Bloquant contre alerte

- **Bloquant (`✗`)** : l'article ne part pas. Un mot-clé absent du titre, un
  chiffre inventé, un interdit de votre `brain/voix.md`. Ce sont des fautes,
  pas des préférences.
- **Alerte (`!`)** : à regarder, pas à craindre. Un paragraphe un peu long,
  trois liens internes au lieu de deux. Vous tranchez.

Un article peut afficher 92/100 et rester bloqué : **un seul fait inventé
suffit**. C'est voulu. La vitesse ne vaut rien si elle publie des erreurs à
votre place.

## L'utiliser

```bash
python3 scripts/eval_article.py articles/mon-article.md     # un article
python3 scripts/eval_article.py articles/                   # tout le dossier
python3 scripts/eval_article.py articles/mon-article.md --json
```

Le code de sortie vaut 1 si l'article ne passe pas : de quoi brancher l'éval
dans un enchaînement automatique le jour où vous en aurez un.

## La rendre vôtre

Cette grille est un point de départ, pas une vérité.

- **Les poids** sont en haut de `scripts/eval_article.py`. Si votre enjeu est
  la voix plutôt que le SEO, inversez-les.
- **Les tics d'IA** sont dans `TICS_IA`, au début de `scripts/check_voix.py`.
  Ajoutez-y chaque formule que vous corrigez à la main : vous ne la
  corrigerez qu'une fois.
- **Vos interdits** n'ont pas besoin de toucher au code : écrivez-les dans
  `brain/voix.md`, sous « Les interdits d'écriture ». Le script les lit.
- **La barre** est la constante `SEUIL`. 80 est sévère au début. Ne la
  baissez pas : montez le niveau des articles.
