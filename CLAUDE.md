# CLAUDE.md — Parcours Complexité des algorithmes (modèle du moteur de contenu)

À lire au début de chaque conversation. À mettre à jour à la fin de chaque session (section « État » et « Journal »).

## But

Deux rôles :

1. **Le parcours** : site public et interactif pour apprendre la complexité des algorithmes (Master MCS, UCAD),
   52 étapes en 10 modules, de la méthode ligne par ligne jusqu'à la taille des clés. Publié sur GitHub Pages par une action.
2. **Le premier parcours construit par le moteur de contenu** (`AlsenyTECH/mathnexus-moteur`, chantier 1 du skill
   projet-dev). Le générateur et les briques en ont été extraits à l'étape M1 ; ce dépôt ne garde que le contenu
   et ce qui lui est propre.

Alseny construit pour apprendre : il lance lui-même le code. Expliquer chaque choix.

## Stack

- Générateur : **mathnexus-moteur**, installé par `pip install -r requirements.txt` (version épinglée) ; réglages du site
  dans `parcours.toml`. Les briques renvoient des objets (`from moteur.blocs import …`), assemblés avec `+`.
- Front statique : HTML, CSS, JavaScript sans framework ; MathJax, Pyodide, polices, style commun, ateliers et mesure
  viennent du moteur (tout marche hors ligne, sauf les ateliers qui demandent un serveur HTTP).
- Vidéos : `outils/video/tuto.py` (voix Kokoro, capture Playwright, ffmpeg) → `videos/` (.mp4 + .vtt).

## Commandes

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # le moteur (commande « moteur »)
moteur construire                      # construit _site/ et affiche l'avancement module par module
python outils/verifier_module0.py      # vérifie les nombres et corrigés du module 0
python outils/verifier_insertion.py    # vérifie par simulation l'étape 3.3
cd _site && python3 -m http.server     # aperçu sur http://localhost:8000

# Vidéos
cd outils/video && npm install katex@0.16.11          # une fois (+ Playwright, ffmpeg, pip install kokoro-onnx soundfile)
python3 tuto.py tutos/m3-insertion.py --brouillon /tmp/images
KOKORO_DIR=/chemin/vers/modeles python3 tuto.py tutos/m3-insertion.py
```

## Organisation

```
parcours.toml       réglages du site : titres, liens, macros MathJax, scripts, nom des parties, quatre temps
requirements.txt    la version du moteur
contenu/
  registre.py       PARTIES : modules et étapes (id, titre, minutes, objectif, prérequis, examen, cours)
  module0.py, module3.py   le cours rédigé (CORPS[id] = etape(...)), avec les briques de moteur.blocs
  pages.py          les pages propres : accueil et calculateurs
modele/             ce qui est propre au parcours : complexite.css, animateur.js (algorithmes), calculateur.js
videos/             les vidéos et leurs sous-titres (dans Git jusqu'à Bunny Stream, M6)
outils/             scripts de vérification, pipeline vidéo (outils/video/)
.github/workflows/  publier.yml (construit et publie Pages) ; preuve-m1.yml (temporaire, voir État)
_site/              LE SITE CONSTRUIT — ignoré par Git
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
Le site est construit par le moteur (M1, v0.1.0) : identique, octet par octet, à celui de l'ancien `build.py`
(commit `2df94a6`, étiquette `avant-moteur`). L'action `preuve-m1.yml` refait cette comparaison : **la supprimer au
premier changement de contenu**, puisque le site changera alors exprès.

**Moteur (chantier 1)** — plan dans le doc projet « Moteur de contenu — plan » (Claude, projet Dev · Moteur et plateforme).
Décisions du 26/11/2026 :
- dépôt **`mathnexus-moteur`** partagé, installé par pip à une version épinglée ; ce dépôt devient un dépôt de contenu ;
- PDF en **LaTeX au style maison** (`mathnexus.sty`) ;
- vidéos **sur Bunny Stream pour tout** (site public et plateforme) ;
- sites publiés par une **action GitHub** : plus de `docs/` généré dans Git, archive hors ligne jointe à chaque version.

Étapes : M0 squelette du moteur → **M1 extraction depuis ce dépôt (fait)** → M2 statuts + `cles.lock` →
M3 sortie paquet → M4 composants partagés + évaluations en données → M5 PDF → M6 vidéos + envoi automatique du paquet.

À faire :
- [ ] statuts **brouillon → vérifié → publié** dans le registre ;
- [ ] sortie **paquet plateforme** (format 1 décrit dans `mathnexus-plateforme/backend/contenus/FORMAT_PAQUET.md` :
      manifeste JSON + fragments HTML sans script, composants déclarés par attributs `data-…`) ;
      aujourd'hui la plateforme convertit les pages HTML avec `outils/convertir_parcours.py`, pont provisoire ;
- [ ] génération des **PDF** à partir du même contenu ;
- [ ] **vidéos** référencées par leur identifiant Bunny Stream, plus stockées dans Git (aujourd'hui dans `videos/`) ;
- [x] gabarit à troisième temps variable selon la discipline (`[gabarit] temps` dans `parcours.toml`) ;
- [x] publication par action GitHub, `docs/` retiré de Git (M1) ;
- [ ] migrer les autres parcours, un à la fois, en gardant chaque site en ligne.

Point d'attention pour le paquet : les ateliers (Pyodide), l'animateur et la mesure reposent sur du JavaScript dans la
page ; le format paquet interdit les scripts. Il faudra les déclarer par attributs et que l'application les anime.

## Journal

- 26/11/2026 — Création de ce fichier ; état reconstitué depuis le README et le code ; `build.py` relancé.
- 26/11/2026 — Plan du moteur proposé ; les quatre décisions sont tranchées (voir « État »). Prochaine tâche : M0.
- 26/11/2026 — M1 : le site est construit par mathnexus-moteur (`moteur construire`) ; `build.py`, `briques.py`, le style
  commun, les ateliers, la mesure et vendor/ retirés (fournis par le moteur) ; `pages.py` garde l'accueil et les
  calculateurs ; `verifier_module0.py` lit les ateliers comme objets. Publication par action, vidéos dans `videos/`.
  Preuve : `moteur comparer` contre l'ancien `build.py`, sites identiques. PR #1.
