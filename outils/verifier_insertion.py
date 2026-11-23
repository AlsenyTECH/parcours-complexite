# -*- coding: utf-8 -*-
"""Vérifie par simulation tous les nombres annoncés dans l'étape 3.3 (tri par insertion).

    python3 outils/verifier_insertion.py

Simule le pseudo-code de l'annale ligne par ligne (tableau indexé de 1 à n, ligne 3 gratuite)
et compare aux formules du cours. Toute différence fait échouer le script.
"""
import itertools
from fractions import Fraction


def simule(T0):
    T = [None] + list(T0)
    n = len(T0)
    cpt = [0] * 9
    tj = {}
    j = 2
    while True:
        cpt[1] += 1
        if j > n:
            break
        cle = T[j]; cpt[2] += 1
        i = j - 1; cpt[4] += 1
        t = 0
        while True:
            cpt[5] += 1; t += 1
            if not (i > 0 and T[i] > cle):
                break
            T[i + 1] = T[i]; cpt[6] += 1
            i -= 1; cpt[7] += 1
        T[i + 1] = cle; cpt[8] += 1
        tj[j] = t
        j += 1
    return T[1:], sum(cpt), tj, cpt[6]


def inversions(T):
    return sum(1 for a, b in itertools.combinations(range(len(T)), 2) if T[a] > T[b])


T, cout, tj, _ = simule([3, 8, 2, 6])
assert T == [2, 3, 6, 8] and tj == {2: 1, 3: 3, 4: 2} and cout == 25, (T, tj, cout)

for n in range(1, 9):
    _, c_min, _, _ = simule(range(n))
    _, c_max, _, _ = simule(range(n, 0, -1))
    assert c_min == 5 * n - 4
    assert Fraction(c_max) == Fraction(3 * n * n, 2) + Fraction(7 * n, 2) - 4
    if n <= 7:
        perms = list(itertools.permutations(range(n)))
        for p in perms:
            _, c, t, dec = simule(p)
            assert c == 3 * sum(t.values()) + 2 * n - 1          # T(n) = c(3 Σ tj + 2n − 1)
            assert dec == inversions(p)                           # décalages = inversions
        moy = Fraction(sum(simule(p)[1] for p in perms), len(perms))
        assert moy == Fraction(3 * n * n, 4) + Fraction(17 * n, 4) - 4, (n, moy)
        moy_t = Fraction(sum(sum(simule(p)[2].values()) for p in perms), len(perms))
        assert moy_t == Fraction(n * n + 3 * n - 4, 4)

# valeurs des tests de l'atelier (nombre d'évaluations de la ligne 5)
for T0, attendu in [([], 0), ([5], 0), (list(range(1, 11)), 9), (list(range(10, 0, -1)), 54),
                    ([2, 2, 2], 2), ([4, 2, 4, 1, 3], 10), ([9, -3, 0, 7, -3, 12, 5, 1], 20)]:
    got = sum(simule(T0)[2].values())
    assert got == attendu, (T0, got, attendu)

print("Tous les nombres de l'étape 3.3 sont vérifiés.")
