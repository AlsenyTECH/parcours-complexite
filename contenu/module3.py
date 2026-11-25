# -*- coding: utf-8 -*-
"""Module 3 — Analyser un algorithme itératif.

Étape pilote : 3.3 Le tri par insertion (exercice 2 de l'annale 2024-2025).
Toutes les valeurs numériques de cette page (traces, tⱼ, T(n), moyennes) ont été vérifiées
par simulation : voir outils/verifier_insertion.py.
"""

from briques import (retenir, demo, prof, master, exercice, video, qcm, preuve, a_toi, a_retenir,
                     etape, atelier, examen, methode, animateur, mesure, tableau)

CORPS = {}

PSEUDO = """<pre class="pseudo tex2jax_ignore"><span class="num">1</span>Pour j = 2 à n
<span class="num">2</span>    clé = T[j]
<span class="num">3</span>    ▹ insérer T[j] dans la suite triée T[1..j−1]
<span class="num">4</span>    i = j − 1
<span class="num">5</span>    tant que i > 0 et T[i] > clé
<span class="num">6</span>        T[i+1] = T[i]
<span class="num">7</span>        i = i − 1
<span class="num">8</span>    T[i+1] = clé</pre>"""

# ─────────────────────────────────────────────────────────────────────────────
ENTREE = qcm("entree", [
    (r"Sur le tableau déjà trié \([1, 2, \dots, n]\), combien de fois le test de la ligne 5 est-il exécuté en tout ?",
     [r"\(0\)", r"\(n-1\)", r"\(n(n-1)/2\)", r"\(n^2\)"], 1,
     r"Pour chaque \(j\) de 2 à \(n\), le test est fait une fois et il est faux tout de suite : \(n-1\) tests."),
    (r"Quelle est la complexité du tri par insertion au pire cas ?",
     [r"\(\Theta(n)\)", r"\(\Theta(n\log n)\)", r"\(\Theta(n^2)\)", r"\(\Theta(2^n)\)"], 2,
     r"Au pire cas, \(t_j = j\) et \(\sum_{j=2}^{n} j = \frac{n(n+1)}{2} - 1\) : c'est quadratique."),
    (r"Après le passage \(j = 3\) sur \(T = [3, 8, 2, 6]\), que vaut \(T\) ?",
     [r"\([2, 3, 8, 6]\)", r"\([3, 2, 8, 6]\)", r"\([2, 3, 6, 8]\)", r"\([3, 8, 2, 6]\)"], 0,
     r"Le passage \(j = 3\) range la clé 2 devant 3 et 8 : \([2, 3, 8, 6]\). Le 6 n'a pas encore bougé."),
])

# ─────────────────────────────────────────────────────────────────────────────
COMPRENDRE = r"""
<p class="lead">Tu tiens des cartes dans ta main gauche, déjà rangées. Tu en pioches une nouvelle : tu la glisses
de droite à gauche, en décalant chaque carte plus grande qu'elle, jusqu'à trouver sa place. Puis tu recommences
avec la carte suivante. Le tri par insertion, c'est exactement ce geste.</p>
""" + video("m3-insertion.mp4", "Le tri par insertion au tableau : l'exemple, le comptage ligne par ligne, le meilleur et le pire cas", "7 min 41") + r"""

<h3>L'algorithme</h3>
<p>Voici la version de l'annale 2024-2025, avec sa numérotation de lignes. Le tableau est indexé de 1 à \(n\).</p>
""" + PSEUDO + r"""
<p>À chaque tour de la boucle <strong>Pour</strong>, la partie gauche \(T[1..j-1]\) est déjà triée.
On met de côté la <em>clé</em> \(T[j]\) (ligne 2), puis on remonte vers la gauche avec l'indice \(i\) (lignes 4 à 7) :
tant que l'élément \(T[i]\) est plus grand que la clé, on le décale d'une case vers la droite. Quand on s'arrête, la case
\(i+1\) est libre et c'est la place de la clé (ligne 8).</p>

""" + prof(r"""<p>La ligne 3 n'est pas une instruction : c'est un commentaire qui dit ce que font les lignes 4 à 8.
Elle ne coûte rien. Si ton professeur la compte quand même, aucun problème : <strong>annonce ta convention</strong>
et tiens-la jusqu'au bout. La complexité asymptotique ne change pas.</p>""") + r"""

<h3>Fais-le tourner</h3>
<p>L'animateur exécute l'algorithme instruction par instruction. Regarde trois choses : la ligne surlignée,
la colonne <em>exéc.</em> qui compte combien de fois chaque ligne a été exécutée, et le tableau des \(t_j\).
Commence par l'entrée de l'annale, puis compare « déjà trié » et « trié à l'envers ».</p>
""" + animateur("anim-insertion", "insertion", [
    ["Annale : 3, 8, 2, 6", [3, 8, 2, 6]],
    ["Déjà trié", [1, 2, 3, 4, 5, 6]],
    ["Trié à l'envers", [6, 5, 4, 3, 2, 1]],
    ["Avec doublons", [4, 2, 4, 1, 3]],
], "le tri par insertion, ligne par ligne") + r"""

<h3>Les nombres \(t_j\)</h3>
""" + retenir("Définition", r"""<p>Pour \(j = 2, \dots, n\), on note \(t_j\) le nombre de fois que le <strong>test</strong> de la
ligne 5 (« \(i > 0\) et \(T[i] > \text{clé}\) ») est évalué pendant le passage numéro \(j\) de la boucle Pour.</p>
<p>Chaque évaluation vraie provoque un décalage ; la dernière évaluation, elle, est fausse et fait sortir de la boucle. Donc
\[ t_j = (\text{nombre de décalages faits pour la clé } T[j]) + 1, \qquad 1 \le t_j \le j. \]</p>""") + r"""
<p>Le minimum \(t_j = 1\) arrive quand la clé est déjà à sa place (le premier test est faux). Le maximum \(t_j = j\) arrive quand la clé
doit aller tout au début : \(i\) prend les valeurs \(j-1, j-2, \dots, 1\) (\(j-1\) tests vrais), puis \(i = 0\) (un test faux).</p>

""" + a_toi(r"""<p><strong>Annale 2024-2025, exercice 2, questions 1 et 2.</strong> On donne \(T = [3, 8, 2, 6]\).
Sans l'animateur, écris l'état du tableau après chaque passage de la boucle Pour, la valeur de la clé,
les décalages effectués et la valeur de \(t_j\). Quelle est la valeur finale de \(T\) ?</p>""",
r"""""" + tableau(
    ["Passage", "clé", "Ce qui se passe", "\\(t_j\\)", "T après le passage"],
    [["\\(j = 2\\)", "8", "\\(T[1] = 3 \\le 8\\) : le premier test est faux, rien ne bouge.", "1", "[3, 8, 2, 6]"],
     ["\\(j = 3\\)", "2", "\\(8 > 2\\) : on décale 8 ; \\(3 > 2\\) : on décale 3 ; \\(i = 0\\) : arrêt. La clé va en case 1.", "3", "[2, 3, 8, 6]"],
     ["\\(j = 4\\)", "6", "\\(8 > 6\\) : on décale 8 ; \\(3 \\le 6\\) : arrêt. La clé va en case 3.", "2", "[2, 3, 6, 8]"]],
    "trace") + r"""
<p>Valeur finale : \(T = [2, 3, 6, 8]\). Au total \(\sum t_j = 1 + 3 + 2 = 6\) tests à la ligne 5, et 3 décalages.</p>""")

