# Parcours Complexité des algorithmes

Site public et interactif pour apprendre la complexité des algorithmes : savoir, devant n'importe quel
algorithme (un tri, une récursion, RSA, AES…), dire ce qu'il coûte, le démontrer proprement et en tirer
les conséquences. 50 étapes en 10 modules, de la méthode ligne par ligne jusqu'à la taille des clés.

Chaque étape suit le même gabarit en quatre temps, puis un test de sortie :

1. **Comprendre** : explication, vidéo sous-titrée, et l'**animateur** qui exécute l'algorithme ligne par ligne avec ses compteurs.
2. **Démontrer** : correction et calcul du coût, avec l'idée, le squelette, puis la preuve repliée.
3. **Implémenter** : l'étudiant code dans la page (Python exécuté dans le navigateur avec Pyodide), des tests vérifient,
   puis la **mesure** lance son code sur des tailles croissantes et trace le coût réel à côté des formules.
4. **S'exercer** : exercices gradués avec indice et correction rédigée, puis le QCM de sortie qui valide l'étape.

Le site comprend aussi une page de **calculateurs** (temps selon la complexité, taille maximale traitable, coût d'une attaque).

## État

Lancer `python3 build.py` affiche l'avancement module par module. L'étape pilote **3.3 Le tri par insertion**
(exercice 2 de l'annale UCAD 2024-2025) est entièrement rédigée ; les autres étapes affichent leur fiche
(objectif, prérequis, lien avec l'examen) en attendant leur cours.

## Construire et publier

```bash
python3 build.py                     # régénère docs/ à partir du contenu
python3 outils/verifier_insertion.py # vérifie par simulation les nombres de l'étape 3.3
cd docs && python3 -m http.server    # aperçu sur http://localhost:8000
```

GitHub Pages : *Settings → Pages*, branche `main`, dossier `/docs`.

Tout fonctionne hors ligne (MathJax, polices et Python sont dans le dépôt), sauf une limite : les ateliers de code
ont besoin que le site soit servi par un serveur (en ligne, ou `python3 -m http.server`), pas ouvert par double-clic.

## Organisation

```
build.py               le générateur : lit contenu/, écrit docs/ ; vérifie prérequis et vidéos
contenu/
  registre.py          les 10 modules et leurs 50 étapes : titres, objectifs, prérequis, lien avec l'annale
  briques.py           les blocs d'écriture (voir ci-dessous)
  module3.py …         le cours rédigé, un fichier par module (dictionnaire CORPS)
modele/
  style.css            identité visuelle commune aux sites MathNexus (cahier quadrillé / tableau noir)
  complexite.css       ajouts : animateur, mesure, calculateurs, accueil ; polices embarquées
  site.js              navigation, quatre temps, QCM, progression gardée sur l'appareil
  atelier.js, atelier-worker.js   ateliers de code (Pyodide, dans un fil séparé)
  animateur.js         l'animateur pas à pas (un algorithme = une fonction trace)
  mesure.js            la mesure expérimentale et son graphique
  calculateur.js       les calculateurs
  vendor/              MathJax, Pyodide, polices
outils/
  verifier_insertion.py   simulation qui vérifie toutes les valeurs de l'étape 3.3
  video/                  génération des vidéos et de leurs sous-titres (voix Kokoro, capture Playwright, ffmpeg)
docs/                  LE SITE — ne rien y modifier à la main, c'est écrasé à chaque construction
  videos/              les .mp4 et leurs sous-titres .vtt
```

## Rédiger une étape

L'étape existe déjà dans `contenu/registre.py`. Son cours s'écrit dans `contenu/moduleN.py` :

```python
CORPS["m3-recherche"] = etape(ENTREE, COMPRENDRE, DEMONTRER, IMPLEMENTER, EXERCER, SORTIE, RETENIR)
```

| Brique | Rendu |
|---|---|
| `retenir(label, corps)` | encadré rouge : définition ou théorème à savoir |
| `preuve(label, énoncé, idée, squelette, preuve)` | énoncé, idée, squelette à compléter, démonstration repliée |
| `methode(titre, étapes)` | méthode numérotée à appliquer |
| `examen(corps)` | ce qui rapporte les points à l'examen |
| `prof(corps)` | le conseil, stylo vert |
| `master(corps)` | le lien avec la cryptographie |
| `animateur(id, algo, entrées, légende)` | algorithme exécuté pas à pas (algorithmes définis dans `modele/animateur.js`) |
| `atelier(id, consigne, départ, tests, corrigé)` | éditeur Python, tests cachés, corrigé après un essai |
| `mesure(id_atelier, consigne, fonction, tailles, courbes)` | lance le code de l'atelier et trace le coût mesuré |
| `exercice(n, niveau, énoncé, indice, correction, remarque)` | exercice gradué |
| `qcm("entree" / "sortie", questions)` | test d'entrée ou de sortie |
| `video(fichier, légende, durée)` | lecteur vidéo, sous-titres joints automatiquement |

Les formules s'écrivent en LaTeX entre `\(…\)` et `\[…\]`.

## Vidéos

```bash
pip install kokoro-onnx soundfile          # + Playwright (Node) et ffmpeg
KOKORO_DIR=/chemin/vers/modeles python3 outils/video/generer.py outils/video/scripts/m3-insertion.json
```

Le script JSON décrit chaque scène (voix, lignes écrites au tableau, légende). L'outil produit le `.mp4`
et le `.vtt` dans `docs/videos/`.

Licences : voir `LICENCE.md`.
