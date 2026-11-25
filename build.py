# -*- coding: utf-8 -*-
"""Générateur du site « Parcours Complexité des algorithmes ».

    python3 build.py

Lit contenu/registre.py (les modules et leurs étapes) et contenu/moduleN.py (le cours rédigé),
écrit docs/index.html, docs/module-0.html … module-9.html, docs/calculateurs.html et docs/assets/.
Refuse de construire si un prérequis manque ou vient après l'étape qui l'utilise,
ou si une vidéo citée dans le cours n'existe pas.
"""

import html
import importlib
import os
import re
import shutil
import sys

RACINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RACINE, "contenu"))

import registre as R  # noqa: E402
from briques import retenir, video  # noqa: E402,F401

PUBLIC = os.path.join(RACINE, "docs")
MODELE = os.path.join(RACINE, "modele")

SITE = "Parcours Complexité"
SITE_LONG = "Parcours Complexité des algorithmes"
SOUS_TITRE = "Mesurer, calculer, comparer — de la boucle au cryptosystème"
AUTEUR = "MathNexus"
ANNEE = 2026

MATHJAX = r"""<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']], displayMath: [['\\[', '\\]']],
    macros: { N:'\\mathbb{N}', Z:'\\mathbb{Z}', R:'\\mathbb{R}', F:'\\mathbb{F}',
              pgcd:'\\operatorname{pgcd}', Card:'\\operatorname{Card}', cle:'\\text{clé}' }
  },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'], ignoreHtmlClass: 'tex2jax_ignore' },
  svg: { fontCache: 'global' }
};
</script>
<script defer src="assets/mathjax/tex-svg.js"></script>"""

THEME_INIT = ("<script>try{var t=localStorage.getItem('complexite-theme');"
              "if(t)document.documentElement.dataset.theme=t;}catch(e){}</script>")
THEME_BTN = '<button type="button" class="theme-btn" aria-pressed="false">Thème sombre</button>'


def pied():
    return ('<footer class="pied"><p>© %d %s · Contenu sous licence '
            '<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr">CC BY-NC-SA 4.0</a>, '
            'code sous licence MIT. Site personnel, sans lien officiel avec une université.</p></footer>'
            % (ANNEE, AUTEUR))


def barre(courant=""):
    liens = [("index.html", "Accueil"), ("calculateurs.html", "Calculateurs"),
             ("module-9.html", "Préparer l'examen")]
    l = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == courant else "", t)
                for h, t in liens)
    return ('<header class="barre"><a class="barre-brand" href="index.html">%s</a>'
            '<nav class="barre-liens" aria-label="Pages">%s</nav><span style="flex:1"></span>%s</header>'
            % (SITE, l, THEME_BTN))


