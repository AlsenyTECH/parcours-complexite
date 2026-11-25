# -*- coding: utf-8 -*-
"""Tuto 3.3 — Le tri par insertion : combien ça coûte ?  (exercice 2 de l'annale 2024-2025)

Déroulé : la question → l'exemple [3, 8, 2, 6] fait au tableau → pourquoi on nomme les tⱼ →
le comptage ligne par ligne (avec la pause sur la ligne 1) → l'addition et sa vérification →
meilleur cas → pire cas (et le piège du − 1) → ce que ça change pour n = 1000 → la méthode.
"""
from tuto import (Tuto, ecrire, formule, cases, valeur, etat, marque, glisse, boite, extrait, depose, code, hl,
                  compte, compteur, fleche, entoure, efface)

T = Tuto("m3-insertion", "Le tri par insertion : combien ça coûte ?")
BLEU, ROUGE, VERT, ORANGE = "#1c3bb0", "#bd1f2b", "#0a7441", "#b15c00"
PSEUDO = ["Pour j = 2 à n", "  clé = T[j]", "  ▹ insérer T[j] dans T[1..j−1]", "  i = j − 1",
          "  tant que i > 0 et T[i] > clé", "    T[i+1] = T[i]", "    i = i − 1", "  T[i+1] = clé"]

# ── La question ──────────────────────────────────────────────────────────────
T.section("La question")
T.dit("Bonjour ! Dans ce tuto, on répond à une question précise : combien coûte le tri par insertion ?",
      ecrire("titre", 100, 80, "Le tri par insertion : combien ça coûte ?", "rouge", 54, gras=True, souligne=True))
T.dit("Attention : je ne veux pas une réponse du genre « il est rapide » ou « il est lent ». "
      "Je veux un nombre d'opérations, en fonction de la taille n du tableau. C'est exactement ce que demande l'exercice deux de l'annale.",
      ecrire("q1", 130, 180, "→ un nombre d'opérations, en fonction de n", "bleu", 42, a=0.45))
T.dit("On va procéder en trois temps. D'abord, comprendre l'algorithme sur un exemple. Ensuite, compter ce que coûte chaque ligne. "
      "Enfin, étudier le meilleur et le pire cas.",
      ecrire("p1", 130, 270, "1. comprendre sur un exemple", "bleu", 40, a=0.1),
      ecrire("p2", 130, 330, "2. compter ligne par ligne", "bleu", 40, a=0.4),
      ecrire("p3", 130, 390, "3. meilleur cas, pire cas", "bleu", 40, a=0.7))

# ── L'idée sur un exemple ────────────────────────────────────────────────────
T.section("1. L'idée, sur un exemple")
T.dit("Commençons par l'idée. Tu as déjà rangé des cartes dans ta main ? La partie gauche est déjà rangée. "
      "Tu prends une nouvelle carte, et tu la fais glisser vers la gauche jusqu'à sa place.",
      efface(), ecrire("t", 100, 70, "L'idée : ranger des cartes", "rouge", 46, gras=True, a=0.1),
      cases("T", 300, 190, [3, 8, 2, 6], 90, a=0.55))
T.dit("Prenons le tableau de l'annale : trois, huit, deux, six. Au départ, que dire de la première case, toute seule ? "
      "Elle est triée : un seul élément est toujours rangé. C'est pour ça que la boucle commence à j égale deux, et pas à un.",
      etat("T", 1, "trie", a=0.55),
      ecrire("n1", 300, 400, "une seule case : déjà triée", "vert", 38, a=0.55),
      ecrire("n2", 300, 455, "→ la boucle commence à j = 2", "vert", 38, a=0.8))
T.dit("Passage j égale deux. La clé, c'est T de deux : le huit. On la met de côté.",
      efface(["n1", "n2"]), boite("cle", 880, 150, "clé", a=0.1), marque("T", "j", 2, BLEU, a=0.2),
      extrait("T", 2, "cle", a=0.55))
