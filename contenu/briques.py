# -*- coding: utf-8 -*-
"""Briques d'écriture des étapes : encadrés, démonstrations, code, exercices, outils interactifs.

Importées par build.py (pour la mise en page) et par les fichiers de contenu
moduleN.py (pour écrire le cours). Module séparé afin d'éviter un import
circulaire entre build.py et le contenu.
"""

import html
import json
import os

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def retenir(label, corps):
    return '<div class="retenir"><p class="lab">%s</p>%s</div>' % (label, corps)


def demo(corps, label="Démonstration"):
    return '<div class="demo"><p class="lab">%s</p>%s<p class="cqfd">∎</p></div>' % (label, corps)


def prof(corps, label="Le conseil"):
    return '<div class="prof"><p class="lab">%s</p>%s</div>' % (label, corps)


def master(corps, label="En cryptographie"):
    return '<div class="master"><p class="lab">%s</p>%s</div>' % (label, corps)


def code(src, lang="python", sortie=None, titre="Implémentation"):
    cls = "sage" if lang.lower().startswith("sage") else ""
    out = ""
    if sortie:
        out = '<pre class="sortie">%s</pre>' % html.escape(sortie.strip("\n"))
    return ('<div class="code tex2jax_ignore"><div class="code-h">'
            '<p class="lab">%s</p><span class="code-lang %s">%s</span>'
            '<button type="button" class="copier">copier</button></div>'
            '<pre>%s</pre>%s</div>'
            % (titre, cls, lang, html.escape(src.strip("\n")), out))


def exo(n, enonce, correction, remarque=None, niveau=None):
    niv = '<span class="niv">%s</span>' % niveau if niveau else ""
    rem = prof(remarque, "Remarque") if remarque else ""
    return ('<article class="exo"><p class="exo-n">Exercice %s%s</p>'
            '<div class="exo-q">%s</div>'
            '<details class="tex2jax_ignore"><summary>Voir la correction</summary>'
            '<div class="copie"><p class="lab">Correction</p>%s</div>%s</details></article>'
            % (n, niv, enonce, correction, rem))


def video(fichier, legende, duree):
    """Lecteur vidéo ; les sous-titres français videos/<nom>.vtt sont joints s'ils existent."""
    base = fichier.rsplit(".", 1)[0]
    piste = ""
    if os.path.exists(os.path.join(_RACINE, "docs", "videos", base + ".vtt")):
        piste = '<track kind="subtitles" srclang="fr" label="Français" src="videos/%s.vtt" default>' % base
    return ('<figure class="video"><video controls preload="metadata" playsinline src="videos/%s">%s'
            '</video><figcaption><span class="tag">Vidéo</span> %s '
            '<span class="dur">%s</span></figcaption></figure>' % (fichier, piste, legende, duree))


def video_attente(sujet):
    return ('<figure class="video attente"><div class="ph"><p>Vidéo à venir : %s</p></div>'
            '<figcaption><span class="tag soon">Vidéo</span> en préparation</figcaption></figure>'
            % sujet)




# ─────────────────────────────────────────────────────────────────────────────
# Gabarit en quatre temps (nœud pilote et suivants)
# ─────────────────────────────────────────────────────────────────────────────

import json
import os
import subprocess
import sys

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CODE = os.path.join(_RACINE, "code")


def qcm(role, questions):
    """Test à choix, corrigé dans le navigateur.

    role       "entree" (permet de sauter l'étape) ou "sortie" (valide l'étape)
    questions  liste de (énoncé, [options], indice de la bonne option, explication)
    """
    titre = {"entree": "Test d'entrée — as-tu besoin de cette étape ?",
             "sortie": "Test de sortie — valide l'étape"}[role]
    seuil = len(questions) if role == "entree" else max(1, len(questions) - 1)
    blocs = []
    for i, (enonce, options, bonne, explication) in enumerate(questions):
        choix = "".join(
            '<label class="qcm-o"><input type="radio" name="q%d" value="%d"> <span>%s</span></label>'
            % (i, k, o) for k, o in enumerate(options))
        blocs.append('<fieldset class="qcm-q" data-bonne="%d"><legend>%d. %s</legend>%s'
                     '<p class="qcm-x" hidden>%s</p></fieldset>' % (bonne, i + 1, enonce, choix, explication))
    return ('<form class="qcm" data-role="%s" data-seuil="%d"><p class="lab">%s</p>%s'
            '<div class="qcm-bas"><button type="submit" class="btn">Corriger</button>'
            '<p class="qcm-res" role="status" hidden></p></div></form>'
            % (role, seuil, titre, "".join(blocs)))


