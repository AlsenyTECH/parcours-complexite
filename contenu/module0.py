# -*- coding: utf-8 -*-
"""Module 0 — Pourquoi la complexité.

0.1 Deux algorithmes, un même problème (recherche séquentielle et dichotomique)
0.2 Ce que coûte une attaque (recherche exhaustive de clé)
Valeurs numériques vérifiées par outils/verifier_module0.py.
"""

from briques import (retenir, prof, master, exercice, video, qcm, preuve, a_toi, a_retenir,
                     etape, atelier, examen, methode, animateur, mesure, tableau)

CORPS = {}

# ═════════════════════════════════════════════════════════════════════════════
# 0.1 Deux algorithmes, un même problème
# ═════════════════════════════════════════════════════════════════════════════

SEQ = """<pre class="pseudo tex2jax_ignore"><span class="num">1</span>Pour i = 1 à n
<span class="num">2</span>    si T[i] = x
<span class="num">3</span>        renvoyer Vrai
<span class="num">4</span>renvoyer Faux</pre>"""

DICHO = """<pre class="pseudo tex2jax_ignore"><span class="num">1</span>g = 1 ; d = n
<span class="num">2</span>tant que g ≤ d
<span class="num">3</span>    m = ⌊(g + d) / 2⌋
<span class="num">4</span>    si T[m] = x : renvoyer Vrai
<span class="num">5</span>    si T[m] &lt; x : g = m + 1
<span class="num">6</span>    sinon : d = m − 1
<span class="num">7</span>renvoyer Faux</pre>"""

TAB10 = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

E01 = qcm("entree", [
    (r"Dans un tableau trié de \(10^6\) valeurs, combien de comparaisons faut-il au plus à la recherche dichotomique ?",
     [r"\(10^6\)", r"\(1000\)", r"\(20\)", r"\(6\)"], 2,
     r"\(\lfloor \log_2 10^6 \rfloor + 1 = 19 + 1 = 20\), car \(2^{19} \le 10^6 < 2^{20}\)."),
    (r"La recherche dichotomique fonctionne-t-elle sur un tableau non trié ?",
     [r"Oui, toujours", r"Non : elle suppose le tableau trié", r"Oui, si \(n\) est pair", r"Oui, mais plus lentement"], 1,
     r"Éliminer une moitié n'est légitime que si l'ordre dit de quel côté se trouve \(x\)."),
    (r"Si \(n\) double, le nombre maximal de comparaisons de la dichotomie…",
     [r"double", r"augmente de 1", r"est multiplié par 4", r"ne change pas"], 1,
     r"\(\lfloor \log_2 (2n) \rfloor = \lfloor \log_2 n \rfloor + 1\) : un tour de plus suffit à couper le tableau doublé."),
])

C01 = r"""
<p class="lead">Tu cherches un mot dans un dictionnaire de 60 000 pages. Personne ne le lit page par page : on l'ouvre au milieu,
on regarde si le mot est avant ou après, et on recommence dans la bonne moitié. Deux méthodes justes, mais l'une demande
60 000 coups d'œil et l'autre environ 16. Toute la complexité des algorithmes est dans cet écart.</p>
""" + video("m0-deux-algos.mp4", "Un million de cases, vingt comparaisons", "1 min 20") + r"""

<h3>Le problème</h3>
<p>On dispose d'un tableau \(T[1..n]\) et d'une valeur \(x\). Question : <strong>\(x\) est-il dans \(T\) ?</strong>
On mesure le travail en <em>comparaisons</em> entre \(x\) et une case du tableau : c'est l'opération qu'on répète.</p>

<h3>Première idée : regarder toutes les cases</h3>
""" + SEQ + r"""
<p>C'est la <strong>recherche séquentielle</strong>. Elle marche sur n'importe quel tableau, trié ou non.
Si \(x\) est absent, elle compare \(x\) à chacune des \(n\) cases avant de répondre Faux.</p>
""" + animateur("anim-seq", "sequentielle", [
    ["x = 23 (présent)", TAB10, 23],
    ["x = 91 (dernière case)", TAB10, 91],
    ["x = 40 (absent)", TAB10, 40],
], "la recherche séquentielle") + r"""

<h3>Deuxième idée : couper en deux</h3>
<p>Si le tableau est <strong>trié</strong>, comparer \(x\) à la case du milieu \(T[m]\) apprend beaucoup plus qu'une case :
si \(T[m] < x\), alors \(x\) ne peut pas être dans \(T[1..m]\), puisque toutes ces cases sont \(\le T[m]\).
On élimine la moitié du tableau d'un seul coup. On garde une zone de recherche \(T[g..d]\) qui rétrécit.</p>
""" + DICHO + animateur("anim-dicho", "dichotomie", [
    ["x = 23 (présent)", TAB10, 23],
    ["x = 91 (dernière case)", TAB10, 91],
    ["x = 40 (absent)", TAB10, 40],
], "la recherche dichotomique") + r"""

<p>Sur le même tableau de 10 cases, pour \(x = 40\) absent : 10 comparaisons d'un côté, 4 de l'autre. L'écart paraît modeste.
Il devient vertigineux quand \(n\) grandit :</p>
""" + tableau(["Taille \\(n\\)", "Séquentielle (pire cas)", "Dichotomique (pire cas)", "Temps à 1 µs la comparaison"], [
    ["\\(10\\)", "10", "4", "10 µs contre 4 µs"],
    ["\\(1\\,000\\)", "1 000", "10", "1 ms contre 10 µs"],
    ["\\(10^6\\)", "1 000 000", "20", "1 s contre 20 µs"],
    ["\\(10^9\\)", "1 000 000 000", "30", "17 min contre 30 µs"],
]) + prof(r"""<p>Remarque ce qui se passe quand \(n\) est multiplié par 1000 : la recherche séquentielle devient 1000 fois plus lente,
la dichotomique ne fait que 10 comparaisons de plus. Ce n'est pas le nombre de comparaisons pour un \(n\) donné qui compte,
c'est <strong>la façon dont il grandit avec \(n\)</strong>. C'est exactement ce que mesure la complexité.</p>""") + a_toi(
r"""<p>Fais tourner la dichotomie à la main sur le tableau ci-dessus (\(2, 5, 8, 12, 16, 23, 38, 56, 72, 91\)) pour \(x = 2\).
Donne à chaque tour les valeurs de \(g\), \(d\) et \(m\). Combien de tours ?</p>""",
tableau(["Tour", "g", "d", "m", "T[m]", "Décision"], [
    ["1", "1", "10", "5", "16", "16 > 2 : d = 4"],
    ["2", "1", "4", "2", "5", "5 > 2 : d = 1"],
    ["3", "1", "1", "1", "2", "trouvé"]]) + "<p>Trois tours. Vérifie avec l'animateur : tape <code>2, 5, 8, 12, 16, 23, 38, 56, 72, 91 ; 2</code>.</p>")

