# -*- coding: utf-8 -*-
"""Moteur des tutos vidéo « au tableau » du Parcours Complexité.

Un tuto s'écrit en Python (outils/video/tutos/<nom>.py) comme une suite de répliques :
chaque réplique est une phrase dite par la voix, accompagnée des gestes faits au tableau
pendant qu'elle est prononcée (écrire, dessiner un tableau de cases, déplacer une valeur,
surligner une ligne de pseudo-code, remplir un tableau, tracer une flèche…).

    KOKORO_DIR=/chemin/modeles python3 outils/video/tuto.py outils/video/tutos/m3-insertion.py

Étapes : voix de chaque réplique (Kokoro) → minutage des gestes → capture image par image
de tuto.html (Playwright) → assemblage ffmpeg → sous-titres WebVTT.
Sorties : videos/<nom>.mp4 et .vtt.

Règles d'écriture d'un bon tuto (voir README) : une question pour commencer, un exemple
travaillé au tableau avant toute formule, le « pourquoi » de chaque étape, les erreurs
classiques, au moins une pause « à toi », un bilan court.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
IPS = 20


# ─────────────────────────────────────────────────────────────────────────────
# Les gestes. Chacun renvoie un dict ; `a` = moment du début dans la réplique (0 → début,
# 1 → fin de la phrase), `d` = durée de l'animation en secondes.
# ─────────────────────────────────────────────────────────────────────────────
def _g(type_, a=0.0, d=0.6, **k):
    k.update(type=type_, a=a, d=d)
    return k


def ecrire(id, x, y, texte, couleur="bleu", taille=44, a=0.0, d=None, gras=False, souligne=False):
    return _g("ecrire", a, d if d is not None else max(0.5, 0.045 * len(texte)), id=id, x=x, y=y, texte=texte,
              couleur=couleur, taille=taille, gras=gras, souligne=souligne)


def formule(id, x, y, tex, couleur="", taille=34, a=0.0, d=1.0, cadre=None):
    return _g("formule", a, d, id=id, x=x, y=y, tex=tex, couleur=couleur, taille=taille, cadre=cadre)


def cases(id, x, y, valeurs, taille=76, a=0.0, d=0.5, indices=True, premier=None):
    return _g("cases", a, d, id=id, x=x, y=y, valeurs=valeurs, taille=taille, indices=indices, premier=premier)


def valeur(id, i, v, a=0.0, d=0.6):
    return _g("valeur", a, d, id=id, i=i, v=v)


def etat(id, i, style, a=0.0):
    return _g("etat", a, 0, id=id, i=list(i) if isinstance(i, (list, tuple, range)) else [i], style=style)


def marque(id, texte, i, couleur="#1c3bb0", rang=0, a=0.0):
    return _g("marque", a, 0, id=id, texte=texte, i=i, couleur=couleur, rang=rang)


def glisse(id, de, vers, a=0.0, d=0.9):
    return _g("glisse", a, d, id=id, de=de, vers=vers)


def boite(id, x, y, label, valeur=None, a=0.0, d=0.5):
    return _g("boite", a, d, id=id, x=x, y=y, label=label, valeur=valeur)


def extrait(cases_, i, boite_, a=0.0, d=1.0):
    return _g("extrait", a, d, id=None, cases=cases_, i=i, boite=boite_)


def depose(boite_, cases_, i, a=0.0, d=1.0, style="trie"):
    return _g("depose", a, d, id=None, cases=cases_, i=i, boite=boite_, style=style)


def code(id, x, y, lignes, taille=22, compte=False, commentaires=(), largeur=None, a=0.0, d=0.5):
    return _g("code", a, d, id=id, x=x, y=y, lignes=lignes, taille=taille, compte=compte,
              commentaires=list(commentaires), largeur=largeur)


def hl(id, n, a=0.0):
    return _g("hl", a, 0, id=id, n=n)


def compte(id, n, v, a=0.0, d=0.5):
    return _g("compte", a, d, id=id, n=n, v=v)


def table(id, x, y, entetes, lignes, largeurs=None, taille=None, a=0.0, d=0.5):
    return _g("table", a, d, id=id, x=x, y=y, entetes=entetes, lignes=lignes, largeurs=largeurs, taille=taille)


def cellule(id, r, c, texte, couleur=None, fond=None, a=0.0, d=0.5):
    return _g("cellule", a, d, id=id, r=r, c=c, texte=texte, couleur=couleur, fond=fond)


def compteur(id, x, y, label, valeur, couleur="bleu", a=0.0, d=0.6):
    return _g("compteur", a, d, id=id, x=x, y=y, label=label, valeur=valeur, couleur=couleur)


def fleche(id, x1, y1, x2, y2, couleur="rouge", courbe=0, a=0.0, d=0.7, epaisseur=4):
    return _g("fleche", a, d, id=id, x1=x1, y1=y1, x2=x2, y2=y2, couleur=couleur, courbe=courbe, epaisseur=epaisseur)


def trait(id, x1, y1, x2, y2, couleur="rouge", a=0.0, d=0.5, epaisseur=4):
    return _g("trait", a, d, id=id, x1=x1, y1=y1, x2=x2, y2=y2, couleur=couleur, courbe=0, epaisseur=epaisseur)


def entoure(id, x, y, w, h, couleur="rouge", a=0.0, d=0.7):
    return _g("entoure", a, d, id=id, x=x, y=y, w=w, h=h, couleur=couleur)


def efface(ids="tout", garder=(), a=0.0, d=0.5):
    return _g("efface", a, d, id=None, ids=ids if ids == "tout" else list(ids), garder=list(garder))


# ─────────────────────────────────────────────────────────────────────────────
class Tuto:
    def __init__(self, nom, titre):
        self.nom, self.titre = nom, titre
        self.repliques = []
        self._section = ""

    def section(self, titre):
        self._section = titre

    def dit(self, texte, *gestes, apres=0.35):
        """Une phrase de la voix, et les gestes faits pendant qu'elle est dite."""
        self.repliques.append({"type": "voix", "texte": texte, "gestes": list(gestes),
                               "section": self._section, "apres": apres})

    def fait(self, *gestes, duree=1.0):
        """Des gestes sans parole (le temps d'une animation)."""
        self.repliques.append({"type": "silence", "texte": "", "gestes": list(gestes),
                               "section": self._section, "duree": duree, "apres": 0})

    def pause(self, texte, secondes=6, titre="À toi !"):
        """Un temps pour chercher : un encadré avec un compte à rebours."""
        self.repliques.append({"type": "pause", "texte": texte, "titre": titre, "gestes": [],
                               "section": self._section, "duree": secondes, "apres": 0.2})