def preuve(enonce_label, enonce, idee, etapes, complete):
    """Un théorème à démontrer soi-même : l'idée, le squelette, puis la preuve repliée."""
    plan = "".join("<li>%s</li>" % e for e in etapes)
    return ('<div class="preuve">%s'
            '<div class="idee"><p class="lab">L\'idée en une phrase</p><p>%s</p></div>'
            '<div class="squelette"><p class="lab">Le squelette — complète chaque étape sur ta feuille</p>'
            '<ol>%s</ol></div>'
            '<details class="tex2jax_ignore"><summary>Voir la démonstration complète</summary>%s</details>'
            '</div>' % (retenir(enonce_label, enonce), idee, plan, demo(complete)))


def exercice(n, niveau, enonce, indice, correction, remarque=None):
    """Exercice gradué : énoncé, indice replié, correction manuscrite repliée."""
    rem = prof(remarque, "Remarque") if remarque else ""
    return ('<article class="exo"><p class="exo-n">Exercice %s<span class="niv">%s</span></p>'
            '<div class="exo-q">%s</div>'
            '<details class="indice tex2jax_ignore"><summary>Un indice</summary><div class="prof">%s</div></details>'
            '<details class="tex2jax_ignore"><summary>Voir la correction</summary>'
            '<div class="copie"><p class="lab">Correction</p>%s</div>%s</details></article>'
            % (n, niveau, enonce, indice, correction, rem))


def a_toi(enonce, solution):
    return ('<div class="atoi"><p class="lab">À toi</p>%s'
            '<details class="tex2jax_ignore"><summary>Voir une solution</summary>%s</details></div>'
            % (enonce, solution))


def a_retenir(lignes):
    return retenir("À retenir", "<ul>%s</ul>" % "".join("<li>%s</li>" % l for l in lignes))


def etape(entree, comprendre, demontrer, implementer, exercer, sortie, retenir_):
    """Assemble une étape au gabarit : test d'entrée, quatre temps en onglets, test de sortie."""
    temps = [("Comprendre", comprendre), ("Démontrer", demontrer),
             ("Implémenter", implementer), ("S'exercer", exercer + sortie + retenir_)]
    onglets = "".join(
        '<button type="button" role="tab" class="onglet" aria-selected="%s" data-t="%d">'
        '<span class="o-n">%d</span>%s</button>' % ("true" if i == 0 else "false", i, i + 1, nom)
        for i, (nom, _) in enumerate(temps))
    panneaux = "".join(
        '<div class="panneau" role="tabpanel" data-t="%d"%s>%s'
        '<p class="suite">%s</p></div>'
        % (i, "" if i == 0 else " hidden", contenu,
           '<button type="button" class="btn ghost aller" data-t="%d">Temps suivant : %s →</button>'
           % (i + 1, temps[i + 1][0]) if i + 1 < len(temps) else "")
        for i, (_, contenu) in enumerate(temps))
    return ('%s<div class="temps"><div class="onglets" role="tablist">%s</div>%s</div>'
            % (entree, onglets, panneaux))