D01 = r"""
<p class="lead">On établit les deux nombres du tableau : \(n\) comparaisons au pire pour la recherche séquentielle,
\(\lfloor \log_2 n \rfloor + 1\) pour la dichotomique. La preuve complète et le cas moyen viendront aux étapes 3.2 et 3.6 ;
ici, on retient l'argument.</p>
""" + preuve("Proposition (recherche séquentielle)",
    r"""<p>La recherche séquentielle fait au plus \(n\) comparaisons, et exactement \(n\) quand \(x\) est absent
    ou seulement dans la dernière case. Au mieux (\(x = T[1]\)), elle en fait une.</p>""",
    r"""Chaque tour de boucle fait une comparaison et avance d'une case ; il y a au plus \(n\) cases.""",
    [r"Combien de tours de boucle au plus ?", r"Quand la boucle va-t-elle jusqu'au bout ?"],
    r"""<p>La ligne 2 est exécutée une fois par valeur de \(i\) atteinte, et \(i\) prend au plus les valeurs \(1, \dots, n\) : au plus \(n\) comparaisons.
    Si \(x\) est absent, aucune comparaison n'arrête la boucle : les \(n\) sont faites. Si \(x\) n'apparaît qu'en \(T[n]\), la dernière
    comparaison réussit : encore \(n\). Si \(T[1] = x\), la première suffit.</p>""") + preuve("Proposition (recherche dichotomique)",
    r"""<p>Sur un tableau trié de taille \(n \ge 1\), la recherche dichotomique fait au plus \(\lfloor \log_2 n \rfloor + 1\) tours de boucle,
    donc au plus \(\lfloor \log_2 n \rfloor + 1\) comparaisons de \(x\) avec un milieu.</p>""",
    r"""À chaque tour, la zone de recherche est au moins divisée par deux ; or on ne peut diviser \(n\) par deux qu'environ \(\log_2 n\) fois avant d'arriver à moins d'une case.""",
    [r"Notons \(L = d - g + 1\) la taille de la zone au début d'un tour. Montre que la zone suivante a au plus \(\lfloor L/2 \rfloor\) cases.",
     r"Déduis-en que la taille au début du tour \(k+1\) est au plus \(\lfloor n / 2^k \rfloor\).",
     r"Le tour \(k+1\) n'a lieu que si cette taille vaut au moins 1. Conclus."],
    r"""<p><strong>Une zone divisée par deux.</strong> Au début d'un tour, la zone \(T[g..d]\) a \(L = d - g + 1 \ge 1\) cases, et
    \(m = \lfloor (g+d)/2 \rfloor\). Si l'on continue à gauche, la nouvelle zone \(T[g..m-1]\) a \(m - g\) cases ; à droite, \(T[m+1..d]\)
    en a \(d - m\). Or \(m - g \le \frac{d - g}{2} = \frac{L - 1}{2}\) et \(d - m \le d - \frac{g + d - 1}{2} = \frac{L}{2}\). Les deux sont des entiers
    \(\le L/2\), donc \(\le \lfloor L/2 \rfloor\).</p>
    <p><strong>Après \(k\) tours.</strong> Notons \(L_k\) la taille de la zone au début du tour \(k+1\). On a \(L_0 = n\) et \(L_{k+1} \le \lfloor L_k / 2 \rfloor\).
    Par récurrence, \(L_k \le \lfloor n / 2^k \rfloor\), car \(\lfloor \lfloor a \rfloor / 2 \rfloor = \lfloor a/2 \rfloor\) pour tout réel \(a \ge 0\).</p>
    <p><strong>Conclusion.</strong> Le tour \(k+1\) n'a lieu que si \(L_k \ge 1\), donc si \(n / 2^k \ge 1\), c'est-à-dire \(k \le \log_2 n\), soit
    \(k \le \lfloor \log_2 n \rfloor\) puisque \(k\) est entier. Les tours ont donc des numéros \(k + 1 \le \lfloor \log_2 n \rfloor + 1\).</p>""") + r"""
<p>La borne est atteinte : quand \(x\) est plus grand que toutes les valeurs, la dichotomie fait exactement \(\lfloor \log_2 n \rfloor + 1\) tours
(tu le vérifieras dans l'atelier). Pour \(n = 10^6\), comme \(2^{19} = 524\,288 \le 10^6 < 2^{20} = 1\,048\,576\), cela fait 20.</p>
""" + retenir("Ce qu'il faut retenir de l'écart", r"""<p>Recherche séquentielle : coût qui grandit comme \(n\). Recherche dichotomique : coût qui grandit comme \(\log_2 n\).
On écrira plus tard \(\Theta(n)\) et \(\Theta(\log n)\) (module 2). Doubler \(n\) double le premier, et n'ajoute qu'une comparaison au second.</p>""") + r"""
<h3>Mais rien n'est gratuit</h3>
<p>La dichotomie exige un tableau <strong>trié</strong>. Trier coûte (au mieux de l'ordre de \(n \log n\) comparaisons, module 4).
Le bon choix dépend donc de l'usage :</p>
<ul><li>une seule recherche dans des données en vrac : la recherche séquentielle (\(n\) comparaisons) bat « trier puis chercher » ;</li>
<li>beaucoup de recherches dans les mêmes données : on trie une fois, et chaque recherche ne coûte plus que \(\log_2 n\).</li></ul>
""" + master(r"""<p>Ce même partage « trier une fois, chercher vite ensuite » est au cœur de l'attaque <em>pas de bébé, pas de géant</em>
contre le logarithme discret (étape 7.3) : on range \(\sqrt q\) valeurs dans une table triée, puis chaque recherche coûte \(\log q\).
C'est ce qui fait tomber le coût d'une attaque sur Diffie-Hellman de \(q\) à environ \(\sqrt q\) opérations.</p>""")