def coquille(titre, body, data="", scripts=()):
    js = "".join('<script defer src="assets/%s"></script>' % s for s in scripts)
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="Un parcours complet et interactif sur la complexité des algorithmes : notations asymptotiques, analyse des boucles et des récursions, classes P et NP, et application aux algorithmes cryptographiques.">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%%3E%%3Crect width='32' height='32' rx='6' fill='%%23bd1f2b'/%%3E%%3Ctext x='16' y='23' font-size='18' text-anchor='middle' fill='white' font-family='serif'%%3EO%%3C/text%%3E%%3C/svg%%3E">
<link rel="stylesheet" href="assets/style.css">
%s
%s
</head>
<body%s>
%s
<script defer src="assets/outils.js"></script>%s
</body>
</html>
""" % (html.escape(titre), THEME_INIT, MATHJAX, data, body, js)


# ─────────────────────────────────────────────────────────────────────────────
_MATHS = re.compile(r"(\\\((?:.|\n)+?\\\)|\\\[(?:.|\n)+?\\\])")


def proteger_maths(texte):
    """Dans les formules, < et > deviennent \\lt et \\gt : sinon le navigateur y voit des balises."""
    return _MATHS.sub(lambda m: m.group(0).replace("<", r"\lt ").replace(">", r"\gt "), texte)


def lien(eid):
    e, m = R.INDEX[eid]
    return '<a href="%s#%s">%s %s</a>' % (m.fichier, eid, R.numero(eid), html.escape(e.titre))


def fiche(e):
    pre = ", ".join(lien(p) for p in e.prereq) or '<span class="rien">aucun — on peut commencer ici</span>'
    suite = [x for x in R.INDEX if e.id in R.INDEX[x][0].prereq]
    ouv = ", ".join(lien(s) for s in suite) or '<span class="rien">—</span>'
    lignes = '<dt>Prérequis</dt><dd>%s</dd><dt>Sert ensuite à</dt><dd>%s</dd>' % (pre, ouv)
    if e.examen:
        lignes += '<dt>À l\'examen</dt><dd><span class="pastille exam">%s</span></dd>' % html.escape(e.examen)
    if e.cours:
        lignes += '<dt>Dans le cours</dt><dd>%s</dd>' % html.escape(e.cours)
    return '<div class="fiche"><dl>%s</dl></div>' % lignes


def section_etape(e, m):
    corps = e.corps or (
        '<div class="a-venir"><p class="lab">Étape en cours de rédaction</p>'
        '<p>Le cours arrive. En attendant, la fiche ci-dessus dit ce qu\'il faudra savoir faire, '
        'ce qu\'il faut avoir vu avant, et à quoi l\'étape servira ensuite.</p></div>')
    num = R.numero(e.id)
    return ('<section class="lesson" id="%s" data-part="%s" data-num="%s" data-title="%s" hidden>'
            '<header class="lhead"><p class="eyebrow">Module %d · Étape %s<span class="meta">%d min</span></p>'
            '<h2>%s</h2></header><div class="lbody">'
            '<p class="objectif">%s</p>%s%s</div></section>'
            % (e.id, html.escape(m.titre), num, html.escape(e.titre), m.num, num, e.minutes,
               html.escape(e.titre), html.escape(e.objectif), fiche(e), proteger_maths(corps)))


def page_module(m, suivant):
    lignes = []
    for e in m.etapes:
        statut = ('<span class="pastille">rédigée</span>' if e.corps
                  else '<span class="rien">à venir</span>')
        lignes.append('<tr><td><a href="#%s">%s %s</a></td><td>%s</td><td>%s</td></tr>'
                      % (e.id, R.numero(e.id), html.escape(e.titre), html.escape(e.objectif), statut))
    depart = ('<section class="lesson" id="depart-%d" data-part="" data-title="Ce module en bref" hidden>'
              '<header class="lhead"><p class="eyebrow">Module %d</p><h2>%s</h2></header>'
              '<div class="lbody"><p class="lead">%s</p>'
              '<div class="howto">'
              '<div><p class="num">1</p><p><strong>Comprendre.</strong> Lis, regarde la vidéo, '
              'fais tourner l\'algorithme dans l\'animateur.</p></div>'
              '<div><p class="num">2</p><p><strong>Démontrer.</strong> Refais chaque calcul '
              'sur une feuille avant d\'ouvrir la correction.</p></div>'
              '<div><p class="num">3</p><p><strong>Implémenter.</strong> Code l\'algorithme dans la page, '
              'les tests vérifient, la mesure trace ce qu\'il coûte vraiment.</p></div>'
              '<div><p class="num">4</p><p><strong>S\'exercer.</strong> Exercices gradués, puis le test '
              'de sortie qui valide l\'étape.</p></div></div>'
              '<h3>Les %d étapes de ce module</h3><div class="table-wrap"><table><thead><tr><th>Étape</th>'
              '<th>Ce qu\'on doit savoir faire</th><th>État</th></tr></thead><tbody>%s</tbody></table></div>'
              '</div></section>'
              % (m.num, m.num, html.escape(m.titre), html.escape(m.resume), len(m.etapes), "".join(lignes)))
    sections = [depart] + [section_etape(e, m) for e in m.etapes]
    nav_mods = "".join('<li><a href="%s"%s><span class="n-num">%d</span>%s</a></li>'
                       % (x.fichier, ' class="ici"' if x is m else '', x.num, html.escape(x.titre))
                       for x in R.MODULES)
    body = """<div class="app">
  <div class="topbar">
    <button type="button" class="btn ghost" id="menu-btn" aria-controls="side" aria-expanded="false">Sommaire</button>
    <p class="brand">Module %d</p>
    <p class="mini" id="mini-prog"></p>
  </div>
  <div class="scrim" id="scrim" hidden></div>
  <nav class="side" id="side" aria-label="Sommaire du module">
    <p class="brand"><a href="index.html">%s</a></p>
    <p class="brand-sub">%s</p>
    <ul class="niveaux"><li><a href="index.html"><span class="n-num">·</span>Accueil</a></li>%s
      <li><a href="calculateurs.html"><span class="n-num">∑</span>Calculateurs</a></li></ul>
    <div class="prog"><div class="prog-bar"><div class="prog-fill" id="prog-fill"></div></div>
      <p class="prog-txt" id="prog-txt"></p></div>
    <div id="nav"></div>
    %s
  </nav>
  <main class="main" id="main">
