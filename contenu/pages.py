# -*- coding: utf-8 -*-
"""Les pages propres du parcours : l'accueil et les calculateurs.

Le moteur construit les pages des modules ; il appelle pages(site) pour les autres pages du site.
`site` donne le parcours (site.parcours), les réglages (site.reglages) et les morceaux communs :
site.coquille, site.barre, site.pied.
"""

import html


def pages(site):
    return {"index.html": page_accueil(site), "calculateurs.html": page_calculateurs(site)}


def page_accueil(site):
    total = sum(len(m.etapes) for m in site.parcours.parties)
    redigees = sum(1 for m in site.parcours.parties for e in m.etapes if e.publiee)
    cartes = []
    for m in site.parcours.parties:
        items = []
        for e in m.etapes:
            pas = ''
            if e.examen:
                pas = ' <span class="pastille exam">examen</span>'
            items.append('<li data-id="%s"%s><span class="n">%s</span><a href="%s#%s">%s</a>%s</li>'
                         % (e.id, ' class="redige"' if e.publiee else '', site.parcours.numero(e.id), m.fichier, e.id,
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
    calcul complet de T(n), atelier de code avec mesure, exercices et corrigé de l'exercice 2
    d'un vrai sujet d'examen du cours (session 2024-2025).</p>
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
  Les étapes marquées <span class="pastille exam">examen</span> préparent directement une question tirée
  d'un sujet d'examen réel de ce cours — utile même si tu prépares un autre examen : la méthode compte plus que l'énoncé.</p>
  <div class="mods">%s</div>
  <h2 class="sec">Les outils</h2>
  <div class="cartes">
    <a class="niv-card" href="calculateurs.html"><p class="k">Outil</p><h3>Calculateurs</h3>
      <p>Combien de temps pour n² ou 2ⁿ opérations ? Quelle taille traiter en une heure ? Combien coûte une attaque sur 128 bits ?</p></a>
    <a class="niv-card" href="module-9.html"><p class="k">Module 9</p><h3>Préparer l'examen</h3>
      <p>Ce que le correcteur attend, sujets d'examens corrigés et évaluations chronométrées.</p></a>
  </div>
</main>
%s""" % (site.barre("index.html"), total,
     ("%d étape sur %d est rédigée." if redigees == 1 else "%d étapes sur %d sont rédigées.") % (redigees, total),
     "\n".join(cartes), site.pied())
    return site.coquille(site.reglages.titre_long, body)


def page_calculateurs(site):
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
%s""" % (site.barre("calculateurs.html"), opts, opts, opts_att, rsa, site.pied())
    return site.coquille("Calculateurs — " + site.reglages.titre_long, body, scripts=("calculateur.js",))
