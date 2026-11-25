# -*- coding: utf-8 -*-
"""Le registre du parcours : 10 modules, leurs étapes, dans l'ordre où on les apprend.

Une étape ajoutée ici apparaît automatiquement dans l'accueil, dans le sommaire de son module
et dans la liste « prérequis » des étapes qui la citent. Le cours d'une étape se rédige dans
contenu/moduleN.py (dictionnaire CORPS) ; tant qu'il n'existe pas, la page affiche la fiche de l'étape.
"""


class Etape:
    def __init__(self, ident, titre, minutes, objectif, prereq=(), examen=None, cours=None):
        self.id = ident
        self.titre = titre
        self.minutes = minutes
        self.objectif = objectif        # « ce qu'on doit savoir faire » à la fin
        self.prereq = list(prereq)
        self.examen = examen            # question d'annale que l'étape prépare, s'il y en a
        self.cours = cours              # partie correspondante du cours de complexité de l'UCAD
        self.corps = None               # rempli par build.py depuis contenu/moduleN.py
        self.video = None


class Module:
    def __init__(self, num, titre, resume, etapes):
        self.num = num
        self.titre = titre
        self.resume = resume
        self.etapes = etapes
        self.fichier = "module-%d.html" % num


E = Etape
MODULES = [
    Module(0, "Pourquoi la complexité", "Deux algorithmes justes peuvent différer d'un facteur un milliard. Mesurer, c'est choisir.", [
        E("m0-deux-algos", "Deux algorithmes, un même problème", 25,
          "Comparer recherche séquentielle et dichotomique sur un million de valeurs, et dire pourquoi l'une gagne.",
          cours="Cours 1, Introduction"),
        E("m0-attaque", "Ce que coûte une attaque", 25,
          "Estimer le temps d'une recherche exhaustive de clé et comprendre pourquoi 128 bits suffisent.",
          ["m0-deux-algos"]),
    ]),
    Module(1, "Mesurer un algorithme", "Opérations élémentaires, taille de l'entrée, pire, meilleur et moyen cas.", [
        E("m1-modele", "Le coût d'un algorithme : ce qu'on compte", 35,
          "Distinguer complexité expérimentale et théorique, temporelle et spatiale ; choisir l'opération élémentaire selon le problème (comparaison, affectation, addition, multiplication) ; justifier un coût constant c par instruction simple.",
          ["m0-deux-algos"], cours="Cours 3, Coût d'un algorithme et Règle de calcul"),
        E("m1-taille", "La taille de l'entrée, en bits", 35,
          "Choisir la taille d'une entrée (entier en bits, tableau, matrice, polynôme, arbre, graphe, mot) ; repérer le piège des algorithmes linéaires en n mais exponentiels en la taille de n.",
          ["m1-modele"], cours="Cours 3, Taille des données ; Cours 1, Fonctions entières"),
        E("m1-cas", "Pire, meilleur et moyen cas", 40,
          "Définir les trois complexités, distinguer complexité asymptotique et non asymptotique, et les calculer sur un exemple simple.",
          ["m1-taille"], examen="Annale 2024-2025, ex. 1, questions 4 à 6", cours="Cours 3, Types de complexité"),
        E("m1-espace", "La complexité en espace", 25,
          "Compter la mémoire utilisée, y compris la pile des appels récursifs.",
          ["m1-cas"]),
    ]),
    Module(2, "Les notations asymptotiques", "O, Ω, Θ : comparer des fonctions sans se perdre dans les constantes.", [
        E("m2-grand-o", "La notation O", 40,
          "Démontrer f = O(g) avec des constantes c et n₀ explicites.", ["m1-cas"], cours="Cours 1, Notation asymptotique (O)"),
        E("m2-omega-theta", "Ω et Θ", 35,
          "Démontrer un encadrement Θ et savoir ce qu'il apporte de plus qu'un O.", ["m2-grand-o"],
          cours="Cours 1, Notation asymptotique (Θ, Ω)"),
        E("m2-petit-o", "Les notations o, ω et ∼", 40,
          "Démontrer f = o(g), f = ω(g) et f ∼ g par la limite de f/g ; utiliser réflexivité, symétrie, symétrie transposée et transitivité.",
          ["m2-omega-theta"], cours="Cours 1, Notation asymptotique (o, ω, ∼) et propriétés"),
        E("m2-croissances", "Croissances comparées et classes de complexité", 40,
          "Démontrer la hiérarchie O(1) ⊂ O(log n) ⊂ O(√n) ⊂ O(n) ⊂ O(n log n) ⊂ O(n²) ⊂ … ⊂ O(2ⁿ) et nommer chaque classe (constant, logarithmique, linéaire, quasi-linéaire, quadratique, polynomial, exponentiel).",
          ["m2-petit-o"], cours="Cours 3, Classification des complexités ; Cours 1, Fonctions de référence"),
        E("m2-regles", "Règles de calcul", 30,
          "Utiliser O(f₁ + f₂) = O(max(f₁, f₂)), O(af) = O(f), O(f₁f₂) = O(f₁)O(f₂) et le critère par la limite, et éviter les abus classiques.",
          ["m2-croissances"], cours="Cours 1, Propriétés"),
        E("m2-sommes", "Sommes classiques", 40,
          "Calculer ou encadrer Σ k, Σ k², Σ log k, Σ 1/k, notamment par comparaison avec une intégrale.",
          ["m2-regles"]),
    ]),
    Module(3, "Analyser un algorithme itératif", "La méthode ligne par ligne, appliquée aux recherches et aux tris.", [
        E("m3-methode", "Les règles de calcul : séquence, conditionnelle, boucles", 45,
          "Appliquer T₁ + T₂ (séquence), T_c + max(T₁, T₂) (si… sinon), les formules des boucles tant que, faire… tant que et pour, puis dresser le tableau ligne par ligne.",
          ["m2-sommes"], cours="Cours 3, Exécution séquentielle, conditionnelle, boucles"),
        E("m3-recherche", "La recherche séquentielle", 35,
          "Calculer le coût de la recherche séquentielle au meilleur, au pire et en moyenne.",
          ["m3-methode"], examen="Annale 2024-2025, ex. 3", cours="Cours 3, Algorithm 3 (Test)"),
        E("m3-insertion", "Le tri par insertion", 60,
          "Faire tourner le tri par insertion à la main, exprimer T(n) en fonction des tⱼ, puis T_min(n), T_max(n) et le coût moyen.",
          ["m3-methode"], examen="Annale 2024-2025, ex. 2", cours="Cours 3, Tri insertion"),
        E("m3-selection-bulles", "Tri par sélection et tri à bulles", 40,
          "Analyser deux autres tris quadratiques et les comparer au tri par insertion.",
          ["m3-insertion"]),
        E("m3-imbriquees", "Boucles imbriquées dépendantes", 35,
          "Calculer le coût de boucles imbriquées, y compris quand les bornes dépendent les unes des autres (Test2, produit matrice-vecteur en 2mn − m opérations).",
          ["m3-methode"], cours="Cours 3, Test1 et Test2 ; Cours 1, Produit matrice-vecteur"),
        E("m3-dichotomie", "La recherche dichotomique", 40,
          "Démontrer que la dichotomie fait au plus ⌊log₂ n⌋ + 1 comparaisons.",
          ["m3-recherche"]),
    ]),
    Module(4, "Les algorithmes récursifs", "Équations de récurrence, diviser pour régner, théorème maître.", [
        E("m4-factorielle", "Une première récurrence : la factorielle", 30,
          "Poser T(n) = T(n−1) + c, la résoudre, et compter les multiplications.",
          ["m3-methode"], examen="Annale 2024-2025, ex. 4", cours="Cours 3, Factorial récursive"),
        E("m4-puissance", "La puissance rapide récursive", 40,
          "Écrire la récurrence de Puissance(x, n) et démontrer qu'elle fait au plus 2 log₂ n multiplications.",
          ["m4-factorielle"], cours="Cours 3, Puissance rapide"),
        E("m4-lineaires", "Récurrences linéaires : Hanoï et Fibonacci", 45,
          "Résoudre T(n) = 2T(n−1) + 1 et T(n) = T(n−1) + T(n−2) + 1, et voir l'explosion exponentielle.",
          ["m4-factorielle"], cours="Cours 3, Fibonacci"),
        E("m4-diviser", "Diviser pour régner : le tri fusion", 50,
          "Analyser la procédure Fusion (avec sentinelles), écrire la récurrence du tri fusion et démontrer T(n) = Θ(n log n).",
          ["m4-lineaires", "m3-insertion"], cours="Cours 3, Diviser pour régner, Tri fusion"),
        E("m4-maitre", "Le théorème maître", 50,
          "Appliquer le théorème maître aux trois cas, et reconnaître quand il ne s'applique pas.",
          ["m4-diviser"]),
        E("m4-arbre", "Arbre des appels et méthode de substitution", 40,
          "Deviner une solution avec l'arbre des appels, puis la démontrer par récurrence.",
          ["m4-maitre"], cours="Cours 3, Résolution de l'équation récursive"),
    ]),
    Module(5, "Les algorithmes arithmétiques", "Le coût des opérations sur les grands entiers : le cœur de la cryptographie.", [
        E("m5-operations", "Addition et multiplication en bits", 35,
          "Compter les opérations binaires d'une addition (O(k)) et d'une multiplication scolaire (O(k²)).",
          ["m1-taille", "m2-regles"]),
        E("m5-karatsuba", "La multiplication de Karatsuba", 45,
          "Établir T(k) = 3T(k/2) + O(k) et en déduire O(k^{log₂ 3}).",
          ["m5-operations", "m4-maitre"]),
        E("m5-euclide", "Euclide et le théorème de Lamé", 45,
          "Démontrer que l'algorithme d'Euclide fait O(log b) divisions.",
          ["m5-operations"]),
        E("m5-euclide-etendu", "Euclide étendu et inverse modulaire", 35,
          "Calculer un inverse modulaire et majorer le coût en O(k²) opérations binaires.",
          ["m5-euclide"]),
        E("m5-exponentiation", "L'exponentiation modulaire rapide", 45,
          "Calculer aᵉ mod n en au plus 2⌊log₂ e⌋ multiplications, et en déduire le coût en bits.",
          ["m5-operations", "m4-puissance"]),
        E("m5-chinois", "Les restes chinois", 35,
          "Reconstruire x à partir de ses restes et en estimer le coût.",
          ["m5-euclide-etendu"]),
        E("m5-primalite", "Tests de primalité", 45,
          "Estimer le coût de la division d'essai, de Fermat et de Miller-Rabin, et dire pourquoi seul le dernier est utilisé.",
          ["m5-exponentiation"]),
    ]),
    Module(6, "Les classes de complexité", "P, NP, co-NP, réductions et NP-complétude.", [
        E("m6-decision", "Problèmes de décision et classe P", 35,
          "Formuler un problème de décision, justifier qu'il est dans P, et savoir ce que veulent dire « algorithme efficace » et « problème traitable ou intraitable ».",
          ["m1-taille"], cours="Cours 3, Algorithme efficace et problème intraitable"),
        E("m6-np", "NP et les certificats", 40,
          "Montrer qu'un problème est dans NP en exhibant un certificat vérifiable en temps polynomial.",
          ["m6-decision"], examen="Annale 2024-2025, ex. 1"),
        E("m6-conp", "co-NP et les questions ouvertes", 30,
          "Placer un problème dans co-NP et énoncer les questions P = NP et NP = co-NP.", ["m6-np"]),
        E("m6-reductions", "Les réductions polynomiales", 45,
          "Rédiger une réduction polynomiale et en tirer une conséquence.",
          ["m6-np"], examen="Annale 2024-2025, ex. 1, question 3"),
        E("m6-np-complet", "NP-complétude et NP-difficulté", 45,
          "Définir NP-complet, P-complet et NP-difficile, et démontrer qu'un problème est NP-complet par réduction.",
          ["m6-reductions"], examen="Annale 2024-2025, ex. 1, questions 1 et 2"),
        E("m6-crypto", "Des problèmes NP-complets en cryptographie", 40,
          "Citer et énoncer le sac à dos et le décodage d'un code linéaire, et savoir pourquoi la factorisation n'en fait pas partie.",
          ["m6-np-complet"], examen="Annale 2024-2025, ex. 1, questions 7 et 8"),
    ]),
    Module(7, "Complexité et cryptographie", "Exponentiel, sous-exponentiel, et ce que cela dit de la taille des clés.", [
        E("m7-sous-exp", "Polynomial, exponentiel, sous-exponentiel", 40,
          "Lire la notation L_q[α, c] et situer un algorithme entre polynomial et exponentiel.",
          ["m2-croissances", "m1-taille"]),
        E("m7-factorisation", "Factoriser : de la division d'essai au crible", 45,
          "Comparer le coût de la division d'essai, de Pollard ρ et du crible algébrique.",
          ["m7-sous-exp", "m5-primalite"]),
        E("m7-log-discret", "Le logarithme discret", 45,
          "Analyser pas de bébé–pas de géant et Pollard ρ en O(√q), et voir Pohlig-Hellman.",
          ["m7-sous-exp", "m5-exponentiation"]),
        E("m7-niveaux", "Taille des clés et niveaux de sécurité", 35,
          "Traduire un niveau de sécurité de k bits en taille de clé RSA, de groupe et de courbe.",
          ["m7-factorisation", "m7-log-discret"]),
        E("m7-shannon", "La sécurité inconditionnelle de Shannon", 40,
          "Démontrer que le masque jetable est parfaitement sûr et que |K| ≥ |P| est nécessaire.",
          ["m1-cas"]),
        E("m7-reduction", "Sécurité réductionniste et oracle aléatoire", 45,
          "Expliquer une preuve par réduction et ce que garantit (ou non) le modèle de l'oracle aléatoire.",
          ["m6-reductions", "m7-shannon"]),
    ]),
    Module(8, "Études de cas : les algorithmes des exposés", "Pour un algorithme donné : le coût de chaque opération, la meilleure attaque, la taille de clé.", [
        E("m8-methode", "La méthode pour analyser un algorithme inconnu", 40,
          "Appliquer une grille en cinq questions à n'importe quel algorithme, avant d'écrire un seul calcul.",
          ["m3-insertion", "m4-maitre", "m5-exponentiation"]),
        E("m8-rsa", "RSA", 50,
          "Calculer le coût de la génération des clés, du chiffrement et du déchiffrement (avec et sans restes chinois), et celui des attaques.",
          ["m8-methode", "m5-chinois", "m7-factorisation"]),
        E("m8-diffie-hellman", "Diffie-Hellman", 45,
          "Calculer le coût de l'échange et relier sa sécurité au logarithme discret.",
          ["m8-methode", "m7-log-discret"]),
        E("m8-elgamal", "ElGamal", 45,
          "Calculer le coût du chiffrement et du déchiffrement, et la taille du chiffré.",
          ["m8-diffie-hellman"]),
        E("m8-aes", "AES", 45,
          "Compter les opérations d'un chiffrement AES et expliquer pourquoi la seule attaque générique est en 2^k.",
          ["m8-methode", "m0-attaque"]),
    ]),
    Module(9, "Préparer l'examen", "Méthode, annales corrigées, évaluations chronométrées.", [
        E("m9-correcteur", "Ce que le correcteur attend", 25,
          "Rédiger une analyse de complexité complète : modèle, calcul, conclusion asymptotique."),
        E("m9-annale-2025", "Annale 2024-2025 corrigée", 150,
          "Traiter l'épreuve complète en 2 h 30, puis comparer avec la correction.",
          ["m3-insertion", "m3-recherche", "m4-factorielle", "m6-crypto"]),
        E("m9-eval-calculs", "Évaluation chronométrée : calculs de complexité", 30,
          "Analyser trois algorithmes en 30 minutes."),
        E("m9-eval-cours", "Évaluation chronométrée : cours et classes", 20,
          "Restituer les définitions et les exemples du cours en 20 minutes."),
    ]),
]

INDEX = {}
for _m in MODULES:
    for _e in _m.etapes:
        INDEX[_e.id] = (_e, _m)


def verifier():
    """Chaque prérequis existe et vient avant l'étape qui le cite (dans l'ordre du parcours)."""
    ordre = [e.id for m in MODULES for e in m.etapes]
    pbs = []
    if len(ordre) != len(set(ordre)):
        pbs.append("identifiant d'étape en double")
    for i, eid in enumerate(ordre):
        for p in INDEX[eid][0].prereq:
            if p not in INDEX:
                pbs.append("%s : prérequis inconnu %s" % (eid, p))
            elif ordre.index(p) >= i:
                pbs.append("%s : le prérequis %s vient après" % (eid, p))
    return pbs


def numero(eid):
    e, m = INDEX[eid]
    return "%d.%d" % (m.num, m.etapes.index(e) + 1)