I01 = r"""
<p class="lead">Écris les deux recherches en Python, en comptant les comparaisons. Puis lance-les sur des tableaux de 1 000 à 100 000 cases.</p>
""" + prof(r"""<p>En Python les indices vont de 0 à \(n-1\) : la dichotomie démarre avec <code>g, d = 0, len(T) - 1</code>,
et <code>m = (g + d) // 2</code>. Compte <strong>un</strong> par tour de boucle pour la dichotomie (on compare \(x\) au milieu).</p>""") + atelier(
    "recherches",
    r"""<p>Complète les deux fonctions. Chacune renvoie le couple <code>(trouve, nb_comparaisons)</code>, où <code>trouve</code> est un booléen.</p>""",
    '''def recherche_seq(T, x):
    """Renvoie (x est dans T, nombre de comparaisons T[i] == x effectuées)."""
    nb = 0
    for v in T:
        pass  # À toi
    return False, nb


def dichotomie(T, x):
    """T est trié. Renvoie (x est dans T, nombre de tours de boucle)."""
    g, d = 0, len(T) - 1
    nb = 0
    # À toi
    return False, nb


T = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(recherche_seq(T, 40), dichotomie(T, 40))
''',
    [
        {"appel": "recherche_seq([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23)", "verif": "r == (True, 6)", "attendu": "(True, 6)"},
        {"appel": "recherche_seq([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 40)", "verif": "r == (False, 10)", "attendu": "(False, 10) : x absent, toutes les cases"},
        {"appel": "recherche_seq([], 1)", "verif": "r == (False, 0)", "attendu": "(False, 0)"},
        {"appel": "recherche_seq([7, 3, 9], 7)", "verif": "r == (True, 1)", "attendu": "(True, 1) : le meilleur cas"},
        {"appel": "dichotomie([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23)", "verif": "r == (True, 3)", "attendu": "(True, 3)"},
        {"appel": "dichotomie([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 40)", "verif": "r == (False, 4)", "attendu": "(False, 4)"},
        {"appel": "dichotomie([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 2)", "verif": "r == (True, 3)", "attendu": "(True, 3)"},
        {"appel": "dichotomie([], 1)", "verif": "r == (False, 0)", "attendu": "(False, 0)"},
        {"appel": "dichotomie(list(range(10**6)), 10**6)", "verif": "r == (False, 20)", "attendu": "(False, 20) : un million de cases, 20 tours"},
        {"appel": "all(dichotomie(list(range(0, 200, 2)), v)[0] == (v % 2 == 0 and 0 <= v < 200) for v in range(-3, 203))",
         "verif": "r is True", "attendu": "True : la bonne réponse pour toutes les valeurs de −3 à 202"},
    ],
    r"""<pre class="pseudo">def recherche_seq(T, x):
    nb = 0
    for v in T:
        nb += 1
        if v == x:
            return True, nb
    return False, nb


def dichotomie(T, x):
    g, d = 0, len(T) - 1
    nb = 0
    while g &lt;= d:
        nb += 1
        m = (g + d) // 2
        if T[m] == x:
            return True, nb
        if T[m] &lt; x:
            g = m + 1
        else:
            d = m - 1
    return False, nb</pre>""") + r"""
<h3>Mesurer</h3>
""" + mesure("recherches",
    r"""<p>Les deux recherches, au pire cas (\(x\) absent et plus grand que tout), sur des tableaux triés de 1 000 à 100 000 cases.
    Regarde la courbe verte : elle reste collée à l'axe.</p>""",
    "recherche_seq", [1000, 5000, 10000, 25000, 50000, 75000, 100000],
    [["n", "n"]],
    [{"nom": "séquentielle, x absent", "court": "séquentielle", "expr": "(list(range(n)), n)", "couleur": "pire", "fonction": "recherche_seq"},
     {"nom": "dichotomique, x absent", "court": "dichotomique", "expr": "(list(range(n)), n)", "couleur": "meilleur", "fonction": "dichotomie"}],
    [["séq. / n", 0, "n"], ["dicho. / log₂ n", 1, "Math.log2(n)"]],
    "taille n du tableau") + prof(r"""<p>La colonne « séq. / n » vaut exactement 1 : le coût est proportionnel à \(n\). La colonne « dicho. / log₂ n »
se stabilise un peu au-dessus de 1 : le coût est proportionnel à \(\log_2 n\). Pour 100 000 cases : 100 000 comparaisons contre 17.</p>""")