def atelier(ident, consigne, depart, tests, corrige):
    """Atelier de code : l'étudiant complète `depart`, puis lance des tests cachés dans son navigateur.

    tests  liste de dictionnaires :
             {"appel": "f(2, 3)", "verif": "r == 5", "attendu": "5"}          vérifie le résultat r
             {"appel": "f(0)", "leve": "ValueError", "attendu": "une ValueError"}  attend une exception
           `verif` est une expression Python ; elle doit tester la propriété, pas une valeur
           arbitraire (plusieurs réponses peuvent être justes).
    """
    return ('<div class="atelier" data-id="%s"><p class="lab">Atelier — à toi de coder</p>%s'
            '<textarea class="at-code" spellcheck="false" autocapitalize="off" autocomplete="off" '
            'autocorrect="off" rows="%d" aria-label="Ton code Python">%s</textarea>'
            '<script type="application/json" class="atelier-tests">%s</script>'
            '<div class="atelier-b"><button type="button" class="btn ghost at-executer">Exécuter</button>'
            '<button type="button" class="btn at-tester">Tester mon code</button>'
            '<button type="button" class="at-reinit">Réinitialiser</button>'
            '<span class="atelier-etat" role="status"></span></div>'
            '<div class="atelier-res" hidden></div>'
            '<details class="atelier-corrige tex2jax_ignore" hidden><summary>Voir le corrigé (après avoir essayé)</summary>%s</details>'
            '</div>'
            % (ident, consigne, depart.strip("\n").count("\n") + 3, html.escape(depart.strip("\n")),
               json.dumps(tests, ensure_ascii=False).replace("</", "<\\/"), corrige))


def sage_atelier(consigne, depart):
    """Cellule SageMath modifiable (service SageMathCell), pour confronter son résultat à la référence."""
    return ('<div class="sage-atelier"><p class="lab">Vérifie avec SageMath</p>%s'
            '<div class="sage-cellule tex2jax_ignore" hidden><script type="text/x-sage">%s</script></div>'
            '<div class="atelier-b"><button type="button" class="btn ghost sage-ouvrir">Ouvrir la cellule SageMath</button>'
            '<span class="sage-msg" role="status"></span></div></div>'
            % (consigne, html.escape(depart.strip("\n"))))


# ─────────────────────────────────────────────────────────────────────────────
# Briques propres au parcours Complexité
# ─────────────────────────────────────────────────────────────────────────────

def examen(corps, label="À l'examen"):
    """Ce qui tombe à l'examen, et comment le rédiger."""
    return '<div class="examen"><p class="lab">%s</p>%s</div>' % (label, corps)


def methode(titre, etapes_):
    """Une méthode numérotée, à appliquer telle quelle."""
    return ('<div class="methode"><p class="lab">Méthode — %s</p><ol>%s</ol></div>'
            % (titre, "".join("<li>%s</li>" % e for e in etapes_)))


def animateur(ident, algo, entrees, legende):
    """Animateur pas à pas : l'algorithme tourne ligne par ligne, avec les compteurs de coût.

    algo     identifiant d'un algorithme connu de assets/animateur.js (ex. "insertion")
    entrees  liste de (nom, tableau) proposés à l'étudiant ; il peut aussi taper le sien
    """
    return ('<div class="anim" data-id="%s" data-algo="%s" data-entrees="%s">'
            '<p class="lab">Animateur — %s</p><noscript>L&#39;animateur a besoin de JavaScript.</noscript></div>'
            % (ident, algo, html.escape(json.dumps(entrees, ensure_ascii=False)), legende))


def mesure(ident, consigne, fonction, tailles, courbes):
    """Mesure expérimentale : le code de l'atelier `ident` est lancé sur des entrées de tailles croissantes ;
    le nombre d'opérations compté est tracé, avec les courbes théoriques à comparer.

    fonction  nom de la fonction de l'étudiant, qui renvoie (resultat, compteur)
    tailles   liste de n
    courbes   liste de (nom, expression JavaScript en n) tracées en pointillés
    """
    return ('<div class="mesure" data-atelier="%s" data-fonction="%s" data-tailles="%s" data-courbes="%s">'
            '<p class="lab">Mesure — ce que ton code fait vraiment</p>%s'
            '<div class="atelier-b"><button type="button" class="btn m-lancer">Mesurer et tracer</button>'
            '<span class="m-etat" role="status"></span></div>'
            '<div class="m-graphe" hidden></div></div>'
            % (ident, fonction, json.dumps(tailles), html.escape(json.dumps(courbes, ensure_ascii=False)), consigne))


def tableau(entetes, lignes, classe=""):
    t = "".join("<th>%s</th>" % h for h in entetes)
    corps = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in l) for l in lignes)
    return ('<div class="table-wrap"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (classe, t, corps))
