# -*- coding: utf-8 -*-
"""Génère une vidéo « tableau manuscrit » et ses sous-titres à partir d'un script JSON.

    KOKORO_DIR=/chemin/vers/modeles python3 outils/video/generer.py outils/video/scripts/m3-insertion.json

Étapes : voix off de chaque scène (Kokoro, voix française) -> durées -> capture image par image
de page.html (Playwright) -> assemblage ffmpeg en 1280x720 -> sous-titres WebVTT calés sur la voix.
Sorties : videos/<fichier>.mp4 et videos/<fichier>.vtt.

Prérequis : pip install kokoro-onnx soundfile ; Playwright (Node) ; ffmpeg ;
les fichiers kokoro-v1.0.onnx et voices-v1.0.bin (variable KOKORO_DIR).
Repris de l'outil vidéo du site « Fondements MCS », avec la génération des sous-titres en plus.
"""
import json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
KOKORO = os.environ.get("KOKORO_DIR", os.path.join(ICI, "modeles"))
IPS, PAUSE = 20, 0.7


def horodatage(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return "%02d:%02d:%06.3f" % (h, m, s)


def morceaux(texte, maxi=84):
    """Découpe une réplique en sous-titres d'au plus deux lignes courtes."""
    phrases, cour = [], ""
    for mot in texte.split():
        if len(cour) + len(mot) + 1 > maxi and cour:
            phrases.append(cour)
            cour = mot
        else:
            cour = (cour + " " + mot).strip()
    if cour:
        phrases.append(cour)
    return phrases


def vtt(scenes):
    out = ["WEBVTT", ""]
    k = 1
    for sc in scenes:
        parts = morceaux(sc["texte"])
        total = sum(len(p) for p in parts)
        t = sc["debut"]
        for p in parts:
            d = sc["voix"] * len(p) / total
            out += [str(k), "%s --> %s" % (horodatage(t), horodatage(t + d)), p, ""]
            t += d
            k += 1
    return "\n".join(out)


def main(chemin):
    script = json.load(open(chemin, encoding="utf-8"))
    k = Kokoro(os.path.join(KOKORO, "kokoro-v1.0.onnx"), os.path.join(KOKORO, "voices-v1.0.bin"))
    piste, t, scenes = [], 0.0, []
    for sc in script["scenes"]:
        son, hz = k.create(sc["voix"], voice="ff_siwis", speed=0.95, lang="fr-fr")
        duree = len(son) / hz
        piste += [son, np.zeros(int(PAUSE * hz), dtype=son.dtype)]
        scenes.append({"debut": t, "voix": duree, "fin": t + duree + PAUSE, "texte": sc.get("sous_titre", sc["voix"]),
                       "lignes": sc["lignes"], "legende": sc["legende"], "efface": sc.get("efface", False)})
        t += duree + PAUSE
    total = t + 1.0
    piste.append(np.zeros(int(1.0 * hz), dtype=piste[0].dtype))
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "voix.wav")
    sf.write(wav, np.concatenate(piste), hz)
    plan = os.path.join(tmp, "plan.json")
    json.dump({"scenes": scenes, "total": total, "ips": IPS}, open(plan, "w"))
    muet = os.path.join(tmp, "muet.mp4")
    subprocess.run(["node", os.path.join(ICI, "capturer.js"), plan, muet], check=True)
    dossier = os.path.join(RACINE, "videos")
    os.makedirs(dossier, exist_ok=True)
    sortie = os.path.join(dossier, script["fichier"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", muet, "-i", wav, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-shortest", "-movflags", "+faststart", sortie],
                   check=True)
    with open(sortie.rsplit(".", 1)[0] + ".vtt", "w", encoding="utf-8") as f:
        f.write(vtt(scenes))
    m, s = divmod(int(round(total)), 60)
    print("%s : %d min %02d, %.1f Mo, sous-titres écrits" % (script["fichier"], m, s, os.path.getsize(sortie) / 1e6))


if __name__ == "__main__":
    main(sys.argv[1])