X01 = r"""
<p class="lead">Des calculs de taille, puis des situations où il faut choisir.</p>
""" + exercice(1, "★", r"""<p>Combien de comparaisons fait au plus la recherche dichotomique dans un tableau trié de \(n = 1000\) valeurs ? De \(n = 1024\) ? De \(n = 8 \times 10^9\)
(une valeur par habitant de la planète) ?</p>""",
r"""<p>Encadre \(n\) entre deux puissances de 2 consécutives.</p>""",
r"""<p>\(2^9 = 512 \le 1000 < 1024 = 2^{10}\), donc \(\lfloor \log_2 1000 \rfloor = 9\) et la borne vaut \(10\).</p>
<p>\(n = 1024 = 2^{10}\) : \(\lfloor \log_2 1024 \rfloor = 10\), borne \(11\). Une case de plus que 1000 peut coûter un tour de plus.</p>
<p>\(2^{32} \approx 4{,}3 \times 10^9 \le 8 \times 10^9 < 2^{33} \approx 8{,}6 \times 10^9\), donc la borne vaut \(33\).
Trente-trois questions suffisent pour retrouver un habitant de la Terre dans un annuaire trié.</p>""") + exercice(2, "★", r"""<p><strong>Le jeu du nombre.</strong> Je pense à un entier entre 1 et 100. Tu proposes un nombre, je réponds « plus grand », « plus petit » ou « gagné ».</p>
<ol><li>Quelle stratégie garantit de gagner en au plus 7 propositions ?</li><li>Pourquoi est-il impossible de garantir 6 ?</li></ol>""",
r"""<p>Pour la question 2, compte combien de nombres différents une stratégie peut « atteindre » en 6 propositions.</p>""",
r"""<p><strong>1.</strong> La dichotomie : proposer le milieu de l'intervalle restant. Avec \(n = 100\), \(\lfloor \log_2 100 \rfloor + 1 = 6 + 1 = 7\) propositions au plus.</p>
<p><strong>2.</strong> Une stratégie déterministe propose un premier nombre ; selon la réponse (plus grand / plus petit), elle en propose un deuxième, et ainsi de suite.
Le nombre de propositions différentes possibles à la \(k\)-ième question est au plus \(2^{k-1}\). En 6 questions, la stratégie peut donc nommer au plus
\(1 + 2 + 4 + 8 + 16 + 32 = 63\) nombres différents. Or il y en a 100 : pour au moins un nombre secret, elle ne l'aura pas proposé. Il faut donc au moins 7 questions.</p>""",
r"""<p>Cet argument (un arbre de décision binaire de profondeur \(k\) a au plus \(2^k - 1\) nœuds) montre que la dichotomie est <strong>optimale</strong> :
aucun algorithme fondé sur des comparaisons ne fait mieux au pire cas. On le retrouvera pour le tri (\(\Omega(n \log n)\), module 4).</p>""") + exercice(3, "★★", r"""<p>On doit répondre à \(q\) recherches dans un tableau non trié de taille \(n = 10^6\). Option A : \(q\) recherches séquentielles.
Option B : trier d'abord (on compte \(n \log_2 n\) comparaisons), puis \(q\) recherches dichotomiques. On compte les comparaisons au pire cas.
À partir de quelle valeur de \(q\) l'option B devient-elle plus avantageuse ?</p>""",
r"""<p>Écris le coût des deux options en fonction de \(q\), avec \(\log_2 10^6 \approx 20\).</p>""",
r"""<p>Option A : \(q \cdot n = 10^6 q\). Option B : \(n \log_2 n + q(\lfloor \log_2 n \rfloor + 1) \approx 2 \times 10^7 + 20q\).</p>
<p>B est meilleure dès que \(10^6 q > 2 \times 10^7 + 20 q\), soit \(q(10^6 - 20) > 2 \times 10^7\), donc \(q > 20{,}0004\) : à partir de \(q = 21\) recherches.
Le tri se rentabilise très vite : au-delà d'une vingtaine de recherches, on a intérêt à trier.</p>""") + exercice(4, "★★", r"""<p>Un collègue propose une « trichotomie » : comparer \(x\) aux cases situées au tiers et aux deux tiers, et garder un seul des trois morceaux.
Elle fait au plus 2 comparaisons par tour et réduit la zone à environ \(n/3\). Est-ce mieux que la dichotomie ?</p>""",
r"""<p>Compare \(2 \log_3 n\) et \(\log_2 n\).</p>""",
r"""<p>Au pire cas, la trichotomie fait environ \(\log_3 n\) tours de 2 comparaisons, soit \(2 \log_3 n = \frac{2}{\log_2 3} \log_2 n \approx 1{,}26 \log_2 n\) comparaisons.
C'est environ 26 % de plus que la dichotomie. Diviser en plus de morceaux réduit le nombre de tours, mais chaque tour coûte plus cher : la dichotomie est meilleure,
conformément à l'optimalité vue à l'exercice 2.</p>""")

