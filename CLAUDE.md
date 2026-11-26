# CLAUDE.md — Parcours Complexité des algorithmes (modèle du moteur de contenu)

À lire au début de chaque conversation. À mettre à jour à la fin de chaque session (section « État » et « Journal »).

## But

Deux rôles :

1. **Le parcours** : site public et interactif pour apprendre la complexité des algorithmes (Master MCS, UCAD),
   52 étapes en 10 modules, de la méthode ligne par ligne jusqu'à la taille des clés. Publié sur GitHub Pages (`docs/`).
2. **Le modèle du moteur de contenu** (chantier 1 du skill projet-dev) : c'est le premier parcours au format
   registre + briques + générateur. Ce format doit être généralisé à tous les parcours (`mathnexus-terminale`,
   `parcours-algebre-lineaire`, `fondements-maths-mcs`, `reseaux-securite`) et produire aussi un paquet pour la
   plateforme Mathnexus.

Alseny construit pour apprendre : il lance lui-même le code. Expliquer chaque choix.

## Stack

- Python 3 sans dépendance pour le générateur (`build.py`) : chaînes HTML assemblées par les briques.
- Front statique : HTML, CSS, JavaScript sans framework ; MathJax, Pyodide et polices **embarqués** dans
  `modele/vendor/` (tout marche hors ligne, sauf les ateliers qui demandent un serveur HTTP).
- Vidéos : `outils/video/tuto.py` (voix Kokoro, capture Playwright, ffmpeg) → `docs/videos/` (.mp4 + .vtt).

## Commandes

```bash
python3 build.py                       # régénère docs/ et affiche l'avancement module par module
python3 outils/verifier_module0.py     # vérifie les nombres et corrigés du module 0
python3 outils/verifier_insertion.py   # vérifie par simulation l'étape 3.3
cd docs && python3 -m http.server      # aperçu sur http://localhost:8000

# Vidéos
cd outils/video && npm install katex@0.16.11          # une fois (+ Playwright, ffmpeg, pip install kokoro-onnx soundfile)
python3 tuto.py tutos/m3-insertion.py --brouillon /tmp/images
KOKORO_DIR=/chemin/vers/modeles python3 tuto.py tutos/m3-insertion.py
```

## Organisation

```
build.py            le générateur : lit contenu/, écrit docs/ ; vérifie prérequis et vidéos
contenu/
  registre.py       MODULES : modules et étapes (id, titre, minutes, objectif, prérequis, examen, cours)
  briques.py        blocs d'écriture : retenir, preuve, methode, examen, prof, master, animateur, atelier,
                    mesure, exercice, qcm, video, tableau… et etape() qui assemble les quatre temps
  module0.py, module3.py   le cours rédigé (dictionnaire CORPS[id] = etape(...))
modele/             style commun MathNexus (style.css) + ajouts (complexite.css), site.js, atelier*.js
                    (Pyodide dans un worker), animateur.js, mesure.js, calculateur.js, vendor/
outils/             scripts de vérification, pipeline vidéo (outils/video/)
docs/               LE SITE GÉNÉRÉ — ne jamais modifier à la main
```

## Conventions

- Contenu, code et noms en **français**.
- Gabarit d'étape en quatre temps puis sortie : **Comprendre → Démontrer → Implémenter → S'exercer**, puis QCM de sortie.
  Le troisième temps variera selon la discipline quand le moteur sera généralisé (Implémenter, Calculer, Pratiquer,
  Appliquer, Construire).
- Une étape existe d'abord dans `registre.py` ; tant que son cours n'est pas écrit, la page affiche sa fiche.
- Formules en LaTeX entre `\(…\)` et `\[…\]`.
- Chaque module rédigé a un script de vérification de ses nombres dans `outils/`.
- Identifiants d'étapes (`m3-insertion`…) : **ne plus les changer** une fois publiés ; ils deviendront les clés stables
  du paquet plateforme (la progression des élèves y sera accrochée).
- Les tutos vidéo suivent la règle du README (question, exemple au tableau, pourquoi, erreurs classiques, pause « à toi »,
  vérification et bilan).

## État (au 26/11/2026)

**Parcours** : 3 étapes rédigées sur 52 (module 0 : 0.1 et 0.2 ; étape pilote 3.3, exercice 2 de l'annale UCAD 2024-2025).
`build.py` passe et régénère `docs/` à l'identique.

**Moteur (chantier 1)** — plan dans le doc projet « Moteur de contenu — plan » (Claude, projet Dev · Moteur et plateforme).
Décisions du 26/11/2026 :
- dépôt **`mathnexus-moteur`** partagé, installé par pip à une version épinglée ; ce dépôt devient un dépôt de contenu ;
- PDF en **LaTeX au style maison** (`mathnexus.sty`) ;
- vidéos **sur Bunny Stream pour tout** (site public et plateforme) ;
- sites publiés par une **action GitHub** : plus de `docs/` généré dans Git, archive hors ligne jointe à chaque version.

Étapes : M0 squelette du moteur → M1 extraction depuis ce dépôt (site identique) → M2 statuts + `cles.lock` →
M3 sortie paquet → M4 composants partagés + évaluations en données → M5 PDF → M6 vidéos + envoi automatique du paquet.

À faire :
- [ ] statuts **brouillon → vérifié → publié** dans le registre ;
- [ ] sortie **paquet plateforme** (format 1 décrit dans `mathnexus-plateforme/backend/contenus/FORMAT_PAQUET.md` :
      manifeste JSON + fragments HTML sans script, composants déclarés par attributs `data-…`) ;
      aujourd'hui la plateforme convertit les pages HTML avec `outils/convertir_parcours.py`, pont provisoire ;
- [ ] génération des **PDF** à partir du même contenu ;
- [ ] **vidéos** référencées par leur identifiant Bunny Stream, plus stockées dans Git (aujourd'hui dans `docs/videos/`) ;
- [ ] gabarit à troisième temps variable selon la discipline ;
- [ ] migrer les autres parcours, un à la fois, en gardant chaque site en ligne.

Point d'attention pour le paquet : les ateliers (Pyodide), l'animateur et la mesure reposent sur du JavaScript dans la
page ; le format paquet interdit les scripts. Il faudra les déclarer par attributs et que l'application les anime.

## Journal

- 26/11/2026 — Création de ce fichier ; état reconstitué depuis le README et le code ; `build.py` relancé.
- 26/11/2026 — Plan du moteur proposé ; les quatre décisions sont tranchées (voir « État »). Prochaine tâche : M0.