T.dit("On la compare à la case de gauche. Trois est-il plus grand que huit ? Non. Le test est faux dès la première fois : "
      "le huit retourne à sa place, rien ne bouge.",
      marque("T", "i", 1, ROUGE, rang=1, a=0.1),
      ecrire("c1", 300, 420, "3 > 8 ?  non", "bleu", 40, a=0.25),
      compteur("t2", 880, 330, "t₂ =", 1, "orange", a=0.5),
      depose("cle", "T", 2, a=0.7), etat("T", [1, 2], "trie", a=0.95))
T.dit("Retiens ce chiffre : pour j égale deux, le test du tant que a été fait une seule fois. On note t deux égale un. "
      "Ces nombres t j sont le cœur de tout le calcul.",
      marque("T", "i", None, a=0.0), entoure("e1", 880, 330, 130, 50, "orange", a=0.4))
T.dit("Passage j égale trois. La clé est le deux. On la sort du tableau, ce qui libère sa case.",
      efface(["c1", "e1"]), marque("T", "j", 3, BLEU, a=0.1), extrait("T", 3, "cle", a=0.5))
T.dit("Premier test : i vaut deux. Huit est-il plus grand que deux ? Oui. Alors on décale le huit d'une case vers la droite, dans la case libre.",
      marque("T", "i", 2, ROUGE, rang=1, a=0.05), compteur("t3", 880, 400, "t₃ =", 1, "orange", a=0.2),
      ecrire("c2", 300, 420, "8 > 2 ?  oui → on décale", "bleu", 40, a=0.25),
      glisse("T", 2, 3, a=0.7), etat("T", 3, "trie", a=0.95), etat("T", 2, "vide", a=0.95))
T.dit("Deuxième test : i vaut un. Trois est-il plus grand que deux ? Oui encore. On décale le trois.",
      efface(["c2"]), marque("T", "i", 1, ROUGE, rang=1, a=0.05), compteur("t3", 880, 400, "t₃ =", 2, "orange", a=0.15),
      ecrire("c3", 300, 420, "3 > 2 ?  oui → on décale", "bleu", 40, a=0.2),
      glisse("T", 1, 2, a=0.65), etat("T", 2, "trie", a=0.95), etat("T", 1, "vide", a=0.95))
T.dit("Troisième test : i vaut zéro. On est arrivé au bord gauche. La condition i supérieur à zéro est fausse, on s'arrête. "
      "Voilà à quoi sert cette condition : sans elle, on sortirait du tableau.",
      efface(["c3"]), marque("T", "i", None), compteur("t3", 880, 400, "t₃ =", 3, "orange", a=0.15),
      ecrire("c4", 300, 420, "i = 0 → on s'arrête", "rouge", 40, a=0.2))
T.dit("La case libre est la case un : on y pose la clé. Bilan du passage : trois tests, et deux décalages.",
      efface(["c4"]), depose("cle", "T", 1, a=0.2), etat("T", [1, 2, 3], "trie", a=0.5))
T.dit("Remarque bien ça : trois tests, mais seulement deux décalages. Le dernier test est toujours celui qui échoue, celui qui fait sortir de la boucle. "
      "Donc, au passage j, il y a t j moins un décalages.",
      ecrire("regle", 300, 430, "décalages au passage j = tⱼ − 1", "rouge", 42, gras=True, a=0.55))
T.dit("Dernier passage, j égale quatre, avec la clé six. Huit est-il plus grand que six ? Oui : on le décale. "
      "Trois est-il plus grand que six ? Non : on s'arrête, et on pose le six dans la case libre.",
      marque("T", "j", 4, BLEU, a=0.02), extrait("T", 4, "cle", a=0.06, d=0.8),
      marque("T", "i", 3, ROUGE, rang=1, a=0.2), compteur("t4", 880, 470, "t₄ =", 1, "orange", a=0.22),
      glisse("T", 3, 4, a=0.32), etat("T", 4, "trie", a=0.44), etat("T", 3, "vide", a=0.44),
      marque("T", "i", 2, ROUGE, rang=1, a=0.5), compteur("t4", 880, 470, "t₄ =", 2, "orange", a=0.52),
      marque("T", "i", None, a=0.78), depose("cle", "T", 3, a=0.8))