S01 = qcm("sortie", [
    (r"La recherche séquentielle d'un élément absent dans un tableau de taille \(n\) fait :",
     [r"\(1\) comparaison", r"\(n/2\) comparaisons", r"\(n\) comparaisons", r"\(\log_2 n\) comparaisons"], 2, r"Il faut avoir regardé chaque case pour affirmer que \(x\) est absent."),
    (r"Au pire cas, la dichotomie sur \(n = 1000\) cases fait :",
     [r"\(9\) tours", r"\(10\) tours", r"\(500\) tours", r"\(1000\) tours"], 1, r"\(2^9 \le 1000 < 2^{10}\) : \(\lfloor \log_2 1000 \rfloor + 1 = 10\)."),
    (r"Quelle hypothèse est indispensable à la dichotomie ?",
     [r"\(n\) est une puissance de 2", r"Les valeurs sont distinctes", r"Le tableau est trié", r"\(x\) est dans le tableau"], 2, r"C'est l'ordre qui permet d'éliminer une moitié."),
    (r"Le nombre de comparaisons de la dichotomie grandit comme :",
     [r"\(n\)", r"\(\sqrt n\)", r"\(\log_2 n\)", r"\(n \log_2 n\)"], 2, r"Chaque tour divise la zone par deux : \(\lfloor \log_2 n \rfloor + 1\) tours au plus."),
    (r"Pour une <em>seule</em> recherche dans un grand tableau non trié, le plus économe est :",
     [r"Trier puis faire une dichotomie", r"Faire une recherche séquentielle", r"Les deux se valent", r"Faire une dichotomie directement"], 1,
     r"Trier coûte déjà de l'ordre de \(n \log n\), plus que les \(n\) comparaisons de la recherche séquentielle."),
])

R01 = a_retenir([
    r"On mesure un algorithme par le nombre d'opérations répétées (ici des comparaisons), <strong>en fonction de la taille \(n\)</strong> de l'entrée.",
    r"Recherche séquentielle : au plus \(n\) comparaisons ; marche sur tout tableau.",
    r"Recherche dichotomique : au plus \(\lfloor \log_2 n \rfloor + 1\) comparaisons ; exige un tableau trié.",
    r"Ce qui compte n'est pas la valeur pour un \(n\) précis, mais la vitesse de croissance : \(n\) contre \(\log_2 n\).",
])

CORPS["m0-deux-algos"] = etape(E01, C01, D01, I01, X01, S01, R01)


# ═════════════════════════════════════════════════════════════════════════════
# 0.2 Ce que coûte une attaque
# ═════════════════════════════════════════════════════════════════════════════

E02 = qcm("entree", [
    (r"Combien y a-t-il de clés de 56 bits ?",
     [r"\(56\)", r"\(56^2\)", r"\(2^{56}\)", r"\(10^{56}\)"], 2, r"Chacun des 56 bits vaut 0 ou 1 : \(2 \times 2 \times \dots \times 2 = 2^{56}\) clés."),
    (r"Ajouter 1 bit à une clé multiplie le temps de la recherche exhaustive par :",
     [r"\(1\)", r"\(2\)", r"\(10\)", r"\(56\)"], 1, r"\(2^{k+1} = 2 \times 2^k\)."),
    (r"En moyenne, une recherche exhaustive sur \(2^k\) clés essaie environ :",
     [r"\(k\) clés", r"\(2^{k-1}\) clés", r"\(2^k\) clés", r"\(k^2\) clés"], 1, r"La bonne clé est en moyenne au milieu de la liste : \(\frac{2^k + 1}{2}\) essais."),
])

C02 = r"""
<p class="lead">Un chiffrement symétrique (AES, DES…) est public : tout le monde connaît l'algorithme. Seule la <strong>clé</strong> est secrète.
Un attaquant qui possède un message clair et son chiffré peut toujours essayer toutes les clés une à une. Cette attaque marche contre
<em>tous</em> les chiffrements ; la seule défense est de rendre son coût astronomique. Combien de bits faut-il pour cela ?</p>
""" + video("m0-attaque.mp4", "Pourquoi 128 bits suffisent", "1 min 13") + r"""

<h3>La recherche exhaustive</h3>
<pre class="pseudo tex2jax_ignore"><span class="num">1</span>Pour k = 0 à 2^b − 1          ▹ toutes les clés de b bits
<span class="num">2</span>    si Chiffrer(m, k) = c
<span class="num">3</span>        renvoyer k
<span class="num">4</span>renvoyer « aucune clé »</pre>
<p>C'est exactement la recherche séquentielle de l'étape 0.1 : on cherche, parmi \(N = 2^b\) clés, celle qui transforme \(m\) en \(c\).
Son coût est donc proportionnel à \(N = 2^b\), c'est-à-dire <strong>exponentiel en la taille de la clé</strong>. Voilà tout le secret :
la taille de l'entrée de l'attaquant, c'est \(b\) bits, et son travail est \(2^b\).</p>

""" + retenir("Le prix d'un bit", r"""<p>Chaque bit de clé supplémentaire <strong>double</strong> le nombre de clés, donc le temps de l'attaque.
Dix bits de plus multiplient le temps par \(2^{10} = 1024 \approx 1000\).</p>""") + r"""

<h3>Les ordres de grandeur</h3>
<p>Temps <strong>moyen</strong> d'une recherche exhaustive (la moitié des clés), selon la vitesse de l'attaquant :</p>
""" + tableau(["Taille de clé", "Nombre de clés", "à \\(10^9\\) clés/s (un PC)", "à \\(10^{12}\\) clés/s (une grappe)", "à \\(10^{18}\\) clés/s (un supercalculateur)"], [
    ["40 bits", "\\(1{,}1 \\times 10^{12}\\)", "9 min", "0,55 s", "0,55 µs"],
    ["56 bits (DES)", "\\(7{,}2 \\times 10^{16}\\)", "1,1 an", "10 h", "0,04 s"],
    ["64 bits", "\\(1{,}8 \\times 10^{19}\\)", "292 ans", "107 jours", "9 s"],
    ["80 bits", "\\(1{,}2 \\times 10^{24}\\)", "19 millions d'années", "19 000 ans", "7 jours"],
    ["128 bits (AES)", "\\(3{,}4 \\times 10^{38}\\)", "\\(5 \\times 10^{21}\\) ans", "\\(5 \\times 10^{18}\\) ans", "\\(5 \\times 10^{12}\\) ans"],
]) + r"""
<p>L'Univers a environ \(1{,}4 \times 10^{10}\) ans. Contre AES-128, même le plus gros supercalculateur aurait besoin de plusieurs centaines de fois l'âge de l'Univers.
Joue avec ces nombres dans les <a href="calculateurs.html#cal-attaque">calculateurs</a>.</p>
""" + master(r"""<p>DES, le standard américain de 1977, avait des clés de 56 bits. En 1998, une machine spécialisée construite par l'Electronic Frontier Foundation
a retrouvé une clé DES par recherche exhaustive en quelques jours. C'est la ligne « 56 bits » du tableau qui s'est réalisée : DES a été remplacé
par AES (2001), dont les clés font 128, 192 ou 256 bits.</p>""")