%s
    <nav class="pager">
      <a class="btn ghost" id="prev" href="#">← Précédent</a>
      <span class="right"><p class="done-note" id="done-note" hidden>Étape validée ✓</p>
      <a class="btn" id="next" href="#">Suivant →</a></span>
    </nav>
    %s
  </main>
</div>""" % (m.num, SITE, html.escape(SOUS_TITRE), nav_mods, THEME_BTN, "\n".join(sections), pied())
    data = ' data-module="%d"%s' % (m.num, ' data-suivant="%s"' % suivant if suivant else "")
    return coquille("Module %d · %s — %s" % (m.num, m.titre, SITE_LONG), body, data,
                    ("site.js", "atelier.js", "animateur.js", "mesure.js"))


def page_accueil():
    total = sum(len(m.etapes) for m in R.MODULES)
    redigees = sum(1 for m in R.MODULES for e in m.etapes if e.corps)
    cartes = []
    for m in R.MODULES:
        items = []
        for e in m.etapes:
            pas = ''
            if e.examen:
                pas = ' <span class="pastille exam">examen</span>'
            items.append('<li data-id="%s"%s><span class="n">%s</span><a href="%s#%s">%s</a>%s</li>'
                         % (e.id, ' class="redige"' if e.corps else '', R.numero(e.id), m.fichier, e.id,
                            html.escape(e.titre), pas))
        cartes.append('<article class="mod-carte" data-module="%d" data-etapes="%s">'
                      '<h3><a href="%s"><span class="mod-num">%d</span>%s</a></h3><p>%s</p>'
                      '<div class="mod-prog"><i></i></div><p class="mod-prog-txt"></p><ol>%s</ol></article>'
                      % (m.num, " ".join(e.id for e in m.etapes), m.fichier, m.num, html.escape(m.titre),
                         html.escape(m.resume), "".join(items)))
    body = """%s
<main class="accueil">
  <section class="hero">
    <h1>La complexité des algorithmes</h1>
    <p>Un parcours complet, du premier comptage d'instructions jusqu'à la taille des clés RSA :
    %d étapes en 10 modules. Chaque étape suit le même chemin : comprendre, démontrer, coder, s'exercer.</p>
    <p class="objectif-site">Le but : devant n'importe quel algorithme — un tri, une récursion, RSA, AES —
    savoir dire ce qu'il coûte, le démontrer proprement, et en tirer les conséquences.</p>
  </section>
  <div class="pilote">
    <p><strong>Étape pilote, entièrement rédigée : 3.3 Le tri par insertion.</strong> Animateur pas à pas,
    calcul complet de T(n), atelier de code avec mesure, exercices et corrigé de l'exercice 2 de l'annale 2024-2025.</p>
    <a class="btn" href="module-3.html#m3-insertion">Ouvrir l'étape pilote →</a>
  </div>
  <h2 class="sec">Comment travailler</h2>
  <div class="howto">
    <div><p class="num">1</p><p><strong>Comprendre.</strong> L'idée, une vidéo, et l'algorithme qui tourne sous tes yeux avec ses compteurs.</p></div>
    <div><p class="num">2</p><p><strong>Démontrer.</strong> Les calculs de coût et les preuves, à refaire sur une feuille.</p></div>
    <div><p class="num">3</p><p><strong>Implémenter.</strong> Tu codes dans la page ; des tests vérifient, une mesure trace le coût réel.</p></div>
    <div><p class="num">4</p><p><strong>S'exercer.</strong> Exercices gradués, corrigés comme une copie, et un test de sortie.</p></div>
  </div>
  <p class="prog-txt" id="prog-globale" style="margin-top:14px"></p>
  <h2 class="sec">Les 10 modules</h2>
  <p>%s Les autres affichent déjà leur objectif, leurs prérequis et leur lien avec l'examen.
  Les étapes marquées <span class="pastille exam">examen</span> préparent directement une question d'annale.</p>
  <div class="mods">%s</div>
  <h2 class="sec">Les outils</h2>
  <div class="cartes">
    <a class="niv-card" href="calculateurs.html"><p class="k">Outil</p><h3>Calculateurs</h3>
      <p>Combien de temps pour n² ou 2ⁿ opérations ? Quelle taille traiter en une heure ? Combien coûte une attaque sur 128 bits ?</p></a>
    <a class="niv-card" href="module-9.html"><p class="k">Module 9</p><h3>Préparer l'examen</h3>
      <p>Ce que le correcteur attend, annales corrigées et évaluations chronométrées.</p></a>
  </div>