T.dit("Le tableau est trié : deux, trois, six, huit. Et on a relevé t deux égale un, t trois égale trois, t quatre égale deux.",
      marque("T", "j", None), etat("T", [1, 2, 3, 4], "trie"), entoure("e2", 880, 330, 130, 190, "orange", a=0.5))

# ── Pourquoi des tⱼ ──────────────────────────────────────────────────────────
T.section("2. Pourquoi nommer les tⱼ")
T.dit("Maintenant, la question clé : pourquoi a-t-on besoin de ces t j ? Parce que le nombre de tests dépend des données.",
      efface(), ecrire("t", 100, 70, "Pourquoi nommer les tⱼ ?", "rouge", 46, gras=True, a=0.1))
T.dit("Sur un tableau déjà trié, chaque clé est déjà à sa place : un seul test par passage. "
      "Sur un tableau trié à l'envers, chaque clé doit remonter jusqu'au début : j tests au passage j.",
      cases("A", 120, 170, [1, 2, 3, 4], 66, a=0.05), etat("A", [1, 2, 3, 4], "trie", a=0.1),
      ecrire("la", 560, 180, "déjà trié : tⱼ = 1", "vert", 40, a=0.2),
      cases("B", 120, 330, [4, 3, 2, 1], 66, a=0.5), etat("B", [1, 2, 3, 4], "cle", a=0.55),
      ecrire("lb", 560, 340, "à l'envers : tⱼ = j", "rouge", 40, a=0.65))
T.dit("On ne peut donc pas écrire un seul nombre valable pour toutes les entrées de taille n. "
      "L'astuce, c'est de donner un nom à ce qu'on ne connaît pas encore : t j. On fait tout le calcul avec ce nom, et on remplace à la fin, cas par cas.",
      ecrire("as", 120, 500, "l'astuce : on nomme ce qui dépend des données", "bleu", 40, a=0.45))
T.dit("Et on sait déjà l'encadrer. Au moins un test, puisque le test est toujours fait une fois. "
      "Au plus j tests, puisque i part de j moins un et descend au pire jusqu'à zéro.",
      formule("enc", 120, 585, r"1 \le t_j \le j", "vert", 52, a=0.3))

# ── Compter ligne par ligne ──────────────────────────────────────────────────
T.section("3. Compter ligne par ligne")
T.dit("Passons au comptage. On reprend le pseudo-code, et pour chaque ligne, on se pose une seule question : combien de fois est-elle exécutée ?",
      efface(), code("C", 84, 70, PSEUDO, 25, compte=True, commentaires=[3], largeur=720, a=0.2))
T.dit("Commence par la ligne un, la boucle pour j égale deux à n. Combien de fois est-elle exécutée ? Réfléchis avant que je réponde.",
      hl("C", 1, a=0.1))
T.pause("Combien de fois la ligne 1, « Pour j = 2 à n », est-elle exécutée ?  Mets la vidéo en pause si tu as besoin de plus de temps.", 7)
T.dit("Beaucoup d'étudiants répondent n moins un, parce que j prend n moins un valeurs, de deux à n. "
      "Mais regarde ce que fait vraiment une boucle pour : avant chaque tour, elle teste si j est inférieur ou égal à n.",
      ecrire("r1", 840, 80, "j = 2, 3, …, n :", "bleu", 36, a=0.55),
      ecrire("r2", 860, 125, "test vrai, n − 1 fois", "bleu", 36, a=0.75))
T.dit("Puis j vaut n plus un. Le test est faux : c'est lui qui fait sortir de la boucle. Et ce test compte aussi ! Total : n.",
      ecrire("r3", 840, 185, "j = n + 1 : test faux", "rouge", 36, a=0.1),
      ecrire("r4", 860, 230, "on sort (il compte !)", "rouge", 36, a=0.35),
      ecrire("r5", 840, 290, "total : n", "vert", 42, gras=True, a=0.7), compte("C", 1, "n", a=0.75))