D02 = r"""
<p class="lead">Deux résultats précis : le nombre moyen d'essais, et ce que vaut un gain de vitesse face à un bit de clé.</p>
""" + preuve("Proposition (nombre d'essais)",
    r"""<p>On essaie les \(N = 2^b\) clés dans un ordre fixé, et la clé secrète est choisie uniformément au hasard. Alors le nombre d'essais
    vaut au pire \(N\), et en moyenne \(\dfrac{N + 1}{2}\).</p>""",
    r"""Si la clé est la \(i\)-ième de la liste, il faut exactement \(i\) essais ; chaque position a la probabilité \(1/N\).""",
    [r"Combien d'essais si la clé secrète est la \(i\)-ième essayée ?", r"Quelle est la probabilité de chaque position ?", r"Calcule l'espérance avec \(\sum_{i=1}^N i = \frac{N(N+1)}{2}\)."],
    r"""<p>Si la clé secrète est la \(i\)-ième de la liste (\(1 \le i \le N\)), l'algorithme fait \(i\) essais : les \(i - 1\) premiers échouent, le \(i\)-ième réussit.
    Le pire cas est \(i = N\). La clé étant uniforme, chaque position a la probabilité \(1/N\), d'où
    \[ \mathbb{E}[\text{essais}] = \sum_{i=1}^{N} i \cdot \frac1N = \frac1N \cdot \frac{N(N+1)}{2} = \frac{N+1}{2}. \]
    Pour \(N = 2^b\), c'est \(2^{b-1} + \frac12\) : environ la moitié des clés.</p>""") + preuve("Proposition (vitesse contre bits)",
    r"""<p>Multiplier la puissance de l'attaquant par \(2^a\) (machines plus rapides, ou \(2^a\) machines en parallèle) a exactement le même effet
    que retirer \(a\) bits à la clé.</p>""",
    r"""Le temps est \(\frac{2^{b-1}}{v}\) : \(\frac{2^{b-1}}{2^a v} = \frac{2^{(b-a)-1}}{v}\).""",
    [r"Écris le temps moyen \(t(b, v)\) en fonction de la taille \(b\) et de la vitesse \(v\).", r"Compare \(t(b, 2^a v)\) et \(t(b - a, v)\)."],
    r"""<p>Le temps moyen est \(t(b, v) \approx \frac{2^{b-1}}{v}\). Alors \(t(b, 2^a v) = \frac{2^{b-1}}{2^a v} = \frac{2^{(b-a)-1}}{v} = t(b - a, v)\).</p>
    <p>Conséquence : la défense gagne toujours la course. Si la puissance de calcul double tous les deux ans, l'attaquant gagne un bit tous les deux ans.
    En 40 ans, 20 bits. Passer de 80 à 128 bits met 48 bits d'avance, soit environ un siècle de progrès.</p>""") + examen(r"""<p>Dans un exercice de dimensionnement, rédige toujours dans cet ordre : nombre de clés \(2^b\) ; nombre moyen d'essais \(2^{b-1}\) ;
temps \(= 2^{b-1} / v\) en secondes ; conversion en années (\(1 \text{ an} \approx 3{,}16 \times 10^7\) s). Les ordres de grandeur suffisent :
\(2^{10} \approx 10^3\), donc \(2^{b} \approx 10^{0{,}3 b}\).</p>""")