# ─────────────────────────────────────────────────────────────────────────────
DEMONTRER = r"""
<p class="lead">Deux choses à établir : l'algorithme <em>trie</em> bien (correction), et ce qu'il <em>coûte</em>.
Pour le coût, on applique la méthode ligne par ligne, puis on étudie les trois cas.</p>

<h3>1. L'algorithme est correct</h3>
""" + preuve("Proposition (invariant de boucle)",
    r"""<p>Au début de chaque passage de la boucle Pour, de numéro \(j\), le sous-tableau \(T[1..j-1]\) contient les éléments
    qui s'y trouvaient au départ, mais triés dans l'ordre croissant. En particulier, à la sortie (\(j = n+1\)), \(T[1..n]\) est trié.</p>""",
    r"""On montre que la propriété est vraie au premier passage, qu'un passage la préserve, et qu'à la sortie elle dit exactement « le tableau est trié ».""",
    [r"<strong>Initialisation</strong> : pour \(j = 2\), que contient \(T[1..1]\) ?",
     r"<strong>Conservation</strong> : que font les lignes 4 à 7 aux éléments plus grands que la clé ? Où se trouve la case libre à la sortie de la boucle ?",
     r"<strong>Terminaison</strong> : quelle est la valeur de \(j\) quand la boucle Pour s'arrête ?"],
    r"""<p><strong>Initialisation.</strong> Pour \(j = 2\), \(T[1..1]\) contient un seul élément, l'élément d'origine : il est trié.</p>
    <p><strong>Conservation.</strong> Supposons \(T[1..j-1]\) trié au début du passage \(j\), et notons \(x\) la clé \(T[j]\).
    La boucle des lignes 5 à 7 décale d'une case vers la droite les éléments \(T[j-1], T[j-2], \dots\) tant qu'ils sont strictement
    plus grands que \(x\). Elle s'arrête au premier indice \(i\) tel que \(i = 0\) ou \(T[i] \le x\). À ce moment :</p>
    <ul><li>\(T[1..i]\) n'a pas bougé : il est trié et tous ses éléments sont \(\le x\) (car \(T[i] \le x\) et \(T[1..i]\) est trié) ;</li>
    <li>\(T[i+2..j]\) contient, dans le même ordre, les anciens \(T[i+1..j-1]\) : ils sont triés et tous \(> x\).</li></ul>
    <p>La ligne 8 écrit \(x\) dans la case \(i+1\). Alors \(T[1..j]\) est trié et contient exactement les éléments d'origine de
    \(T[1..j]\). C'est l'invariant pour le passage suivant \(j+1\).</p>
    <p><strong>Terminaison.</strong> La boucle Pour s'arrête quand \(j = n+1\). L'invariant dit alors que \(T[1..n]\) est trié.
    Par ailleurs chaque boucle tant que s'arrête, car \(i\) diminue de 1 à chaque tour et le test exige \(i > 0\).</p>""") + r"""

<h3>2. Le coût, ligne par ligne</h3>
""" + methode("analyser un algorithme itératif", [
    r"Fixer le modèle : chaque instruction simple (affectation, comparaison, test) coûte une constante.",
    r"Pour chaque ligne, écrire son coût et le <strong>nombre de fois</strong> où elle est exécutée, en fonction de \(n\) et des quantités qui dépendent des données (ici les \(t_j\)).",
    r"Additionner : \(T(n) = \sum (\text{coût} \times \text{nombre d'exécutions})\).",
    r"Étudier le meilleur cas, le pire cas, puis éventuellement le cas moyen, en encadrant les quantités qui dépendent des données.",
]) + r"""
<p>On note \(c_k\) le coût de la ligne \(k\). La seule difficulté est de compter juste les exécutions.</p>
""" + tableau(["Ligne", "Instruction", "Coût", "Nombre d'exécutions"], [
    ["1", "Pour j = 2 à n", r"\(c_1\)", r"\(n\)"],
    ["2", "clé = T[j]", r"\(c_2\)", r"\(n - 1\)"],
    ["3", "commentaire", r"\(0\)", r"\(n - 1\)"],
    ["4", "i = j − 1", r"\(c_4\)", r"\(n - 1\)"],
    ["5", "tant que i > 0 et T[i] > clé", r"\(c_5\)", r"\(\sum_{j=2}^{n} t_j\)"],
    ["6", "T[i+1] = T[i]", r"\(c_6\)", r"\(\sum_{j=2}^{n} (t_j - 1)\)"],
    ["7", "i = i − 1", r"\(c_7\)", r"\(\sum_{j=2}^{n} (t_j - 1)\)"],
    ["8", "T[i+1] = clé", r"\(c_8\)", r"\(n - 1\)"],
], "cout") + r"""
<p>Trois points méritent une justification sur ta copie :</p>
<ul>
<li><strong>Ligne 1 : \(n\) fois, pas \(n-1\).</strong> La boucle Pour teste \(j \le n\) pour \(j = 2, 3, \dots, n\) (\(n-1\) tests vrais),
puis une dernière fois pour \(j = n+1\) (test faux, qui fait sortir). Total : \(n\).</li>
<li><strong>Lignes 2, 4, 8 : \(n-1\) fois</strong>, une fois par passage dans la boucle.</li>
<li><strong>Lignes 6 et 7 : \(t_j - 1\) fois par passage</strong>, car le corps de la boucle tant que s'exécute pour chaque test vrai,
et seul le dernier des \(t_j\) tests est faux.</li>
</ul>
<p>En additionnant :</p>
\[ T(n) = c_1 n + (c_2 + c_4 + c_8)(n-1) + c_5 \sum_{j=2}^{n} t_j + (c_6 + c_7) \sum_{j=2}^{n} (t_j - 1). \]
<p>L'annale demande le cas où toutes les instructions simples coûtent la même constante \(c\). Comme
\(\sum_{j=2}^{n}(t_j - 1) = \sum_{j=2}^{n} t_j - (n-1)\) :</p>
\[ T(n) = c\Big[\, n + 3(n-1) + \sum_{j=2}^{n} t_j + 2\Big(\sum_{j=2}^{n} t_j - (n-1)\Big)\Big] \]
""" + retenir("Le coût du tri par insertion", r"""\[ T(n) = c\Big(3\sum_{j=2}^{n} t_j + 2n - 1\Big). \]
<p>Vérification sur \(T = [3, 8, 2, 6]\) : \(n = 4\), \(\sum t_j = 6\), donc \(T(4) = c(18 + 7) = 25c\).
L'animateur, qui compte chaque exécution une par une, trouve aussi \(25c\).</p>""") + r"""

<h3>3. Le meilleur cas</h3>
""" + preuve("Proposition (meilleur cas)",
    r"""<p>\(T_{\min}(n) = c(5n - 4)\), atteint exactement quand le tableau est déjà trié. Donc \(T_{\min}(n) = \Theta(n)\).</p>""",
    r"""Le coût croît avec les \(t_j\), et chaque \(t_j\) vaut au moins 1.""",
    [r"Pourquoi a-t-on toujours \(t_j \ge 1\) ?",
     r"Quand a-t-on \(t_j = 1\) ? Traduis-le en une condition sur \(T[j-1]\) et la clé.",
     r"Remplace dans la formule de \(T(n)\)."],
    r"""<p>Le test de la ligne 5 est évalué au moins une fois à chaque passage, donc \(t_j \ge 1\) et \(\sum_{j=2}^{n} t_j \ge n-1\). Ainsi
    \[ T(n) \ge c\big(3(n-1) + 2n - 1\big) = c(5n - 4). \]
    Cette borne est atteinte si et seulement si \(t_j = 1\) pour tout \(j\), c'est-à-dire si le premier test est faux à chaque passage :
    \(T[j-1] \le T[j]\) (avec \(i = j - 1 \ge 1\), la première partie du test est vraie, donc c'est la comparaison qui échoue).
    C'est exactement dire que le tableau est trié. Enfin \(c(5n-4)\) est un polynôme de degré 1 : \(T_{\min}(n) = \Theta(n)\).</p>""") + r"""

<h3>4. Le pire cas</h3>
""" + preuve("Proposition (pire cas)",
    r"""<p>\(T_{\max}(n) = c\Big(\dfrac{3n^2}{2} + \dfrac{7n}{2} - 4\Big)\), atteint quand le tableau est trié dans l'ordre strictement décroissant.
    Donc \(T_{\max}(n) = \Theta(n^2)\).</p>""",
    r"""Chaque \(t_j\) vaut au plus \(j\), et un tableau trié à l'envers force chaque clé à remonter jusqu'au début.""",
    [r"Pourquoi a-t-on toujours \(t_j \le j\) ?",
     r"Sur un tableau strictement décroissant, montre que \(t_j = j\).",
     r"Calcule \(\sum_{j=2}^{n} j\), puis remplace."],
    r"""<p>Pendant le passage \(j\), l'indice \(i\) part de \(j-1\) et diminue de 1 après chaque test vrai ; un test avec \(i = 0\) est forcément faux.
    Le test est donc évalué au plus pour \(i = j-1, j-2, \dots, 1, 0\), soit \(t_j \le j\).</p>
    <p>Si le tableau est strictement décroissant, au passage \(j\) la clé est strictement plus petite que tous les éléments de \(T[1..j-1]\)
    (ce sont les éléments d'origine \(T[1], \dots, T[j-1]\), tous plus grands qu'elle). Tous les tests avec \(i \ge 1\) sont vrais : \(t_j = j\).</p>
    <p>Or \(\displaystyle \sum_{j=2}^{n} j = \frac{n(n+1)}{2} - 1\). Donc
    \[ T_{\max}(n) = c\Big(3\Big(\frac{n(n+1)}{2} - 1\Big) + 2n - 1\Big) = c\Big(\frac{3n^2}{2} + \frac{7n}{2} - 4\Big). \]
    Le terme dominant est \(\frac{3c}{2} n^2\) : \(T_{\max}(n) = \Theta(n^2)\).</p>""") + r"""

<h3>5. Le cas moyen</h3>
<p>Le pire cas est une garantie ; le cas moyen dit ce qui se passe « d'habitude ». Il faut d'abord un modèle de hasard :
on suppose les éléments distincts et les \(n!\) ordres possibles <strong>équiprobables</strong>.</p>
""" + preuve("Proposition (cas moyen)",
    r"""<p>Sous cette hypothèse, \(\mathbb{E}[t_j] = \dfrac{j+1}{2}\), et le coût moyen vaut
    \[ T_{\text{moy}}(n) = c\Big(\frac{3n^2}{4} + \frac{17n}{4} - 4\Big) = \Theta(n^2). \]
    En moyenne, le tri par insertion coûte environ la moitié du pire cas : c'est toujours quadratique.</p>""",
    r"""\(t_j - 1\) est le nombre d'éléments de \(T[1..j-1]\) plus grands que la clé, et le rang de la clé parmi les \(j\) premiers éléments est uniforme.""",
    [r"Montre que \(t_j - 1\) est le nombre d'indices \(k < j\) tels que \(T[k] > T[j]\) (valeurs d'origine).",
     r"Pourquoi ce nombre est-il uniforme sur \(\{0, 1, \dots, j-1\}\) ?",
     r"Calcule son espérance, puis utilise la linéarité de l'espérance."],
    r"""<p>Le passage \(j\) décale exactement les éléments de \(T[1..j-1]\) strictement plus grands que la clé (ils sont rangés à droite de la partie triée).
    Donc \(t_j - 1 = \Card\{k < j : T[k] > T[j]\}\), en valeurs d'origine.</p>
    <p>Pour une permutation au hasard, les \(j\) premiers éléments sont dans un ordre relatif au hasard : la clé a la même probabilité
    \(1/j\) d'être la plus petite, la deuxième, …, la plus grande d'entre eux. Le nombre d'éléments plus grands qu'elle est donc uniforme
    sur \(\{0, \dots, j-1\}\), d'espérance \(\frac{j-1}{2}\). D'où \(\mathbb{E}[t_j] = \frac{j+1}{2}\).</p>
    <p>Par linéarité de l'espérance :
    \[ \mathbb{E}\Big[\sum_{j=2}^{n} t_j\Big] = \frac12 \sum_{j=2}^{n} (j+1) = \frac12\Big(\frac{(n+1)(n+2)}{2} - 3\Big) = \frac{n^2 + 3n - 4}{4}, \]
    et \(T_{\text{moy}}(n) = c\big(3 \cdot \frac{n^2+3n-4}{4} + 2n - 1\big) = c\big(\frac{3n^2}{4} + \frac{17n}{4} - 4\big)\).</p>""") + r"""

""" + examen(r"""<p>Pour l'exercice 2 de l'annale, voici ce qui rapporte les points, et pourquoi.</p>
<ul>
<li><strong>Le tableau ligne / coût / nombre d'exécutions.</strong> C'est la preuve que tu as compté. Une formule écrite seule semble sortie de nulle part :
le correcteur ne peut pas savoir si elle est juste par hasard.</li>
<li><strong>La justification de la ligne 1 (\(n\) fois) et des lignes 6 et 7 (\(t_j - 1\) fois).</strong> Ce sont les deux endroits où les copies se trompent,
donc ceux que le correcteur vérifie en premier. Une phrase suffit : « le dernier test de la boucle Pour, pour \(j = n+1\), est faux et compte aussi »,
et « le corps du tant que s'exécute une fois par test vrai, et seul le dernier des \(t_j\) tests est faux ».</li>
<li><strong>La formule simplifiée \(T(n) = c(3\sum t_j + 2n - 1)\).</strong> Elle montre que tu sais regrouper : la question 3 demande « en fonction de \(c\), des \(t_j\) et de \(n\) »,
pas une somme de huit termes.</li>
<li><strong>Pour \(T_{\min}\) et \(T_{\max}\) : la valeur des \(t_j\), pourquoi c'est le minimum ou le maximum, et quelle entrée l'atteint.</strong>
Sans l'entrée, tu as seulement un minorant ou un majorant ; c'est l'entrée (tableau trié, ou trié à l'envers) qui prouve que la borne est atteinte.</li>
<li><strong>La conclusion asymptotique, \(\Theta(n)\) et \(\Theta(n^2)\).</strong> C'est la réponse à la question qu'on se pose vraiment : comment le coût grandit avec \(n\).</li>
</ul>""") + master(r"""<p>Le temps du tri par insertion <em>dépend des données</em> : rapide sur un tableau presque trié, lent sur un tableau à l'envers.
En cryptographie, c'est un défaut grave. Un attaquant qui mesure le temps d'exécution apprend quelque chose sur les données secrètes :
c'est une <strong>attaque par canal auxiliaire</strong>. Les bibliothèques cryptographiques écrivent donc leurs opérations sur les secrets
« en temps constant », c'est-à-dire avec un nombre d'opérations qui ne dépend que de la taille de l'entrée.</p>""")