def parle(texte):
    """Corrections de prononciation pour la voix de synthèse."""
    r = texte
    for a, b in [("tⱼ", "t j"), ("T(n)", "T de n"), ("Σ", "somme"), ("≤", "inférieur ou égal à"), ("n−1", "n moins un"),
                 ("−", " moins "), ("×", " fois "), ("Tmin", "T min"), ("Tmax", "T max")]:
        r = r.replace(a, b)
    return re.sub(r"\s+", " ", r).strip()


def horodatage(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return "%02d:%02d:%06.3f" % (h, m, s)


def decouper(texte, maxi=90):
    """Sous-titres lisibles : on coupe d'abord aux fins de phrase, puis aux virgules, puis entre les mots ;
    un bout trop court est recollé au précédent."""
    phrases = re.findall(r"[^.!?;:]+[.!?;:»]*\s*", texte) or [texte]
    res = []
    for ph in (p.strip() for p in phrases):
        if not ph:
            continue
        while len(ph) > maxi:
            k = ph.rfind(", ", 0, maxi)
            if k < maxi // 3:
                k = ph.rfind(" ", 0, maxi)
            res.append(ph[:k + 1].strip())
            ph = ph[k + 1:].strip()
        res.append(ph)
    fus = []
    for r in res:
        if fus and (len(r) < 22 or len(fus[-1]) < 22) and len(fus[-1]) + len(r) + 1 <= maxi + 20:
            fus[-1] += " " + r
        else:
            fus.append(r)
    return fus


def ecrire_vtt(chemin, cues):
    lignes, n = ["WEBVTT", ""], 1
    for debut, duree, texte in cues:
        parts = decouper(texte)
        tot = sum(len(p) for p in parts)
        x = debut
        for p in parts:
            dd = duree * len(p) / tot
            lignes += [str(n), "%s --> %s" % (horodatage(x), horodatage(x + dd)), p, ""]
            x += dd
            n += 1
    open(chemin, "w", encoding="utf-8").write("\n".join(lignes))


def produire(tuto, kokoro_dir):
    import numpy as np
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(kokoro_dir, "kokoro-v1.0.onnx"), os.path.join(kokoro_dir, "voices-v1.0.bin"))
    hz = 24000
    morceaux, actions, beats, cues = [], [], [], []
    t = 0.6
    morceaux.append(np.zeros(int(0.6 * hz), dtype=np.float32))
    for r in tuto.repliques:
        if r["type"] == "voix":
            son, hz = k.create(parle(r["texte"]), voice="ff_siwis", speed=1.0, lang="fr-fr")
            son = son.astype(np.float32)
            duree = len(son) / hz
            morceaux.append(son)
            cues.append((t, duree, r["texte"]))
        else:
            duree = r["duree"]
            morceaux.append(np.zeros(int(duree * hz), dtype=np.float32))
        beats.append({"debut": t, "fin": t + duree, "section": r["section"]})
        for g in r["gestes"]:
            g = dict(g)
            g["debut"] = round(t + g.pop("a") * duree, 3)
            g["duree"] = g.pop("d")
            actions.append(g)
        if r["type"] == "pause":
            actions.append({"type": "pause", "debut": t, "duree": duree, "texte": r["texte"], "titre": r["titre"], "id": None})
        pause_apres = r.get("apres", 0)
        morceaux.append(np.zeros(int(pause_apres * hz), dtype=np.float32))
        t += duree + pause_apres
    total = t + 1.5
    morceaux.append(np.zeros(int(1.5 * hz), dtype=np.float32))
    actions.sort(key=lambda g: g["debut"])

    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "voix.wav")
    sf.write(wav, np.concatenate(morceaux), hz)
    plan = os.path.join(tmp, "plan.json")
    json.dump({"beats": beats, "actions": actions, "total": total, "ips": IPS}, open(plan, "w"))
    muet = os.path.join(tmp, "muet.mp4")
    print("voix : %d min %02d ; capture des images…" % (int(total) // 60, int(total) % 60), flush=True)
    subprocess.run(["node", os.path.join(ICI, "capturer_tuto.js"), plan, muet], check=True)
    dossier = os.path.join(RACINE, "videos")
    os.makedirs(dossier, exist_ok=True)
    sortie = os.path.join(dossier, tuto.nom + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", muet, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "64k",
                    "-ac", "1", "-shortest", "-movflags", "+faststart", sortie], check=True)
    ecrire_vtt(sortie[:-4] + ".vtt", cues)
    print("%s : %d min %02d, %.1f Mo, %d répliques" % (os.path.basename(sortie), int(total) // 60, int(total) % 60,
                                                    os.path.getsize(sortie) / 1e6, len(tuto.repliques)), flush=True)
    return plan


def charger(chemin):
    spec = importlib.util.spec_from_file_location("tuto_script", chemin)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, ICI)
    spec.loader.exec_module(m)
    return m.TUTO


