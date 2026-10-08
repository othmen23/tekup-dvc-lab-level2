# Niveau 2 : pipeline DVC + Git avancé

## Exercice 2.1 : pipeline en 3 étapes
- Étapes `prepare`, `train`, `evaluate` (dvc.yaml), hyperparamètres dans params.yaml.
- `metrics/metrics.json` déclaré avec `cache: false` (option `-M`).
- Piège rencontré : les sorties (train.csv, test.csv, model.pkl) avaient été ajoutées à Git par `git add .` car les .gitignore n'existaient pas encore. Corrigé avec `git rm --cached` puis `dvc repro --force`.
- Métriques : accuracy 0.9917, f1_score 0.9918.

## Exercice 2.2 : hooks
`.pre-commit-config.yaml` : black + check-added-large-files (--maxkb=5000). Message obtenu en committant un fichier de 8 Mo :

    check for added large files..............................................Failed
    - hook id: check-added-large-files
    - exit code: 1

    big.bin (7813 KB) exceeds 5000 KB.

## Exercice 2.3 : expérimentation, rebase, tag
- Branche `experiment/rf-tuning` : 3 commits WIP (fix typo, n_estimators=200, max_depth=5), chacun précédé de `dvc repro`.
- `dvc params diff main` : max_depth 3 -> 5, n_estimators 100 -> 200. `dvc metrics diff main` est vide : le réglage n'a pas changé le score sur Iris.
- `git rebase -i main` : les 3 commits sont écrasés en un seul (559b89e) "Tune random forest: n_estimators=200, max_depth=5".
- Merge fast-forward dans main, `dvc repro` : tout à jour. Tag annoté `v1.1.0-rf-tuned` (acc=0.9917).
- Black a reformaté `src/train.py` pendant les commits ; il faut re-ajouter le fichier et recommencer le commit.

## Questions de contrôle

**Quelles étapes se sont ré-exécutées quand seul un hyperparamètre de `train` a changé, et pourquoi `prepare` a-t-elle été ignorée ?**
`train` puis `evaluate`. `prepare` ne dépend que de `iris.csv`, de `prepare.py` et des paramètres `prepare.*` : leurs hashes dans dvc.lock n'ont pas changé. `train` dépend des paramètres `train.*`, et `evaluate` du hash de `model.pkl`, qui a changé.

**Pourquoi peut-on rebaser `experiment/rf-tuning` sans risque ? Dans quel cas serait-ce interdit ?**
C'est une branche locale, jamais poussée : réécrire ses commits ne perturbe personne. Ce serait interdit sur une branche partagée ou déjà poussée, car les copies des collègues divergeraient après un `push --force`.

**Pourquoi un tag annoté est-il préférable à un tag léger pour un jalon de modèle ?**
Un tag annoté est un objet Git complet (auteur, date, message, signature possible). Il documente pourquoi le jalon existe (ici l'accuracy et le renvoi vers dvc.lock). Un tag léger n'est qu'un nom qui pointe vers un commit.
