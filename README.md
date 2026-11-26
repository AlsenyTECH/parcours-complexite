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

Lancer `moteur construire` affiche l'avancement module par module. Rédigés : module 0 (0.1 et 0.2) et l'étape pilote 3.3
(exercice 2 de l'annale UCAD 2024-2025). Les autres étapes affichent leur fiche (objectif, prérequis, lien avec l'examen)
en attendant leur cours. Les nombres de chaque module rédigé sont vérifiés par un script de `outils/`.

## Construire et publier

Le site est construit par le moteur de contenu MathNexus
([mathnexus-moteur](https://github.com/AlsenyTECH/mathnexus-moteur)), installé à une version épinglée
dans `requirements.txt`. Les réglages du site sont dans `parcours.toml`.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt      # installe le moteur (commande « moteur »)
moteur construire                    # régénère le site à partir du contenu
python3 outils/verifier_module0.py   # vérifie les nombres et les corrigés du module 0
python3 outils/verifier_insertion.py # vérifie par simulation les nombres de l'étape 3.3
cd docs && python3 -m http.server    # aperçu sur http://localhost:8000
```

GitHub Pages : *Settings → Pages*, branche `main`, dossier `/docs`.

Tout fonctionne hors ligne (MathJax, polices et Python sont dans le dépôt), sauf une limite : les ateliers de code
ont besoin que le site soit servi par un serveur (en ligne, ou `python3 -m http.server`), pas ouvert par double-clic.

## Organisation

```
parcours.toml          les réglages du site (titres, liens, macros, scripts, nom des parties)
requirements.txt       la version du moteur
contenu/
  registre.py          les 10 modules et leurs 50 étapes : titres, objectifs, prérequis, lien avec l'annale
  module3.py …         le cours rédigé, un fichier par module (dictionnaire CORPS)
  pages.py             les pages propres : l'accueil et les calculateurs
modele/                ce qui est propre à ce parcours (le reste vient du moteur)
  complexite.css       ajouts : animateur, mesure, calculateurs, accueil
  animateur.js         l'animateur pas à pas (un algorithme = une fonction trace)
  calculateur.js       les calculateurs
outils/
  verifier_insertion.py   simulation qui vérifie toutes les valeurs de l'étape 3.3
  video/                  génération des vidéos et de leurs sous-titres (voix Kokoro, capture Playwright, ffmpeg)
docs/                  LE SITE — ne rien y modifier à la main, c'est écrasé à chaque construction
  videos/              les .mp4 et leurs sous-titres .vtt
```

## Rédiger une étape

L'étape existe déjà dans `contenu/registre.py`. Son cours s'écrit dans `contenu/moduleN.py`, avec les briques
du moteur (`from moteur.blocs import retenir, preuve, …`). Chaque brique renvoie un objet, et on les assemble
avec `+` entre du HTML simple ; un bloc ne se met pas dans un `%` ou un `join` (erreur claire).

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

## Vidéos : des tutos au tableau

Les tutos s'écrivent en Python dans `outils/video/tutos/<étape>.py`, comme une suite de répliques : chaque phrase dite par la voix
est accompagnée des gestes faits au tableau pendant qu'elle est prononcée.

```python
T.dit("Premier test : huit est-il plus grand que deux ? Oui. On décale le huit dans la case libre.",
      marque("T", "i", 2, ROUGE), ecrire("c2", 300, 420, "8 > 2 ?  oui → on décale"),
      glisse("T", 2, 3, a=0.7))          # a = moment du geste dans la phrase (0 → début, 1 → fin)
T.pause("Combien de fois la ligne 1 est-elle exécutée ?", 7)
```

Gestes disponibles : `ecrire`, `formule` (LaTeX), `cases` (tableau de valeurs), `valeur`, `etat` (trié, actif, clé, vide, éliminé),
`marque` (i, j… sous une case), `glisse` (une valeur vole d'une case à l'autre), `boite`, `extrait`, `depose`, `code`, `hl` (surligner
des lignes), `compte` (nombre d'exécutions d'une ligne), `table`, `cellule`, `compteur`, `fleche`, `trait`, `entoure`, `efface`, et `pause`.

```bash
cd outils/video && npm install katex@0.16.11       # une fois ; + Playwright (Node), ffmpeg, pip install kokoro-onnx soundfile
python3 tuto.py tutos/m3-insertion.py --brouillon /tmp/images   # minutage estimé + une image par réplique : contrôle de la mise en page
KOKORO_DIR=/chemin/vers/modeles python3 tuto.py tutos/m3-insertion.py   # la vidéo et ses sous-titres dans docs/videos/
```

**Ce qu'est un bon tuto** (la règle de tous les tutos du site) :

1. une **question** pour commencer, qui dit ce qu'on va savoir faire à la fin ;
2. un **exemple travaillé au tableau** avant toute formule ;
3. le **pourquoi** de chaque étape, dit à voix haute (« pourquoi n et pas n − 1 ? ») ;
4. les **erreurs classiques**, montrées et corrigées ;
5. au moins une **pause « à toi »** avant une réponse importante ;
6. une **vérification** sur l'exemple, puis un **bilan** court : la méthode, réutilisable ailleurs.

L'ancien outil (`generer.py`, `page.html`, scripts JSON) n'écrit que des lignes de texte ; il reste pour mémoire, les tutos
sont refaits avec `tuto.py`.

Licences : voir `LICENCE.md`.