# ─────────────────────────────────────────────────────────────────────────────
IMPLEMENTER = r"""
<p class="lead">À toi d'écrire le tri en Python, en comptant toi-même les tests de la ligne 5.
Puis tu le lanceras sur des tableaux de plus en plus grands pour <em>voir</em> les formules de la partie Démontrer.</p>
""" + prof(r"""<p>Deux pièges en passant du pseudo-code à Python :</p>
<ul><li>Python indexe à partir de 0 : la boucle devient <code>for j in range(1, n)</code>, et le test « \(i > 0\) » devient <code>i &gt;= 0</code>.</li>
<li>Pour compter <em>chaque</em> évaluation du test, y compris la dernière (fausse), écris la boucle ainsi :
<code>while True:</code> puis <code>nb += 1</code>, puis <code>if not (i &gt;= 0 and T[i] &gt; cle): break</code>.</li></ul>""") + atelier(
    "insertion",
    r"""<p>Complète <code>tri_insertion(T)</code>. Elle trie la liste <code>T</code> sur place et renvoie le couple
    <code>(T, nb_tests)</code>, où <code>nb_tests</code> est \(\sum t_j\), le nombre total d'évaluations du test de la ligne 5.
    Exemple attendu : <code>tri_insertion([3, 8, 2, 6])</code> renvoie <code>([2, 3, 6, 8], 6)</code>.</p>""",
    '''def tri_insertion(T):
    """Trie T sur place ; renvoie (T, nombre d'évaluations du test de la ligne 5)."""
    n = len(T)
    nb_tests = 0
    for j in range(1, n):          # j = 2 à n dans le pseudo-code
        cle = T[j]
        i = j - 1
        # À toi : la boucle « tant que », en comptant chaque test dans nb_tests

        T[i + 1] = cle
    return T, nb_tests


print(tri_insertion([3, 8, 2, 6]))
''',
    [
        {"appel": "tri_insertion([3, 8, 2, 6])", "verif": "r == ([2, 3, 6, 8], 6)", "attendu": "([2, 3, 6, 8], 6) — l'exemple de l'annale"},
        {"appel": "tri_insertion([])", "verif": "r == ([], 0)", "attendu": "([], 0) : aucun passage, aucun test"},
        {"appel": "tri_insertion([5])", "verif": "r == ([5], 0)", "attendu": "([5], 0)"},
        {"appel": "tri_insertion(list(range(1, 11)))", "verif": "r == (list(range(1, 11)), 9)", "attendu": "tableau trié de taille 10 : 9 tests (meilleur cas, n − 1)"},
        {"appel": "tri_insertion(list(range(10, 0, -1)))", "verif": "r == (list(range(1, 11)), 54)", "attendu": "trié à l'envers, n = 10 : 54 tests (pire cas, n(n+1)/2 − 1)"},
        {"appel": "tri_insertion([2, 2, 2])", "verif": "r == ([2, 2, 2], 2)", "attendu": "([2, 2, 2], 2) : des éléments égaux ne se décalent pas"},
        {"appel": "tri_insertion([4, 2, 4, 1, 3])", "verif": "r == ([1, 2, 3, 4, 4], 10)", "attendu": "([1, 2, 3, 4, 4], 10)"},
        {"appel": "tri_insertion([9, -3, 0, 7, -3, 12, 5, 1])", "verif": "r[0] == sorted([9, -3, 0, 7, -3, 12, 5, 1]) and r[1] == 20", "attendu": "le tableau trié, et 20 tests"},
    ],
    r"""<pre class="pseudo">def tri_insertion(T):
    n = len(T)
    nb_tests = 0
    for j in range(1, n):
        cle = T[j]
        i = j - 1
        while True:
            nb_tests += 1                      # une évaluation du test de la ligne 5
            if not (i &gt;= 0 and T[i] &gt; cle):
                break
            T[i + 1] = T[i]                    # ligne 6
            i -= 1                             # ligne 7
        T[i + 1] = cle                         # ligne 8
    return T, nb_tests</pre>
    <p>Version plus courte, si l'on ne compte pas : <code>while i &gt;= 0 and T[i] &gt; cle: T[i+1] = T[i]; i -= 1</code>.</p>""") + r"""

<h3>Mesurer : la formule devient une courbe</h3>
""" + mesure("insertion",
    r"""<p>Ce bouton lance <strong>ton</strong> <code>tri_insertion</code> sur des tableaux de taille 10 à 400 :
    déjà triés, au hasard (moyenne de 8 essais) et triés à l'envers. Il trace le nombre de tests compté,
    avec en pointillés les trois formules démontrées : \(n - 1\), \(\frac{n^2+3n-4}{4}\) et \(\frac{n(n+1)}{2} - 1\).</p>""",
    "tri_insertion", [10, 25, 50, 100, 150, 200, 300, 400],
    [["n(n+1)/2 − 1", "n*(n+1)/2 - 1"], ["(n²+3n−4)/4", "(n*n + 3*n - 4)/4"], ["n − 1", "n - 1"]],
    [{"nom": "pire cas (trié à l'envers)", "court": "pire", "expr": "(list(range(n, 0, -1)),)", "couleur": "pire"},
     {"nom": "moyenne sur 8 tableaux au hasard", "court": "moyen", "expr": "(random.sample(range(10 * n), n),)", "couleur": "moyen", "essais": 8},
     {"nom": "meilleur cas (déjà trié)", "court": "meilleur", "expr": "(list(range(n)),)", "couleur": "meilleur"}],
    [["pire / n²", 0, "n*n"], ["moyen / n²", 1, "n*n"]]) + r"""
""" + prof(r"""<p>Regarde les deux dernières colonnes du tableau : « pire / \(n^2\) » se rapproche de \(\frac12\), et « moyen / \(n^2\) » de \(\frac14\).
C'est le sens concret de \(\Theta(n^2)\) : le rapport au carré de \(n\) se stabilise. La courbe verte, elle, est collée à l'axe :
\(n - 1\) est négligeable devant \(n^2\).</p>""")