</main>
%s""" % (barre("index.html"), total,
     ("%d étape sur %d est rédigée." if redigees == 1 else "%d étapes sur %d sont rédigées.") % (redigees, total),
     "\n".join(cartes), pied())
    return coquille(SITE_LONG, body)


def page_calculateurs():
    vitesses = [("1000000", "10⁶ op/s — la machine du cours (10⁹ instructions/s, 1000 par opération)"),
                ("1000000000", "10⁹ op/s — un cœur de processeur actuel"),
                ("1000000000000", "10¹² op/s — une grosse grappe de calcul"),
                ("1000000000000000000", "10¹⁸ op/s — le plus puissant supercalculateur (exaflop)")]
    opts = "".join('<option value="%s">%s</option>' % v for v in vitesses)
    opts_att = "".join('<option value="%s"%s>%s</option>' % (v, ' selected' if i == 3 else '', t.replace("op/s", "clés/s"))
                       for i, (v, t) in enumerate(vitesses))
    rsa = "".join('<option value="%d"%s>%d bits</option>' % (b, ' selected' if b == 2048 else '', b)
                  for b in (1024, 2048, 3072, 7680, 15360))
    body = """%s
<main class="page-simple">
  <h1>Calculateurs</h1>
  <p>Trois outils pour sentir ce que veulent dire n², 2ⁿ ou 2¹²⁸. Les calculs supposent qu'un algorithme de
  complexité f(n) fait exactement f(n) opérations élémentaires : on néglige la constante, comme dans le cours.</p>

  <section class="cal" id="cal-temps">
    <h3>1. Combien de temps ?</h3>
    <p>Choisis la vitesse de la machine et jusqu'à cinq tailles d'entrée.</p>
    <div class="cal-ctrl">
      <label>Vitesse <select class="cal-vitesse">%s</select></label>
      <label>Tailles n <input class="cal-n" type="text" value="10, 100, 1000" inputmode="numeric"></label>
    </div>
    <div class="cal-sortie"></div>
    <p class="cal-note">Couleurs : vert, moins d'une seconde ; bleu, moins d'une heure ; orange, moins d'un an ; rouge, au-delà.
    Avec la vitesse du cours et n = 10, 100, 1000, tu retrouves le tableau comparatif du chapitre 1.</p>
  </section>

  <section class="cal" id="cal-taille">
    <h3>2. Quelle taille peut-on traiter ?</h3>
    <p>Le plus grand n que l'algorithme traite dans le temps donné. Observe la dernière ligne : passer d'une seconde à un siècle
    ne fait gagner que quelques unités à un algorithme exponentiel.</p>
    <div class="cal-ctrl"><label>Vitesse <select class="cal-vitesse">%s</select></label></div>
    <div class="cal-sortie"></div>
  </section>

  <section class="cal" id="cal-attaque">
    <h3>3. Le coût d'une attaque</h3>
    <p>Recherche exhaustive d'une clé de k bits : c'est la seule attaque générique contre un chiffrement symétrique comme AES.</p>
    <div class="cal-ctrl">
      <label>Taille de clé k <input class="cal-bits" type="number" min="1" max="512" value="128"> bits</label>
      <label>Vitesse <select class="cal-vitesse">%s</select></label>
    </div>
    <div class="cal-sortie"></div>
    <p style="margin-top:8px"><strong>Et pour RSA ?</strong> La meilleure attaque connue, le crible algébrique, est sous-exponentielle :
    son coût est</p>
    \\[L_N[1/3, c] = \\exp\\big((c+o(1))(\\ln N)^{1/3}(\\ln\\ln N)^{2/3}\\big), \\quad c = (64/9)^{1/3}.\\]
    <div class="cal-ctrl"><label>Taille du module N <select class="cal-rsa">%s</select></label></div>
    <div class="cal-sortie-rsa"></div>
  </section>