T.dit("Les lignes deux, quatre et huit sont dans le corps de la boucle pour, mais en dehors du tant que : "
      "elles s'exécutent une fois par passage, donc n moins un fois chacune.",
      efface(["r1", "r2", "r3", "r4", "r5"]), hl("C", [2, 4, 8], a=0.15),
      compte("C", 2, "n−1", a=0.7), compte("C", 4, "n−1", a=0.78), compte("C", 8, "n−1", a=0.86))
T.dit("La ligne trois est un commentaire : elle annonce ce que font les lignes suivantes, ce n'est pas une instruction. Elle ne coûte rien.",
      hl("C", 3, a=0.05), compte("C", 3, "0", a=0.7))
T.dit("La ligne cinq, c'est le test du tant que. Au passage j, il est fait t j fois, par définition. "
      "Sur tous les passages, ça fait la somme des t j, pour j allant de deux à n.",
      hl("C", 5, a=0.05), compte("C", 5, "Σ tⱼ", a=0.8),
      formule("s5", 850, 120, r"\sum_{j=2}^{n} t_j", "bleu", 44, a=0.8))
T.dit("Et les lignes six et sept ? Elles sont exécutées une fois par test vrai. Or, sur les t j tests, seul le dernier est faux. "
      "Donc t j moins un fois par passage, et au total, la somme des t j moins un.",
      efface(["s5"]), hl("C", [6, 7], a=0.05),
      ecrire("r6", 840, 90, "une fois par test vrai", "bleu", 36, a=0.25),
      formule("s6", 850, 150, r"t_j - 1 \text{ par passage}", "bleu", 34, a=0.55),
      compte("C", 6, "Σ(tⱼ−1)", a=0.85), compte("C", 7, "Σ(tⱼ−1)", a=0.9))
T.dit("Le tableau est complet. C'est lui que le correcteur veut voir sur ta copie, avec la justification des deux lignes délicates : la un, et les six et sept.",
      hl("C", None), efface(["r6", "s6"]), entoure("e3", 676, 76, 120, 262, "rouge", a=0.4))

# ── On additionne ────────────────────────────────────────────────────────────
T.section("4. On additionne")
T.dit("Chaque instruction simple coûte la même constante c, nous dit l'énoncé. On additionne donc les nombres d'exécutions, et on multiplie par c.",
      efface(), ecrire("t", 100, 70, "On additionne", "rouge", 46, gras=True),
      formule("F1", 100, 150, r"T(n) = c\Big[\, n + 3(n-1) + \displaystyle\sum_{j=2}^{n} t_j + 2\displaystyle\sum_{j=2}^{n}(t_j - 1)\Big]", "", 36, a=0.45, d=1.6))
T.dit("D'où vient le trois fois n moins un ? Des lignes deux, quatre et huit. Et le deux devant la dernière somme ? Des lignes six et sept.",
      ecrire("a1", 110, 292, "3(n − 1) : lignes 2, 4, 8", "gris", 34, a=0.25), ecrire("a2", 560, 292, "2 Σ(tⱼ − 1) : lignes 6 et 7", "gris", 34, a=0.7))
T.dit("Pour simplifier, une seule remarque. La somme des t j moins un, c'est la somme des t j, moins la somme des un. "
      "Et combien y a-t-il de termes quand j va de deux à n ? Exactement n moins un.",
      formule("F2", 100, 350, r"\displaystyle\sum_{j=2}^{n}(t_j - 1) = \sum_{j=2}^{n} t_j - (n-1)", "bleu", 36, a=0.35, d=1.4))
T.dit("On remplace, et on regroupe. n, plus trois fois n moins un, moins deux fois n moins un : il reste n plus n moins un, soit deux n moins un. "
      "Et devant la somme des t j, un plus deux, trois.",
      formule("F3", 100, 470, r"T(n) = c\,\Big(3\displaystyle\sum_{j=2}^{n} t_j + 2n - 1\Big)", "vert", 46, a=0.55, d=1.3, cadre="vert"))