# ─────────────────────────────────────────────────────────────────────────────
EXERCER = r"""
<p class="lead">Les exercices sont gradués. Fais-les sur une feuille, puis compare ta rédaction avec la correction, ligne à ligne.</p>
""" + exercice(1, "annale", r"""<p><strong>Annale 2024-2025, exercice 2, questions 3 à 5.</strong> Rédige comme le jour de l'examen :</p>
<ol start="3"><li>Exprime le coût \(T(n)\) en fonction de \(c\), des \(t_j\) et de \(n\).</li>
<li>Exprime \(T_{\min}(n)\), le coût dans le meilleur des cas.</li>
<li>Exprime \(T_{\max}(n)\), le coût dans le pire des cas.</li></ol>""",
r"""<p>Fais le tableau des lignes avant tout calcul. Pour la ligne 1, compte aussi le test qui fait sortir de la boucle.</p>""",
r"""<p><strong>Modèle.</strong> Chaque instruction simple coûte \(c\). La ligne 3 est un commentaire, de coût nul.
On note \(t_j\) le nombre d'évaluations du test de la ligne 5 au passage \(j\).</p>
<p><strong>3.</strong> La ligne 1 est exécutée \(n\) fois (\(n-1\) tests vrais pour \(j = 2, \dots, n\) et un test faux pour \(j = n+1\)).
Les lignes 2, 4 et 8 sont exécutées une fois par passage : \(n-1\) fois chacune. La ligne 5 est exécutée \(\sum_{j=2}^n t_j\) fois.
Les lignes 6 et 7 sont exécutées une fois par test vrai, soit \(t_j - 1\) fois au passage \(j\). Donc</p>
\[ T(n) = c\Big[n + 3(n-1) + \sum_{j=2}^n t_j + 2\sum_{j=2}^n (t_j - 1)\Big] = c\Big(3\sum_{j=2}^n t_j + 2n - 1\Big). \]
<p><strong>4.</strong> On a toujours \(t_j \ge 1\), avec égalité si et seulement si \(T[j-1] \le T[j]\) au moment du passage \(j\).
Le minimum est atteint pour un tableau déjà trié : \(\sum t_j = n - 1\) et
\[ T_{\min}(n) = c\big(3(n-1) + 2n - 1\big) = c(5n - 4) = \Theta(n). \]</p>
<p><strong>5.</strong> On a toujours \(t_j \le j\) (l'indice \(i\) va au plus de \(j-1\) à \(0\)), avec égalité pour tout \(j\) quand le tableau
est strictement décroissant. Alors \(\sum_{j=2}^n t_j = \frac{n(n+1)}{2} - 1\) et
\[ T_{\max}(n) = c\Big(\frac{3n(n+1)}{2} - 3 + 2n - 1\Big) = c\Big(\frac{3n^2}{2} + \frac{7n}{2} - 4\Big) = \Theta(n^2). \]</p>""",
r"""<p>Si tu as compté la ligne 3 avec un coût \(c\), tu obtiens \(T(n) = c(3\sum t_j + 3n - 2)\), \(T_{\min} = c(6n - 5)\) et
\(T_{\max} = c(\frac{3n^2}{2} + \frac{9n}{2} - 5)\). C'est juste aussi, à condition de l'avoir annoncé.</p>""") + exercice(2, "★", r"""<p>On ne compte plus les tests de la ligne 5, mais seulement les <strong>comparaisons entre éléments</strong>
\(T[i] > \text{clé}\). Attention : dans « \(i > 0\) et \(T[i] > \text{clé}\) », si \(i > 0\) est faux, la comparaison n'est pas évaluée
(évaluation paresseuse du « et »). Combien de comparaisons entre éléments au meilleur cas ? Au pire cas ?</p>""",
r"""<p>Au pire cas, le dernier test de chaque passage a lieu avec \(i = 0\).</p>""",
r"""<p>Au passage \(j\), une comparaison est évaluée pour chaque test où \(i \ge 1\).</p>
<p><strong>Meilleur cas</strong> (tableau trié) : un seul test, avec \(i = j - 1 \ge 1\) : une comparaison par passage, soit \(n - 1\) au total.</p>
<p><strong>Pire cas</strong> (tableau strictement décroissant) : les tests ont lieu pour \(i = j-1, \dots, 1, 0\) ; le dernier (\(i = 0\)) ne compare rien.
Il y a donc \(j - 1\) comparaisons au passage \(j\), et au total \(\sum_{j=2}^{n} (j-1) = \frac{n(n-1)}{2}\).</p>
<p>C'est le nombre qu'on cite en général : « le tri par insertion fait au plus \(\frac{n(n-1)}{2}\) comparaisons ». Il diffère de \(\sum t_j\)
de \(n-1\) au plus, ce qui ne change pas le \(\Theta(n^2)\).</p>""") + exercice(3, "★★", r"""<p>Une <strong>inversion</strong> d'un tableau \(T\) est un couple d'indices \((k, \ell)\) avec \(k < \ell\) et \(T[k] > T[\ell]\).</p>
<ol><li>Montre que le nombre total de décalages (exécutions de la ligne 6) est égal au nombre d'inversions du tableau de départ.</li>
<li>Combien d'inversions a un tableau trié à l'envers ? Retrouve le pire cas.</li>
<li>En déduire le nombre moyen de décalages pour une permutation au hasard, en associant à chaque tableau son « miroir ».</li></ol>""",
r"""<p>Pour 3, un couple \((k, \ell)\) est une inversion dans \(T\) ou dans son miroir (le tableau lu de droite à gauche), jamais dans les deux.</p>""",
r"""<p><strong>1.</strong> Au passage \(\ell\), la clé \(T[\ell]\) est décalée devant exactement les éléments d'origine \(T[k]\), \(k < \ell\), qui lui sont
strictement supérieurs : ce sont les inversions de la forme \((k, \ell)\). En sommant sur \(\ell\), on compte chaque inversion une fois.</p>
<p><strong>2.</strong> Dans un tableau strictement décroissant, tous les couples \(k < \ell\) sont des inversions : il y en a \(\binom{n}{2} = \frac{n(n-1)}{2}\).
C'est bien \(\sum (t_j - 1) = \sum_{j=2}^n (j - 1)\).</p>
<p><strong>3.</strong> Les éléments étant distincts, chacun des \(\binom n2\) couples \(k<\ell\) est une inversion soit de \(T\), soit de son miroir.
Donc \(\text{inv}(T) + \text{inv}(\text{miroir}) = \binom n2\). Le miroir d'une permutation au hasard est encore une permutation au hasard,
d'où \(2\,\mathbb{E}[\text{inv}] = \binom n2\) et \(\mathbb{E}[\text{inv}] = \frac{n(n-1)}{4}\).
On retrouve \(\mathbb{E}\big[\sum (t_j - 1)\big] = \frac{n^2+3n-4}{4} - (n-1) = \frac{n(n-1)}{4}\).</p>""",
r"""<p>Ce résultat est puissant : <em>tout</em> tri qui ne fait qu'échanger des éléments voisins fait au moins autant d'échanges qu'il y a
d'inversions, donc \(\Theta(n^2)\) en moyenne. Pour faire mieux, il faut déplacer des éléments loin d'un coup : c'est ce que fait le tri fusion (module 4).</p>""") + exercice(4, "★★", r"""<p><strong>Insertion dichotomique.</strong> Dans la partie triée \(T[1..j-1]\), on cherche la place de la clé par recherche dichotomique
(au plus \(\lceil \log_2 j \rceil\) comparaisons), puis on décale les éléments plus grands.</p>
<ol><li>Majore le nombre total de comparaisons par \(O(n \log n)\).</li>
<li>Le tri devient-il pour autant un tri en \(O(n \log n)\) ? Justifie.</li></ol>""",
r"""<p>Les comparaisons ne sont pas les seules opérations : regarde les décalages au pire cas.</p>""",
r"""<p><strong>1.</strong> \(\sum_{j=2}^{n} \lceil \log_2 j \rceil \le \sum_{j=2}^{n} (\log_2 n + 1) \le n(\log_2 n + 1) = O(n \log n)\).</p>
<p><strong>2.</strong> Non. Trouver la place plus vite ne change pas le nombre de décalages : sur un tableau à l'envers, la clé \(T[j]\) doit toujours
aller en tête, et il faut décaler \(j - 1\) éléments. Le total des décalages reste \(\frac{n(n-1)}{2}\), et le coût reste \(\Theta(n^2)\) au pire cas.
L'insertion dichotomique est utile seulement quand une comparaison coûte beaucoup plus cher qu'un déplacement (comparer de longues chaînes, par exemple).</p>""") + exercice(5, "★★★", r"""<p>On dit qu'un tableau est <strong>\(k\)-presque trié</strong> si chaque élément est à au plus \(k\) positions de sa place dans le tableau trié.
Montre que le tri par insertion trie un tel tableau en \(O(nk)\). Que dire pour \(k\) constant ?</p>""",
r"""<p>Majore le nombre d'éléments plus grands que \(T[j]\) situés avant lui.</p>""",
r"""<p>Soit \(x = T[j]\), de place finale \(p\), avec \(|j - p| \le k\). Un élément \(y > x\) placé avant \(x\) (à un indice \(q < j\)) a une place finale
\(p_y > p\). Comme \(|q - p_y| \le k\), on a \(q \ge p_y - k > p - k \ge j - 2k\). Donc \(y\) est parmi les indices \(j-2k+1, \dots, j-1\) :
il y a au plus \(2k - 1\) tels éléments. Ainsi \(t_j - 1 \le 2k - 1\), \(\sum t_j \le 2k(n-1)\) et \(T(n) = c(3\sum t_j + 2n - 1) = O(nk)\).</p>
<p>Pour \(k\) constant, le tri est <strong>linéaire</strong>. C'est pourquoi on l'utilise pour finir un tri presque fini, ou sur de petits tableaux
(les implémentations rapides de tri l'utilisent en dessous d'une vingtaine d'éléments).</p>""")