I02 = r"""
<p class="lead">Tu vas attaquer un chiffrement jouet sur 32 bits avec des clés courtes, puis mesurer le nombre d'essais quand la clé grandit d'un bit.</p>
""" + atelier(
    "attaque",
    r"""<p>La fonction <code>chiffrer(m, k)</code> est donnée (ne la modifie pas). Écris <code>attaque(m, c, b)</code> qui essaie les clés
    \(k = 0, 1, \dots, 2^b - 1\) <strong>dans l'ordre</strong> et renvoie le couple <code>(k, nb_essais)</code> pour la première clé telle que
    <code>chiffrer(m, k) == c</code>, ou <code>(None, nb_essais)</code> si aucune ne convient.</p>""",
    '''def chiffrer(m, k):
    """Chiffrement jouet : message m sur 32 bits, clé k entière. (Ne pas modifier.)"""
    x = (m ^ (k * 0x9E3779B1)) & 0xFFFFFFFF
    x = (x * 0x85EBCA6B + k) & 0xFFFFFFFF
    return x ^ (x >> 13)


def attaque(m, c, b):
    """Essaie toutes les clés de b bits ; renvoie (clé trouvée ou None, nombre d'essais)."""
    nb = 0
    # À toi
    return None, nb


c = chiffrer(2026, 1000)
print(attaque(2026, c, 12))
''',
    [
        {"appel": "attaque(2026, chiffrer(2026, 7), 8)", "verif": "r == (7, 8)", "attendu": "(7, 8) : la clé 7 est la 8e essayée"},
        {"appel": "attaque(2026, chiffrer(2026, 0), 8)", "verif": "r == (0, 1)", "attendu": "(0, 1) : le meilleur cas"},
        {"appel": "attaque(2026, chiffrer(2026, 255), 8)", "verif": "r == (255, 256)", "attendu": "(255, 256) : le pire cas, toutes les clés"},
        {"appel": "attaque(2026, chiffrer(2026, 1000), 12)", "verif": "r == (1000, 1001)", "attendu": "(1000, 1001)"},
        {"appel": "attaque(2026, chiffrer(2026, 300), 8)", "verif": "r == (None, 256)", "attendu": "(None, 256) : la clé 300 ne tient pas sur 8 bits"},
        {"appel": "attaque(2026, chiffrer(2026, 40000), 16)", "verif": "r == (40000, 40001)", "attendu": "(40000, 40001)"},
    ],
    r"""<pre class="pseudo">def attaque(m, c, b):
    nb = 0
    for k in range(2 ** b):
        nb += 1
        if chiffrer(m, k) == c:
            return k, nb
    return None, nb</pre>""") + r"""
<h3>Mesurer : un bit de plus, deux fois plus d'essais</h3>
""" + mesure("attaque",
    r"""<p>On lance ton attaque pour des clés de 4 à 14 bits : au pire cas (la dernière clé) et pour des clés tirées au hasard (moyenne de 20).
    En pointillés : \(2^b\) et \(\frac{2^b + 1}{2}\).</p>""",
    "attaque", [4, 6, 8, 9, 10, 11, 12, 13, 14],
    [["2^b", "Math.pow(2, n)"], ["(2^b + 1)/2", "(Math.pow(2, n) + 1) / 2"]],
    [{"nom": "pire cas (dernière clé)", "court": "pire", "expr": "(2026, chiffrer(2026, 2**n - 1), n)", "couleur": "pire"},
     {"nom": "clé au hasard (moyenne de 20)", "court": "moyen", "expr": "(2026, chiffrer(2026, random.randrange(2**n)), n)", "couleur": "moyen", "essais": 20}],
    [["pire / 2^b", 0, "Math.pow(2, n)"], ["moyen / 2^b", 1, "Math.pow(2, n)"]],
    "taille de clé b (bits)") + prof(r"""<p>À chaque bit de plus, la courbe rouge double : c'est la forme d'une exponentielle. La colonne « moyen / 2^b » tourne autour de 0,5,
avec des écarts dus au hasard. Ton navigateur fait de l'ordre d'un million d'essais par seconde : à ce rythme, essayer toutes les clés de 40 bits
prendrait environ deux semaines, et toutes celles de 128 bits \(10^{25}\) ans.</p>""")