T.dit("Vérifions sur notre exemple : c'est une habitude à prendre. n vaut quatre, et la somme des t j vaut un plus trois plus deux, six. "
      "Trois fois six, dix-huit ; plus huit moins un, sept : vingt-cinq c. L'animateur du site, qui compte les instructions une par une, trouve aussi vingt-cinq.",
      formule("F4", 100, 625, r"n = 4,\ \ \sum t_j = 1 + 3 + 2 = 6 \ \Rightarrow\ T(4) = c\,(18 + 7) = 25\,c", "bleu", 36, a=0.3, d=2.0))

# ── Le meilleur cas ──────────────────────────────────────────────────────────
T.section("5. Le meilleur cas")
T.dit("Il reste à remplacer les t j. D'abord le meilleur cas. Le coût augmente avec les t j : le meilleur cas, c'est quand chaque t j est le plus petit possible, t j égale un.",
      efface(), ecrire("t", 100, 70, "Meilleur cas", "rouge", 46, gras=True),
      formule("m1", 100, 150, r"t_j = 1 \ \text{ pour tout } j", "bleu", 42, a=0.75))
T.dit("Quand est-ce que ça arrive ? Quand le premier test est faux à chaque passage, c'est-à-dire quand la case de gauche n'est jamais plus grande que la clé. "
      "C'est exactement un tableau déjà trié.",
      cases("A", 640, 140, [1, 2, 3, 4, 5], 60, indices=False, a=0.6), etat("A", [1, 2, 3, 4, 5], "trie", a=0.65))
T.dit("Alors la somme des t j, c'est n moins un fois un : n moins un. On remplace : trois fois n moins un, plus deux n moins un. Ça fait cinq n moins quatre.",
      formule("m2", 100, 250, r"\displaystyle\sum_{j=2}^{n} t_j = n - 1", "bleu", 40, a=0.2),
      formule("m3", 100, 370, r"T_{\min}(n) = c\big(3(n-1) + 2n - 1\big) = c\,(5n - 4)", "vert", 44, a=0.6, d=1.4, cadre="vert"))
T.dit("Cinq n moins quatre est une fonction affine de n. Si n double, le coût double, à peu près. On dit que le coût est linéaire, et on écrira grand thêta de n.",
      formule("m4", 100, 490, r"T_{\min}(n) = \Theta(n)", "vert", 48, a=0.55), ecrire("m5", 560, 495, "linéaire", "vert", 46, gras=True, a=0.75))

# ── Le pire cas ──────────────────────────────────────────────────────────────
T.section("6. Le pire cas")
T.dit("Le pire cas, maintenant : chaque t j le plus grand possible, t j égale j. Il faut que chaque clé remonte jusqu'au tout début, en étant comparée à tous les éléments avant elle.",
      efface(), ecrire("t", 100, 70, "Pire cas", "rouge", 46, gras=True), formule("p1", 100, 150, r"t_j = j", "bleu", 44, a=0.3))
T.dit("Ça arrive quand chaque clé est plus petite que tout ce qui la précède : le tableau trié à l'envers. "
      "Regarde le dernier passage : le un doit passer devant le quatre, le trois et le deux. Quatre tests, pour j égale quatre.",
      cases("B", 640, 150, [2, 3, 4, 1], 70, a=0.15), etat("B", [1, 2, 3], "trie", a=0.2), etat("B", 4, "cle", a=0.2),
      fleche("f1", 940, 150, 675, 150, "rouge", courbe=60, a=0.6, d=1.0),
      compteur("t4", 1010, 260, "t₄ =", 4, "orange", a=0.85))
T.dit("Il faut alors calculer la somme des j, pour j allant de deux à n. C'est le seul calcul délicat. "
      "On connaît la somme de un à n : n fois n plus un, sur deux. Il manque juste le terme j égale un : on le retire.",
      formule("p2", 100, 300, r"\displaystyle\sum_{j=1}^{n} j = \frac{n(n+1)}{2}", "bleu", 40, a=0.45),
      formule("p3", 560, 300, r"\displaystyle\sum_{j=2}^{n} j = \frac{n(n+1)}{2} - 1", "bleu", 40, a=0.8))