</main>
%s""" % (barre("calculateurs.html"), opts, opts, opts_att, rsa, pied())
    return coquille("Calculateurs — " + SITE_LONG, body, scripts=("calculateur.js",))


# ─────────────────────────────────────────────────────────────────────────────
def charger_contenu():
    n = 0
    for m in R.MODULES:
        nom = "module%d" % m.num
        if not os.path.exists(os.path.join(RACINE, "contenu", nom + ".py")):
            continue
        try:
            mod = importlib.import_module(nom)
        except Exception as err:
            raise SystemExit("Erreur dans contenu/%s.py : %s: %s" % (nom, type(err).__name__, err))
        for eid, texte in getattr(mod, "CORPS", {}).items():
            if eid not in R.INDEX:
                raise SystemExit("contenu/%s.py : étape inconnue %s" % (nom, eid))
            R.INDEX[eid][0].corps = texte
            n += 1
    return n


def copier_assets():
    a = os.path.join(PUBLIC, "assets")
    os.makedirs(a, exist_ok=True)
    with open(os.path.join(a, "style.css"), "w", encoding="utf-8") as f:
        for nom in ("style.css", "complexite.css"):
            f.write(open(os.path.join(MODELE, nom), encoding="utf-8").read() + "\n")
    for nom in ("site.js", "atelier.js", "atelier-worker.js", "animateur.js", "mesure.js",
                "calculateur.js", "outils.js"):
        shutil.copy(os.path.join(MODELE, nom), os.path.join(a, nom))
    os.makedirs(os.path.join(a, "mathjax"), exist_ok=True)
    shutil.copy(os.path.join(MODELE, "vendor", "tex-svg.js"), os.path.join(a, "mathjax", "tex-svg.js"))
    for dossier in ("fonts", "pyodide"):
        cible = os.path.join(a, dossier)
        if os.path.exists(cible):
            shutil.rmtree(cible)
        shutil.copytree(os.path.join(MODELE, "vendor", dossier), cible)


def verifier_videos():
    pbs = []
    for m in R.MODULES:
        for e in m.etapes:
            for v in re.findall(r'src="videos/([^"]+)"', e.corps or ""):
                if not os.path.exists(os.path.join(PUBLIC, "videos", v)):
                    pbs.append("%s : vidéo manquante videos/%s" % (e.id, v))
    return pbs


def construire():
    pbs = R.verifier()
    if pbs:
        print("Registre incohérent :\n  - " + "\n  - ".join(pbs))
        return 1
    charger_contenu()
    pbs = verifier_videos()
    if pbs:
        print("Vidéos :\n  - " + "\n  - ".join(pbs))
        return 1
    os.makedirs(os.path.join(PUBLIC, "videos"), exist_ok=True)
    copier_assets()
    open(os.path.join(PUBLIC, ".nojekyll"), "w").close()

    def ecrire(nom, contenu):
        with open(os.path.join(PUBLIC, nom), "w", encoding="utf-8") as f:
            f.write(contenu)
    ecrire("index.html", page_accueil())
    ecrire("calculateurs.html", page_calculateurs())
    for k, m in enumerate(R.MODULES):
        suivant = R.MODULES[k + 1].fichier if k + 1 < len(R.MODULES) else None
        ecrire(m.fichier, page_module(m, suivant))

    total = sum(len(m.etapes) for m in R.MODULES)
    red = sum(1 for m in R.MODULES for e in m.etapes if e.corps)
    print("Site construit dans docs/ : %d pages, %d étapes, %d rédigée(s) (%d %%)"
          % (len(R.MODULES) + 2, total, red, round(100 * red / total)))
    for m in R.MODULES:
        print("  module %d : %2d/%2d  %s" % (m.num, sum(1 for e in m.etapes if e.corps), len(m.etapes), m.titre))
    return 0


if __name__ == "__main__":
    sys.exit(construire())