X02 = r"""
<p class="lead">Des dimensionnements réalistes. Convertis toujours avec \(1 \text{ an} \approx 3{,}16 \times 10^7\) s et \(2^{10} \approx 10^3\).</p>
""" + exercice(1, "★", r"""<p>Un attaquant dispose d'une grappe qui teste \(10^{12}\) clés DES par seconde. Combien de temps lui faut-il en moyenne pour retrouver une clé de 56 bits ?</p>""",
r"""<p>En moyenne : \(2^{55}\) essais.</p>""",
r"""<p>\(2^{55} \approx 3{,}6 \times 10^{16}\) essais, donc \(t \approx \frac{3{,}6 \times 10^{16}}{10^{12}} = 3{,}6 \times 10^4\) s, soit environ <strong>10 heures</strong>.
Une clé DES ne protège plus rien contre un attaquant équipé.</p>""") + exercice(2, "★★", r"""<p>On veut qu'un attaquant capable de tester \(10^{21}\) clés par seconde (l'ordre de grandeur de la puissance de calcul
de tout le réseau Bitcoin) mette en moyenne au moins 1000 ans. Quelle taille de clé minimale faut-il ?</p>""",
r"""<p>Écris \(2^{b-1} \ge v \cdot t\) et passe au \(\log_2\).</p>""",
r"""<p>Il faut \(2^{b-1} \ge 10^{21} \times 1000 \times 3{,}16 \times 10^7 \approx 3{,}2 \times 10^{31}\).
Or \(\log_2(3{,}2 \times 10^{31}) \approx 104{,}6\), donc \(b - 1 \ge 104{,}6\), soit \(b \ge 106\) bits.
Les 128 bits d'AES laissent une marge de plus de 20 bits, c'est-à-dire un facteur supérieur à un million.</p>""") + exercice(3, "★★", r"""<p><strong>Mots de passe.</strong> Un attaquant qui a volé une base de mots de passe hachés teste \(10^{10}\) mots de passe par seconde avec une carte graphique.</p>
<ol><li>Combien de temps lui faut-il, au pire, pour un mot de passe de 8 lettres minuscules ?</li>
<li>Et pour un mot de passe de 12 caractères pris parmi les 94 caractères imprimables du clavier ?</li>
<li>Combien de « bits » vaut chacun de ces mots de passe ?</li></ol>""",
r"""<p>Il y a \(26^8\) mots de passe de 8 minuscules. Le « nombre de bits » est \(\log_2\) du nombre de possibilités.</p>""",
r"""<p><strong>1.</strong> \(26^8 \approx 2{,}1 \times 10^{11}\), donc au pire \(2{,}1 \times 10^{11} / 10^{10} \approx 21\) secondes.</p>
<p><strong>2.</strong> \(94^{12} \approx 4{,}8 \times 10^{23}\), donc \(4{,}8 \times 10^{13}\) s, soit environ <strong>1,5 million d'années</strong>.</p>
<p><strong>3.</strong> \(\log_2(26^8) = 8 \log_2 26 \approx 37{,}6\) bits ; \(\log_2(94^{12}) = 12 \log_2 94 \approx 78{,}7\) bits.
La longueur compte plus que tout : chaque caractère ajoute \(\log_2 94 \approx 6{,}6\) bits.</p>""",
r"""<p>Ce calcul suppose un mot de passe choisi au hasard. Un mot du dictionnaire, même long, est trouvé bien plus vite : l'attaquant essaie d'abord les mots probables.</p>""") + exercice(4, "★★★", r"""<p>Aujourd'hui, une attaque sur une clé de 80 bits à \(10^{18}\) clés/s prend en moyenne environ 7 jours. Si la puissance de calcul double tous les deux ans,
dans combien d'années l'attaque <em>au pire cas</em> (toutes les clés) prendra-t-elle moins d'une journée ? Et combien de temps une clé de 128 bits résistera-t-elle,
avec le même critère, à ce rythme ?</p>""",
r"""<p>Au pire cas, aujourd'hui : \(2^{80} / 10^{18}\) secondes. Combien de doublements pour descendre sous 86 400 s ?</p>""",
r"""<p>Au pire : \(2^{80}/10^{18} \approx 1{,}2 \times 10^6\) s, soit environ 14 jours. Il faut diviser par 14, donc \(\log_2 14 \approx 3{,}8\) doublements,
soit 4 doublements entiers : <strong>8 ans</strong>.</p>
<p>Pour 128 bits, il y a 48 bits de plus, donc 48 doublements supplémentaires : \(8 + 2 \times 48 = 104\) ans environ.
Et encore, cela suppose que la loi de doublement tienne un siècle, ce que la physique rend très improbable.</p>""")

S02 = qcm("sortie", [
    (r"Le coût d'une recherche exhaustive sur une clé de \(b\) bits est proportionnel à :",
     [r"\(b\)", r"\(b^2\)", r"\(2^b\)", r"\(\log_2 b\)"], 2, r"Il y a \(2^b\) clés à essayer au pire."),
    (r"Doubler la vitesse de l'attaquant équivaut à :",
     [r"Doubler la taille de la clé", r"Retirer un bit à la clé", r"Retirer la moitié des bits", r"Rien du tout"], 1, r"\(2^{b-1}/(2v) = 2^{(b-1)-1}/v\)."),
    (r"Le nombre moyen d'essais pour une clé uniforme parmi \(N\) est :",
     [r"\(N\)", r"\(\frac{N+1}{2}\)", r"\(\log_2 N\)", r"\(\sqrt N\)"], 1, r"\(\frac1N \sum_{i=1}^N i = \frac{N+1}{2}\)."),
    (r"À \(10^{12}\) clés par seconde, une clé de 56 bits tombe en moyenne en environ :",
     [r"10 secondes", r"10 heures", r"10 ans", r"10 siècles"], 1, r"\(2^{55}/10^{12} \approx 3{,}6 \times 10^4\) s \(\approx\) 10 h."),
    (r"Pourquoi dit-on que la recherche exhaustive est « exponentielle » ?",
     [r"Parce qu'elle utilise l'exponentiation modulaire", r"Parce que son coût est exponentiel en la taille \(b\) de la clé",
      r"Parce qu'elle essaie les clés dans un ordre exponentiel", r"Parce que son coût est \(e^n\) pour un message de \(n\) bits"], 1,
     r"La taille de l'entrée de l'attaquant est \(b\) ; son travail est \(2^b\)."),
])

R02 = a_retenir([
    r"La recherche exhaustive essaie les \(2^b\) clés : au pire \(2^b\) essais, en moyenne \(\frac{2^b+1}{2} \approx 2^{b-1}\).",
    r"Chaque bit de clé double le coût de l'attaque ; 10 bits le multiplient par environ 1000.",
    r"Multiplier la puissance de l'attaquant par \(2^a\) revient à retirer \(a\) bits à la clé.",
    r"56 bits (DES) : cassable en quelques heures ; 80 bits : à la portée d'un supercalculateur ; 128 bits (AES) : hors de portée pour longtemps.",
])

CORPS["m0-attaque"] = etape(E02, C02, D02, I02, X02, S02, R02)