def brouillon(tuto, dossier):
    """Minutage estimé (sans voix) et une image à la fin de chaque réplique : pour contrôler la mise en page."""
    actions, beats, t, fins = [], [], 0.6, []
    for r in tuto.repliques:
        duree = r.get("duree") or max(1.2, len(parle(r["texte"])) / 15.0)
        beats.append({"debut": t, "fin": t + duree, "section": r["section"]})
        for g in r["gestes"]:
            g = dict(g); g["debut"] = round(t + g.pop("a") * duree, 3); g["duree"] = g.pop("d"); actions.append(g)
        if r["type"] == "pause":
            actions.append({"type": "pause", "debut": t, "duree": duree, "texte": r["texte"], "titre": r["titre"], "id": None})
        t += duree + r.get("apres", 0)
        fins.append(t - 0.05)
    actions.sort(key=lambda g: g["debut"])
    plan = os.path.join(tempfile.mkdtemp(), "plan.json")
    json.dump({"beats": beats, "actions": actions, "total": t + 1, "ips": IPS}, open(plan, "w"))
    subprocess.run(["node", os.path.join(ICI, "capturer_tuto.js"), plan, dossier, "--images",
                    ",".join("%.2f" % f for f in fins)], check=True)
    print("brouillon : %d images dans %s, durée estimée %d min %02d" % (len(fins), dossier, int(t) // 60, int(t) % 60))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--brouillon":
        brouillon(charger(sys.argv[1]), sys.argv[3])
    else:
        produire(charger(sys.argv[1]), os.environ.get("KOKORO_DIR", os.path.join(ICI, "modeles")))
