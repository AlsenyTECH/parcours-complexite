/* Exécute le code de l'étudiant dans un fil séparé : une boucle infinie ne bloque pas la page,
   et le fil peut être arrêté de l'extérieur. Python tourne dans le navigateur (Pyodide). */
importScripts('pyodide/pyodide.js');

var HARNAIS = [
'import json, io, contextlib, traceback',
'def __erreur(e):',
'    tb = traceback.extract_tb(e.__traceback__)',
'    lignes = [f.lineno for f in tb if f.filename == "<etudiant>"]',
'    if isinstance(e, SyntaxError) and e.filename == "<etudiant>":',
'        lignes = [e.lineno]',
'    ou = (" (ligne %d)" % lignes[-1]) if lignes else ""',
'    texte = e.msg if isinstance(e, SyntaxError) else str(e)',
'    return "%s%s : %s" % (type(e).__name__, ou, texte)',
'def __lancer(code, tests):',
'    ns, sortie = {"__name__": "__main__"}, io.StringIO()',
'    try:',
'        with contextlib.redirect_stdout(sortie):',
'            exec(compile(code, "<etudiant>", "exec"), ns)',
'    except BaseException as e:',
'        return {"erreur": __erreur(e), "sortie": sortie.getvalue()[:3000]}',
'    res = []',
'    for t in tests:',
'        ligne = {"appel": t["appel"], "attendu": t["attendu"]}',
'        try:',
'            with contextlib.redirect_stdout(io.StringIO()):',
'                r = eval(t["appel"], ns)',
'            if t.get("leve"):',
'                ligne.update(ok=False, obtenu=repr(r)[:160] + " (aucune erreur levée)")',
'            else:',
'                env = dict(ns); env["r"] = r',
'                ligne.update(ok=bool(eval(t["verif"], env)), obtenu=repr(r)[:160])',
'        except BaseException as e:',
'            if t.get("leve") and type(e).__name__ == t["leve"]:',
'                ligne.update(ok=True, obtenu=t["leve"] + " levée")',
'            else:',
'                ligne.update(ok=False, obtenu="erreur — " + __erreur(e))',
'        res.append(ligne)',
'    return {"tests": res, "sortie": sortie.getvalue()[:3000]}',
'json.dumps(__lancer(__code, json.loads(__tests)), ensure_ascii=False)'
].join('\n');

var pret = loadPyodide({ indexURL: new URL('pyodide/', self.location.href).href })
  .then(function (py) { self.postMessage({ type: 'pret' }); return py; })
  .catch(function (e) { self.postMessage({ type: 'panne', message: String(e) }); throw e; });

self.onmessage = function (ev) {
  pret.then(function (py) {
    py.globals.set('__code', ev.data.code);
    py.globals.set('__tests', JSON.stringify(ev.data.tests));
    var json;
    try { json = py.runPython(HARNAIS); }
    catch (e) { json = JSON.stringify({ erreur: String(e) }); }
    self.postMessage({ type: 'resultat', json: json });
  });
};