T.dit("Attention au piège : beaucoup oublient ce moins un. Il ne change pas l'ordre de grandeur, mais le résultat devient faux, et le correcteur le voit.",
      efface(["p3"], a=0.15, d=0.01),
      formule("p3r", 560, 300, r"\displaystyle\sum_{j=2}^{n} j = \frac{n(n+1)}{2} \textcolor{#bd1f2b}{\boxed{\,-\,1\,}}", "bleu", 40, a=0.15, d=0.01),
      ecrire("pg", 560, 452, "piège : ne pas oublier le − 1", "rouge", 36, a=0.35))
T.dit("On remplace dans la formule, et on développe : trois n carré sur deux, plus sept n sur deux, moins quatre.",
      formule("p4", 100, 510, r"T_{\max}(n) = c\Big(3\big(\tfrac{n(n+1)}{2} - 1\big) + 2n - 1\Big) = c\Big(\tfrac{3n^2}{2} + \tfrac{7n}{2} - 4\Big)", "vert", 38, a=0.2, d=2.0, cadre="vert"))
T.dit("Le terme qui domine, c'est n carré. Si n double, le coût est multiplié par quatre, à peu près. Le coût est quadratique : grand thêta de n carré.",
      formule("p5", 100, 625, r"T_{\max}(n) = \Theta(n^2)", "vert", 48, a=0.5), ecrire("p6", 560, 630, "quadratique", "vert", 46, gras=True, a=0.75))

# ── Ce que ça change ─────────────────────────────────────────────────────────
T.section("7. Ce qu'il faut retenir")
T.dit("Pour sentir la différence, prenons mille éléments. Déjà triés : environ cinq mille c. Triés à l'envers : environ un million et demi de c. "
      "Le même algorithme, trois cents fois plus lent, selon l'ordre dans lequel arrivent les données.",
      efface(), ecrire("t", 100, 70, "Pour n = 1000", "rouge", 46, gras=True),
      formule("c1", 120, 160, r"T_{\min}(1000) = 4\,996\,c \approx 5\,000\,c", "vert", 40, a=0.3),
      formule("c2", 120, 250, r"T_{\max}(1000) = 1\,503\,496\,c \approx 1{,}5 \text{ million de } c", "rouge", 40, a=0.55),
      ecrire("c3", 120, 340, "× 300 selon l'ordre des données", "rouge", 40, gras=True, a=0.85))
T.dit("Récapitulons la méthode, parce que c'est elle que tu réutiliseras pour n'importe quel algorithme. "
      "Un : nommer ce qui dépend des données, ici les t j. Deux : compter les exécutions de chaque ligne. "
      "Trois : additionner et simplifier. Quatre : remplacer, dans le meilleur et dans le pire cas.",
      efface(["c1", "c2", "c3"], a=0.0), ecrire("t2", 100, 70, "La méthode", "rouge", 46, gras=True, a=0.05),
      efface(["t"], a=0.02),
      ecrire("k1", 130, 160, "1. nommer ce qui dépend des données (tⱼ)", "bleu", 40, a=0.3),
      ecrire("k2", 130, 225, "2. compter les exécutions de chaque ligne", "bleu", 40, a=0.52),
      ecrire("k3", 130, 290, "3. additionner et simplifier", "bleu", 40, a=0.7),
      ecrire("k4", 130, 355, "4. remplacer : meilleur cas, pire cas", "bleu", 40, a=0.84))
T.dit("À toi, maintenant : fais tourner l'animateur du site sur tes propres tableaux, puis code le tri dans l'atelier. "
      "La mesure te montrera la droite et la parabole, obtenues avec ton propre code.",
      ecrire("k5", 130, 460, "→ l'animateur, l'atelier, la mesure", "vert", 42, gras=True, a=0.3))

TUTO = T