SORTIE = qcm("sortie", [
    (r"Le test de la ligne 5 est évalué \(t_j\) fois au passage \(j\). Combien de fois la ligne 6 est-elle exécutée à ce passage ?",
     [r"\(t_j\)", r"\(t_j - 1\)", r"\(t_j + 1\)", r"\(j - 1\)"], 1,
     r"Le corps de la boucle s'exécute une fois par test vrai ; le dernier test est faux."),
    (r"Avec un coût \(c\) par instruction simple (ligne 3 gratuite), \(T(n)\) vaut :",
     [r"\(c(3\sum t_j + 2n - 1)\)", r"\(c(\sum t_j + n)\)", r"\(c(3\sum t_j + 3n)\)", r"\(c \sum t_j\)"], 0,
     r"\(n + 3(n-1) + \sum t_j + 2\sum(t_j - 1) = 3\sum t_j + 2n - 1\)."),
    (r"Pour quelle entrée de taille \(n\) le tri par insertion atteint-il son pire cas ?",
     [r"Un tableau déjà trié", r"Un tableau dont tous les éléments sont égaux", r"Un tableau trié dans l'ordre strictement décroissant", r"Un tableau au hasard"], 2,
     r"Chaque clé est plus petite que tout ce qui la précède : elle remonte jusqu'au début, \(t_j = j\)."),
    (r"Que vaut \(\sum_{j=2}^{n} j\) ?",
     [r"\(\frac{n(n+1)}{2}\)", r"\(\frac{n(n-1)}{2}\)", r"\(\frac{n(n+1)}{2} - 1\)", r"\(n^2 - 1\)"], 2,
     r"\(\sum_{j=1}^{n} j = \frac{n(n+1)}{2}\), et on retire le terme \(j = 1\)."),
    (r"Le coût moyen du tri par insertion (permutations équiprobables) est :",
     [r"\(\Theta(n)\), car le hasard évite le pire cas", r"\(\Theta(n \log n)\)", r"\(\Theta(n^2)\), environ la moitié du pire cas", r"Impossible à calculer"], 2,
     r"\(\mathbb{E}[t_j] = \frac{j+1}{2}\), donc \(\mathbb{E}[\sum t_j] = \frac{n^2+3n-4}{4}\) : toujours quadratique."),
])

RETENIR = a_retenir([
    r"\(t_j\) = nombre d'évaluations du test de la ligne 5 au passage \(j\) ; \(1 \le t_j \le j\), et \(t_j - 1\) = nombre de décalages.",
    r"\(T(n) = c\,(3\sum_{j=2}^{n} t_j + 2n - 1)\), la ligne 1 comptant \(n\) fois.",
    r"Meilleur cas (tableau trié) : \(T_{\min}(n) = c(5n - 4) = \Theta(n)\).",
    r"Pire cas (trié à l'envers) : \(T_{\max}(n) = c(\frac{3n^2}{2} + \frac{7n}{2} - 4) = \Theta(n^2)\).",
    r"Cas moyen : \(c(\frac{3n^2}{4} + \frac{17n}{4} - 4) = \Theta(n^2)\) ; le nombre de décalages est le nombre d'inversions, \(\frac{n(n-1)}{4}\) en moyenne.",
])

CORPS["m3-insertion"] = etape(ENTREE, COMPRENDRE, DEMONTRER, IMPLEMENTER, EXERCER, SORTIE, RETENIR)
