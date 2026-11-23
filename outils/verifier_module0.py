# -*- coding: utf-8 -*-
"""Vérifie les nombres du module 0 et exécute les corrigés des ateliers contre leurs tests.

    python3 outils/verifier_module0.py
"""
import math, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "contenu"))
import module0  # noqa: E402


def dicho(T, x):
    g, d, t = 0, len(T) - 1, 0
    while g <= d:
        t += 1
        m = (g + d) // 2
        if T[m] == x:
            return True, t
        if T[m] < x:
            g = m + 1
        else:
            d = m - 1
    return False, t


# borne de la dichotomie : exactement floor(log2 n) + 1 au pire, atteinte pour x > max
for n in range(1, 2000):
    T = list(range(0, 2 * n, 2))
    pire = max(dicho(T, x)[1] for x in range(-1, 2 * n + 1))
    assert pire == math.floor(math.log2(n)) + 1 == dicho(T, 2 * n)[1], n
for n, b in [(10, 4), (1000, 10), (1024, 11), (10**6, 20), (10**9, 30), (8 * 10**9, 33), (100, 7)]:
    assert math.floor(math.log2(n)) + 1 == b, (n, b)

# tableaux du cours (temps moyens)
AN = 3.15576e7
def duree(bits, v):
    return 2 ** (bits - 1) / v
assert abs(duree(40, 1e9) / 60 - 9.2) < 0.1
assert abs(duree(56, 1e12) / 3600 - 10.0) < 0.1
assert abs(duree(64, 1e12) / 86400 - 106.8) < 0.5
assert abs(duree(80, 1e18) / 86400 - 7.0) < 0.05
assert 2 ** 127 / 1e18 / AN / 1.38e10 > 300
assert math.ceil(math.log2(1e21 * 1000 * AN) + 1) == 106
assert abs(26 ** 8 / 1e10 - 20.9) < 0.1 and abs(94 ** 12 / 1e10 / AN / 1e6 - 1.5) < 0.05
assert math.ceil(math.log2(2 ** 80 / 1e18 / 86400)) == 4

# corrigés des ateliers contre leurs tests
def corrige(html_):
    src = re.search(r'<pre class="pseudo">(.*?)</pre>', html_, re.S).group(1)
    return src.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")

for eid, depart_fn in [("m0-deux-algos", None), ("m0-attaque", "chiffrer")]:
    page = module0.CORPS[eid]
    bloc = re.search(r'<div class="atelier".*?</details></div>', page, re.S).group(0)
    ns = {}
    if depart_fn:
        depart = re.search(r'<textarea[^>]*>(.*?)</textarea>', bloc, re.S).group(1)
        depart = depart.replace("&#x27;", "'").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        exec(depart.split("def attaque")[0], ns)
    exec(corrige(bloc.split('atelier-corrige')[1]), ns)
    import json, html
    tests = json.loads(html.unescape(re.search(r'<script type="application/json" class="atelier-tests">(.*?)</script>', bloc, re.S).group(1)).replace("<\\/", "</"))
    for t in tests:
        r = eval(t["appel"], ns)
        env = dict(ns); env["r"] = r
        assert eval(t["verif"], env), (eid, t["appel"], r)
print("Module 0 : nombres et corrigés vérifiés.")
