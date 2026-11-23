/* Mesure expérimentale : lance la fonction de l'étudiant (écrite dans un atelier) sur des entrées
   de tailles croissantes, pour plusieurs « cas » (meilleur, moyen, pire…), puis trace le compteur
   renvoyé à côté des courbes théoriques. Chaque cas est une expression Python qui fabrique
   les arguments à partir de n ; un cas aléatoire est répété et moyenné. */
(function () {
  var blocs = document.querySelectorAll('.mesure');
  if (!blocs.length) return;

  function harnais(f, tailles, cas) {
    var defs = cas.map(function (c, k) {
      return 'def __cas' + k + '(n):\n    return ' + c.expr;
    }).join('\n');
    var essais = JSON.stringify(cas.map(function (c) { return c.essais || 1; }));
    return [
      '',
      'import json as __json, random as __random, random',
      '__random.seed(2025)',
      defs,
      'def __compte(fn, args):',
      '    r = fn(*args)',
      '    if not (isinstance(r, tuple) and len(r) == 2):',
      '        raise TypeError(fn.__name__ + " doit renvoyer un couple (résultat, compteur)")',
      '    return r[1]',
      '__cas = [' + cas.map(function (c, k) { return '__cas' + k; }).join(', ') + ']',
      '__fns = [' + cas.map(function (c) { return c.fonction || f; }).join(', ') + ']',
      '__essais = ' + essais,
      '__res = []',
      'for __n in ' + JSON.stringify(tailles) + ':',
      '    __ligne = [__n]',
      '    for __c, __e, __f in zip(__cas, __essais, __fns):',
      '        __ligne.append(sum(__compte(__f, __c(__n)) for _ in range(__e)) / __e)',
      '    __res.append(__ligne)',
      'print("__MESURE__" + __json.dumps(__res))'
    ].join('\n');
  }

  var COUL = { meilleur: 'var(--prof)', moyen: 'var(--pen)', pire: 'var(--rouge)', autre: 'var(--or)' };

  function nombre(x) {
    if (x >= 1e9) return (x / 1e9).toFixed(2).replace('.', ',') + ' G';
    if (x >= 1e6) return (x / 1e6).toFixed(2).replace('.', ',') + ' M';
    return String(Math.round(x * 10) / 10).replace('.', ',');
  }

  function graphe(donnees, courbes, cas, ratios, axe) {
    var W = 640, H = 340, g = 60, d = 16, h = 16, b = 44;
    var nmin = donnees[0][0], nmax = donnees[donnees.length - 1][0];
    var x0 = nmin > nmax / 4 ? nmin : 0;
    var ymax = 0;
    donnees.forEach(function (l) { for (var k = 1; k < l.length; k++) ymax = Math.max(ymax, l[k]); });
    var fns = courbes.map(function (c) { return { nom: c[0], f: new Function('n', 'return ' + c[1]) }; });
    fns.forEach(function (c) { ymax = Math.max(ymax, c.f(nmax)); });
    ymax = (ymax || 1) * 1.05;
    function X(n) { return g + (W - g - d) * (n - x0) / (nmax - x0); }
    function Y(v) { return H - b - (H - b - h) * v / ymax; }
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="m-svg" role="img" aria-label="Compteur mesuré en fonction de la taille">';
    for (var k = 0; k <= 4; k++) {
      var v = ymax * k / 4, y = Y(v);
      s += '<line x1="' + g + '" x2="' + (W - d) + '" y1="' + y + '" y2="' + y + '" class="m-grille"/>' +
           '<text x="' + (g - 6) + '" y="' + (y + 4) + '" text-anchor="end" class="m-t">' + nombre(v >= 100 ? Math.round(v) : v) + '</text>';
    }
    var dernier = 1e9;
    for (var q = donnees.length - 1; q >= 0; q--) {   // de droite à gauche : la dernière valeur est toujours écrite
      var x = X(donnees[q][0]), lab = String(donnees[q][0]), larg = 7 * lab.length + 10;
      if (dernier - x < larg) continue;
      var ancre = q === donnees.length - 1 ? 'end' : 'middle';
      s += '<text x="' + (ancre === 'end' ? x + 4 : x) + '" y="' + (H - b + 18) + '" text-anchor="' + ancre + '" class="m-t">' + lab + '</text>';
      dernier = x - (ancre === 'end' ? larg : larg / 2);
    }
    s += '<text x="' + ((g + W - d) / 2) + '" y="' + (H - 6) + '" text-anchor="middle" class="m-t">' + axe + '</text>';
    fns.forEach(function (c) {
      var p = '';
      for (var i = 0; i <= 80; i++) { var n = x0 + (nmax - x0) * i / 80; p += (i ? 'L' : 'M') + X(n).toFixed(1) + ',' + Y(c.f(n)).toFixed(1); }
      s += '<path d="' + p + '" class="m-theo"/>';
      s += '<text x="' + (W - d - 4) + '" y="' + (Y(c.f(nmax)) - 6) + '" text-anchor="end" class="m-t m-nom">' + c.nom + '</text>';
    });
    cas.forEach(function (c, k) {
      var col = COUL[c.couleur] || COUL.autre, p = '';
      donnees.forEach(function (l, i) { p += (i ? 'L' : 'M') + X(l[0]).toFixed(1) + ',' + Y(l[k + 1]).toFixed(1); });
      s += '<path d="' + p + '" fill="none" stroke="' + col + '" stroke-width="2.2"/>';
      donnees.forEach(function (l) {
        s += '<circle cx="' + X(l[0]).toFixed(1) + '" cy="' + Y(l[k + 1]).toFixed(1) + '" r="3.6" fill="' + col + '"><title>' + l[0] + ' : ' + nombre(l[k + 1]) + '</title></circle>';
      });
    });
    s += '</svg>';
    var leg = '<p class="m-leg">' + cas.map(function (c) {
      return '<span style="--c:' + (COUL[c.couleur] || COUL.autre) + '">' + c.nom + '</span>';
    }).join('') + '<span class="theo">en pointillés : les formules du cours</span></p>';
    var fr = ratios.map(function (r) { return { nom: r[0], k: r[1] + 1, f: new Function('n', 'return ' + r[2]) }; });
    var tab = '<div class="table-wrap"><table class="m-tab"><thead><tr><th>' + axe.split(' ')[0] + '</th>' +
              cas.map(function (c) { return '<th>' + c.court + '</th>'; }).join('') +
              fr.map(function (r) { return '<th>' + r.nom + '</th>'; }).join('') + '</tr></thead><tbody>' +
              donnees.map(function (l) {
                return '<tr><td>' + l[0] + '</td>' + l.slice(1).map(function (v) { return '<td>' + nombre(v) + '</td>'; }).join('') +
                  fr.map(function (r) { return '<td>' + (l[r.k] / r.f(l[0])).toFixed(3).replace('.', ',') + '</td>'; }).join('') + '</tr>';
              }).join('') + '</tbody></table></div>';
    return s + leg + tab;
  }

  blocs.forEach(function (bloc) {
    var bouton = bloc.querySelector('.m-lancer'), etat = bloc.querySelector('.m-etat'), zone = bloc.querySelector('.m-graphe');
    var tailles = JSON.parse(bloc.dataset.tailles), courbes = JSON.parse(bloc.dataset.courbes);
    var cas = JSON.parse(bloc.dataset.cas), ratios = JSON.parse(bloc.dataset.ratios || '[]');
    var f = bloc.dataset.fonction, axe = bloc.dataset.axe || 'taille n';
    bouton.addEventListener('click', function () {
      var at = document.querySelector('.atelier[data-id="' + bloc.dataset.atelier + '"] textarea');
      if (!at || !window.CXatelier) { etat.textContent = 'Atelier introuvable.'; return; }
      bouton.disabled = true;
      var code = at.value + '\n' + harnais(f, tailles, cas);
      window.CXatelier.executer(code, [], function (t) { etat.textContent = t; }, function (r) {
        bouton.disabled = false; etat.textContent = '';
        var sortie = r.sortie || '', i = sortie.lastIndexOf('__MESURE__');
        if (r.erreur || i < 0) {
          zone.hidden = false;
          zone.innerHTML = '<p class="at-ko">' + (r.erreur ? 'Ton code produit une erreur : ' + String(r.erreur).replace(/&/g, '&amp;').replace(/</g, '&lt;')
            : 'La mesure n\'a rien renvoyé.') + ' Fais d\'abord passer les tests de l\'atelier.</p>';
          return;
        }
        var donnees = JSON.parse(sortie.slice(i + 10).split('\n')[0]);
        zone.innerHTML = graphe(donnees, courbes, cas, ratios, axe);
        zone.hidden = false;
      });
    });
  });
})();
