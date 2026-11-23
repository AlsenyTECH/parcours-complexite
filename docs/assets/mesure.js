/* Mesure expérimentale : lance la fonction de l'étudiant (écrite dans l'atelier) sur des entrées
   de tailles croissantes, au meilleur cas (tableau trié), en moyenne (tableaux au hasard) et au pire cas
   (tableau trié à l'envers), puis trace le compteur renvoyé à côté des courbes théoriques. */
(function () {
  var blocs = document.querySelectorAll('.mesure');
  if (!blocs.length) return;

  var HARNAIS = [
    '',
    'import json as __json, random as __random',
    '__random.seed(2025)',
    'def __compte(T):',
    '    r = %F%(list(T))',
    '    if not (isinstance(r, tuple) and len(r) == 2):',
    '        raise TypeError("%F% doit renvoyer un couple (tableau trié, nombre de tests)")',
    '    return r[1]',
    '__res = []',
    'for __n in %T%:',
    '    __moy = sum(__compte(__random.sample(range(10 * __n), __n)) for _ in range(8)) / 8',
    '    __res.append([__n, __compte(range(__n)), __moy, __compte(range(__n, 0, -1))])',
    'print("__MESURE__" + __json.dumps(__res))'
  ].join('\n');

  var COUL = { meilleur: 'var(--prof)', moyen: 'var(--pen)', pire: 'var(--rouge)' };

  function nombre(x) {
    return x >= 1e6 ? (x / 1e6).toFixed(2).replace('.', ',') + ' M' : String(Math.round(x * 10) / 10).replace('.', ',');
  }

  function graphe(donnees, courbes) {
    var W = 640, H = 340, g = 56, d = 16, h = 16, b = 44;
    var nmax = donnees[donnees.length - 1][0];
    var ymax = 0;
    donnees.forEach(function (l) { ymax = Math.max(ymax, l[3]); });
    var fns = courbes.map(function (c) { return { nom: c[0], f: new Function('n', 'return ' + c[1]) }; });
    fns.forEach(function (c) { ymax = Math.max(ymax, c.f(nmax)); });
    ymax *= 1.05;
    function X(n) { return g + (W - g - d) * n / nmax; }
    function Y(v) { return H - b - (H - b - h) * v / ymax; }
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="m-svg" role="img" aria-label="Nombre de tests mesuré en fonction de n">';
    for (var k = 0; k <= 4; k++) {
      var v = ymax * k / 4, y = Y(v);
      s += '<line x1="' + g + '" x2="' + (W - d) + '" y1="' + y + '" y2="' + y + '" class="m-grille"/>' +
           '<text x="' + (g - 6) + '" y="' + (y + 4) + '" text-anchor="end" class="m-t">' + nombre(v) + '</text>';
    }
    donnees.forEach(function (l) {
      s += '<text x="' + X(l[0]) + '" y="' + (H - b + 18) + '" text-anchor="middle" class="m-t">' + l[0] + '</text>';
    });
    s += '<text x="' + ((g + W - d) / 2) + '" y="' + (H - 6) + '" text-anchor="middle" class="m-t">taille n du tableau</text>';
    fns.forEach(function (c) {
      var p = '';
      for (var i = 0; i <= 60; i++) { var n = nmax * i / 60; p += (i ? 'L' : 'M') + X(n).toFixed(1) + ',' + Y(c.f(n)).toFixed(1); }
      s += '<path d="' + p + '" class="m-theo"/>';
      s += '<text x="' + (W - d - 4) + '" y="' + (Y(c.f(nmax)) - 6) + '" text-anchor="end" class="m-t m-nom">' + c.nom + '</text>';
    });
    [['meilleur', 1], ['moyen', 2], ['pire', 3]].forEach(function (serie) {
      var p = '';
      donnees.forEach(function (l, i) { p += (i ? 'L' : 'M') + X(l[0]).toFixed(1) + ',' + Y(l[serie[1]]).toFixed(1); });
      s += '<path d="' + p + '" fill="none" stroke="' + COUL[serie[0]] + '" stroke-width="2.2"/>';
      donnees.forEach(function (l) {
        s += '<circle cx="' + X(l[0]).toFixed(1) + '" cy="' + Y(l[serie[1]]).toFixed(1) + '" r="3.6" fill="' + COUL[serie[0]] + '"><title>n = ' + l[0] + ' : ' + nombre(l[serie[1]]) + '</title></circle>';
      });
    });
    s += '</svg>';
    var leg = '<p class="m-leg"><span style="--c:' + COUL.pire + '">pire cas (trié à l\'envers)</span>' +
              '<span style="--c:' + COUL.moyen + '">moyenne sur 8 tableaux au hasard</span>' +
              '<span style="--c:' + COUL.meilleur + '">meilleur cas (déjà trié)</span>' +
              '<span class="theo">en pointillés : les formules du cours</span></p>';
    var tab = '<div class="table-wrap"><table class="m-tab"><thead><tr><th>n</th><th>meilleur</th><th>moyen</th><th>pire</th>' +
              '<th>pire / n²</th><th>moyen / n²</th></tr></thead><tbody>' +
              donnees.map(function (l) {
                return '<tr><td>' + l[0] + '</td><td>' + nombre(l[1]) + '</td><td>' + nombre(l[2]) + '</td><td>' + nombre(l[3]) + '</td>' +
                       '<td>' + (l[3] / (l[0] * l[0])).toFixed(3).replace('.', ',') + '</td><td>' + (l[2] / (l[0] * l[0])).toFixed(3).replace('.', ',') + '</td></tr>';
              }).join('') + '</tbody></table></div>';
    return s + leg + tab;
  }

  blocs.forEach(function (bloc) {
    var bouton = bloc.querySelector('.m-lancer'), etat = bloc.querySelector('.m-etat'), zone = bloc.querySelector('.m-graphe');
    var tailles = JSON.parse(bloc.dataset.tailles), courbes = JSON.parse(bloc.dataset.courbes), f = bloc.dataset.fonction;
    bouton.addEventListener('click', function () {
      var at = document.querySelector('.atelier[data-id="' + bloc.dataset.atelier + '"] textarea');
      if (!at || !window.CXatelier) { etat.textContent = 'Atelier introuvable.'; return; }
      bouton.disabled = true;
      var code = at.value + '\n' + HARNAIS.replace(/%F%/g, f).replace('%T%', JSON.stringify(tailles));
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
        zone.innerHTML = graphe(donnees, courbes);
        zone.hidden = false;
      });
    });
  });
})();
