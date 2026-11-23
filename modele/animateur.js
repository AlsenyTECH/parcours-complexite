/* Animateur pas à pas : l'algorithme tourne instruction par instruction, avec le nombre
   d'exécutions de chaque ligne, comme dans un tableau d'analyse de coût.
   La trace complète est calculée d'avance : on peut avancer, reculer, rejouer.

   Chaque algorithme fournit :
     lignes        le pseudo-code (numérotation 1, 2, …)
     commentaires  numéros des lignes qui ne coûtent rien
     param         null, ou le nom d'un paramètre en plus du tableau (ex. "x")
     trace(T, p)   la liste des états ; un état = { ligne, T, cpt, msg, marques, classes, vars, extra, fini }
     bilan(e, n)   le texte affiché à la fin */
(function () {
  var blocs = document.querySelectorAll('.anim');
  if (!blocs.length) return;

  function ech(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function sub(k) { return String(k).split('').map(function (c) { return '₀₁₂₃₄₅₆₇₈₉'[+c]; }).join(''); }
  function somme(cpt) { return cpt.reduce(function (a, b) { return a + b; }, 0); }

  function enregistreur(T, nlignes) {
    var etats = [], cpt = [];
    for (var k = 0; k <= nlignes; k++) cpt.push(0);
    return {
      cpt: cpt,
      note: function (ligne, msg, o) {
        o = o || {};
        etats.push({ ligne: ligne, T: T.slice(1), cpt: cpt.slice(), msg: msg, marques: o.marques || {}, classes: o.classes || {},
                     vars: o.vars || [], extra: o.extra || '', fini: !!o.fini, info: o.info || {} });
      },
      etats: etats
    };
  }

  // ─────────────────────────────────────────────────────────────────────────
  var ALGOS = {};

  ALGOS.insertion = {
    lignes: ['Pour j = 2 à n', '  clé = T[j]', '  ▹ insérer T[j] dans T[1..j−1] trié', '  i = j − 1',
             '  tant que i > 0 et T[i] > clé', '    T[i+1] = T[i]', '    i = i − 1', '  T[i+1] = clé'],
    commentaires: [3], param: null,
    trace: function (T0) {
      var T = [null].concat(T0), n = T0.length, R = enregistreur(T, 8), cpt = R.cpt, tj = {};
      var j = 2, i = null, cle = null, t = 0;
      function o(extra) {
        var marques = {}, classes = {};
        for (var p = 1; p <= n; p++) {
          if ((extra && extra.fini) || p < j || (extra && extra.place && p <= j)) classes[p] = 'trie';
        }
        if (extra && extra.decale) classes[extra.decale] = 'bouge';
        if (extra && extra.place) classes[extra.place] = 'pose';
        if (!(extra && extra.fini) && j <= n) marques[j] = ['j'];
        if (i !== null && i >= 1) (marques[i] = marques[i] || []).push('i');
        var cles = Object.keys(tj);
        return {
          marques: marques, classes: classes, fini: extra && extra.fini,
          vars: [['n', n], ['j', (extra && extra.fini) ? '—' : j], ['i', i === null ? '—' : i], ['clé', cle === null ? '—' : cle, 'rouge']],
          extra: cles.length
            ? '<table><tr><th>j</th>' + cles.map(function (x) { return '<td>' + x + '</td>'; }).join('') + '</tr>' +
              '<tr><th>t<sub>j</sub></th>' + cles.map(function (x) { return '<td>' + tj[x] + '</td>'; }).join('') + '</tr></table>'
            : '<p class="an-vide">Les t<sub>j</sub> (nombre de tests de la ligne 5 pour chaque j) s\'afficheront ici.</p>',
          info: { tj: JSON.parse(JSON.stringify(tj)) }
        };
      }
      R.note(0, 'Départ : n = ' + n + '. Clique sur « Pas suivant » pour exécuter la première instruction.', o());
      for (;;) {
        cpt[1]++;
        if (j > n) { R.note(1, 'Test de la boucle Pour : j = ' + j + ' > n = ' + n + ', la boucle s\'arrête. Ce dernier test compte aussi : la ligne 1 s\'exécute n fois.', o({ fini: true })); break; }
        R.note(1, 'Test de la boucle Pour : j = ' + j + ' ≤ n = ' + n + ', on entre dans la boucle.', o());
        cle = T[j]; cpt[2]++;
        R.note(2, 'clé = T[' + j + '] = ' + cle + '. C\'est la carte qu\'on va ranger.', o());
        i = j - 1; cpt[4]++; t = 0;
        R.note(4, 'i = j − 1 = ' + i + '. On compare la clé aux éléments déjà triés, de droite à gauche.', o());
        for (;;) {
          cpt[5]++; t++; tj[j] = t;
          var vrai = i > 0 && T[i] > cle;
          var pourquoi = i > 0 ? 'i = ' + i + ' > 0 et T[' + i + '] = ' + T[i] + (vrai ? ' > ' : ' ≤ ') + 'clé = ' + cle
                               : 'i = 0 : on est arrivé au début du tableau';
          R.note(5, 'Test n° ' + t + ' de la ligne 5 (t' + sub(j) + ' vaut maintenant ' + t + ') : ' + pourquoi + (vrai ? ' → vrai, on décale.' : ' → faux, on sort de la boucle.'), o());
          if (!vrai) break;
          T[i + 1] = T[i]; cpt[6]++;
          R.note(6, 'T[' + (i + 1) + '] = T[' + i + '] = ' + T[i] + ' : l\'élément plus grand que la clé glisse d\'une case à droite.', o({ decale: i + 1 }));
          i = i - 1; cpt[7]++;
          R.note(7, 'i = i − 1 = ' + i + '.', o());
        }
        T[i + 1] = cle; cpt[8]++;
        R.note(8, 'T[' + (i + 1) + '] = clé = ' + cle + '. La clé est à sa place : T[1..' + j + '] est trié. Bilan : t' + sub(j) + ' = ' + t + '.', o({ place: i + 1 }));
        j++; i = null; cle = null;
      }
      return R.etats;
    },
    bilan: function (e, n) {
      var s = 0; for (var k in e.info.tj) s += e.info.tj[k];
      var total = somme(e.cpt), formule = 3 * s + 2 * n - 1;
      return 'Σ tⱼ = ' + s + '. En comptant c par instruction simple : T(' + n + ') = c × ' + total + ' = ' + total +
             'c. La formule T(n) = c(3 Σ tⱼ + 2n − 1) donne c(3×' + s + ' + 2×' + n + ' − 1) = ' + formule + 'c' + (formule === total ? ' ✓' : ' ✗');
    }
  };

  ALGOS.sequentielle = {
    lignes: ['Pour i = 1 à n', '  si T[i] = x', '    renvoyer Vrai', 'renvoyer Faux'],
    commentaires: [], param: 'x',
    trace: function (T0, x) {
      var T = [null].concat(T0), n = T0.length, R = enregistreur(T, 4), cpt = R.cpt, i = 1, comp = 0;
      function o(extra) {
        var marques = {}, classes = {};
        for (var p = 1; p < i && p <= n; p++) classes[p] = 'vu';
        if (extra && extra.trouve) classes[i] = 'pose';
        if (i <= n) marques[i] = ['i'];
        return { marques: marques, classes: classes, fini: extra && extra.fini,
                 vars: [['n', n], ['x', x, 'rouge'], ['i', i <= n ? i : '—'], ['comparaisons', comp]], info: { comp: comp } };
      }
      R.note(0, 'On cherche x = ' + x + ' en regardant les cases une par une, de gauche à droite.', o());
      for (;;) {
        cpt[1]++;
        if (i > n) { R.note(1, 'i = ' + i + ' > n : on a tout regardé.', o()); break; }
        R.note(1, 'i = ' + i + ' ≤ n : on regarde la case ' + i + '.', o());
        cpt[2]++; comp++;
        if (T[i] === x) {
          R.note(2, 'Comparaison n° ' + comp + ' : T[' + i + '] = ' + T[i] + ' = x. Trouvé !', o({ trouve: true }));
          cpt[3]++; R.note(3, 'On renvoie Vrai après ' + comp + ' comparaison' + (comp > 1 ? 's' : '') + '.', o({ trouve: true, fini: true }));
          return R.etats;
        }
        R.note(2, 'Comparaison n° ' + comp + ' : T[' + i + '] = ' + T[i] + ' ≠ ' + x + '. On passe à la case suivante.', o());
        i++;
      }
      cpt[4]++; R.note(4, 'x n\'est pas dans le tableau : on renvoie Faux après ' + comp + ' comparaisons, une par case.', o({ fini: true }));
      return R.etats;
    },
    bilan: function (e, n) {
      return e.info.comp + ' comparaison' + (e.info.comp > 1 ? 's' : '') + ' de T[i] avec x, pour n = ' + n +
             '. Au pire cas (x absent, ou dans la dernière case), il en faut n = ' + n + '.';
    }
  };

  ALGOS.dichotomie = {
    lignes: ['g = 1 ; d = n', 'tant que g ≤ d', '  m = ⌊(g + d) / 2⌋', '  si T[m] = x : renvoyer Vrai',
             '  si T[m] < x : g = m + 1', '  sinon : d = m − 1', 'renvoyer Faux'],
    commentaires: [], param: 'x', trie: true,
    trace: function (T0, x) {
      var T = [null].concat(T0), n = T0.length, R = enregistreur(T, 7), cpt = R.cpt;
      var g = 1, d = n, m = null, tours = 0;
      function o(extra) {
        var marques = {}, classes = {};
        for (var p = 1; p <= n; p++) if (p < g || p > d) classes[p] = 'elimine';
        if (m !== null && extra && extra.trouve) classes[m] = 'pose';
        else if (m !== null && !(extra && extra.horsm)) classes[m] = 'bouge';
        if (g >= 1 && g <= n) (marques[g] = marques[g] || []).push('g');
        if (d >= 1 && d <= n) (marques[d] = marques[d] || []).push('d');
        if (m !== null && !(extra && extra.horsm)) (marques[m] = marques[m] || []).push('m');
        return { marques: marques, classes: classes, fini: extra && extra.fini,
                 vars: [['n', n], ['x', x, 'rouge'], ['g', g], ['d', d], ['m', m === null ? '—' : m], ['tours', tours],
                        ['cases restantes', Math.max(0, d - g + 1)]], info: { tours: tours } };
      }
      cpt[1]++; R.note(1, 'Le tableau est trié. On cherche x = ' + x + ' dans la zone T[g..d] = T[1..' + n + '], tout le tableau.', o());
      for (;;) {
        cpt[2]++;
        if (g > d) { R.note(2, 'g = ' + g + ' > d = ' + d + ' : la zone de recherche est vide.', o({ horsm: true })); break; }
        R.note(2, 'g = ' + g + ' ≤ d = ' + d + ' : il reste ' + (d - g + 1) + ' case' + (d - g + 1 > 1 ? 's' : '') + ' à examiner.', o({ horsm: true }));
        tours++; m = Math.floor((g + d) / 2); cpt[3]++;
        R.note(3, 'Tour ' + tours + ' : on regarde le milieu, m = ⌊(' + g + ' + ' + d + ') / 2⌋ = ' + m + ', où T[' + m + '] = ' + T[m] + '.', o());
        cpt[4]++;
        if (T[m] === x) {
          R.note(4, 'T[' + m + '] = ' + x + ' : trouvé, en ' + tours + ' tour' + (tours > 1 ? 's' : '') + '.', o({ trouve: true, fini: true }));
          return R.etats;
        }
        R.note(4, 'T[' + m + '] = ' + T[m] + ' ≠ ' + x + '.', o());
        cpt[5]++;
        if (T[m] < x) { g = m + 1; R.note(5, T[m] + ' < ' + x + ' : x ne peut être qu\'à droite de m. g = ' + g + ' : la moitié gauche est éliminée.', o({ horsm: true })); }
        else { cpt[6]++; d = m - 1; R.note(6, T[m] + ' > ' + x + ' : x ne peut être qu\'à gauche de m. d = ' + d + ' : la moitié droite est éliminée.', o({ horsm: true })); }
      }
      cpt[7]++; R.note(7, x + ' n\'est pas dans le tableau. On renvoie Faux après ' + tours + ' tour' + (tours > 1 ? 's' : '') + '.', o({ fini: true, horsm: true }));
      return R.etats;
    },
    bilan: function (e, n) {
      var borne = Math.floor(Math.log2(Math.max(1, n))) + 1;
      return e.info.tours + ' tour' + (e.info.tours > 1 ? 's' : '') + ' de boucle (une comparaison avec le milieu à chaque tour), pour n = ' + n +
             '. Au pire cas il en faut ⌊log₂ n⌋ + 1 = ' + borne + ' : chaque tour divise au moins par deux la zone restante.';
    }
  };

  // ─────────────────────────────────────────────────────────────────────────
  blocs.forEach(function (bloc) {
    var algo = ALGOS[bloc.dataset.algo];
    if (!algo) return;
    var entrees = JSON.parse(bloc.dataset.entrees || '[]');

    var choix = entrees.map(function (e, k) {
      return '<button type="button" class="an-preset" data-k="' + k + '">' + ech(e[0]) + '</button>';
    }).join('');
    var aide = algo.param ? 'ex. 1, 4, 7, 9 ; 7' : 'ex. 5, 1, 4, 2';
    var etiquette = algo.param ? 'Ton tableau, puis un point-virgule et la valeur ' + algo.param : 'Ton tableau, valeurs séparées par des virgules';
    bloc.insertAdjacentHTML('beforeend',
      '<div class="an-entree"><span class="an-l">Entrée :</span>' + choix +
      '<label class="an-perso">ou la tienne <input type="text" placeholder="' + aide + '" aria-label="' + etiquette + '"></label>' +
      '<button type="button" class="an-ok btn ghost">Charger</button></div>' +
      '<div class="an-scene">' +
        '<div class="an-code" aria-label="Pseudo-code"><table><thead><tr><th>n°</th><th>instruction</th><th title="nombre d\'exécutions">exéc.</th></tr></thead><tbody></tbody></table></div>' +
        '<div class="an-droite"><div class="an-tab"></div><div class="an-vars"></div><div class="an-tj"></div></div>' +
      '</div>' +
      '<p class="an-msg" role="status" aria-live="polite"></p>' +
      '<div class="an-cmd">' +
        '<button type="button" class="btn ghost an-debut" title="Revenir au départ">⟲ Départ</button>' +
        '<button type="button" class="btn ghost an-prec">◀ Pas précédent</button>' +
        '<button type="button" class="btn an-suiv">Pas suivant ▶</button>' +
        '<button type="button" class="btn ghost an-auto">Lecture auto</button>' +
        '<button type="button" class="btn ghost an-fin" title="Aller à la fin">Fin ⏭</button>' +
        '<span class="an-compte"></span>' +
      '</div>' +
      '<p class="an-bilan" hidden></p>');

    var corps = bloc.querySelector('.an-code tbody');
    corps.innerHTML = algo.lignes.map(function (l, k) {
      var com = algo.commentaires.indexOf(k + 1) >= 0;
      return '<tr data-l="' + (k + 1) + '"' + (com ? ' class="com"' : '') + '><td>' + (k + 1) + '</td><td><code>' + ech(l) + '</code></td><td class="an-n">' + (com ? '—' : '0') + '</td></tr>';
    }).join('');
    var lignesEl = corps.querySelectorAll('tr');
    var tabEl = bloc.querySelector('.an-tab'), varsEl = bloc.querySelector('.an-vars'), extraEl = bloc.querySelector('.an-tj');
    var msgEl = bloc.querySelector('.an-msg'), compteEl = bloc.querySelector('.an-compte'), bilanEl = bloc.querySelector('.an-bilan');
    var autoBtn = bloc.querySelector('.an-auto');
    var etats = [], k = 0, n = 0, minuteur = null;

    function charger(T, p) { stop(); n = T.length; etats = algo.trace(T, p); k = 0; dessiner(); }

    function dessiner() {
      var e = etats[k];
      lignesEl.forEach(function (tr, idx) {
        var l = idx + 1;
        tr.classList.toggle('ici', l === e.ligne);
        if (!tr.classList.contains('com')) tr.querySelector('.an-n').textContent = e.cpt[l];
      });
      var h = '<div class="an-cases">';
      e.T.forEach(function (v, idx) {
        var p = idx + 1, cls = 'an-case' + (e.classes[p] ? ' ' + e.classes[p] : '');
        var mq = (e.marques[p] || []).map(function (m) { return '<span class="mq ' + m + '">' + m + '</span>'; }).join('');
        h += '<div class="' + cls + '"><span class="v">' + ech(v) + '</span><span class="idx">' + p + '</span><span class="mqs">' + mq + '</span></div>';
      });
      tabEl.innerHTML = h + '</div>';
      varsEl.innerHTML = e.vars.map(function (v) {
        return '<span' + (v[2] ? ' class="an-cle"' : '') + '>' + ech(v[0]) + ' = <b>' + ech(v[1]) + '</b></span>';
      }).join('');
      extraEl.innerHTML = e.extra;
      msgEl.textContent = e.msg;
      compteEl.textContent = 'pas ' + k + ' / ' + (etats.length - 1);
      bloc.querySelector('.an-prec').disabled = k === 0;
      bloc.querySelector('.an-debut').disabled = k === 0;
      bloc.querySelector('.an-suiv').disabled = k === etats.length - 1;
      bloc.querySelector('.an-fin').disabled = k === etats.length - 1;
      var fin = k === etats.length - 1;
      bilanEl.hidden = !fin;
      if (fin) { bilanEl.textContent = algo.bilan(e, n); stop(); }
    }

    function stop() { if (minuteur) { clearInterval(minuteur); minuteur = null; } autoBtn.textContent = 'Lecture auto'; }
    autoBtn.addEventListener('click', function () {
      if (minuteur) { stop(); return; }
      if (k === etats.length - 1) k = 0;
      autoBtn.textContent = 'Pause';
      minuteur = setInterval(function () { if (k < etats.length - 1) { k++; dessiner(); } else stop(); }, 900);
    });
    bloc.querySelector('.an-suiv').addEventListener('click', function () { stop(); if (k < etats.length - 1) { k++; dessiner(); } });
    bloc.querySelector('.an-prec').addEventListener('click', function () { stop(); if (k > 0) { k--; dessiner(); } });
    bloc.querySelector('.an-debut').addEventListener('click', function () { stop(); k = 0; dessiner(); });
    bloc.querySelector('.an-fin').addEventListener('click', function () { stop(); k = etats.length - 1; dessiner(); });

    var presets = bloc.querySelectorAll('.an-preset');
    function marquer(b) { presets.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); }
    presets.forEach(function (b) {
      b.addEventListener('click', function () { var e = entrees[+b.dataset.k]; marquer(b); charger(e[1].slice(), e[2]); });
    });
    var champ = bloc.querySelector('.an-perso input');
    function perso() {
      var parts = champ.value.split(';'), p;
      var vals = parts[0].split(/[,\s]+/).filter(Boolean).map(Number);
      if (!vals.length || vals.some(isNaN)) { msgEl.textContent = 'Écris des nombres séparés par des virgules' + (algo.param ? ', puis un point-virgule et la valeur cherchée, par exemple 1, 4, 7, 9 ; 7.' : ', par exemple 5, 1, 4, 2.'); return; }
      var maxi = algo.param ? 20 : 12;
      if (vals.length > maxi) { msgEl.textContent = maxi + ' valeurs au plus : au-delà, la trace devient trop longue à suivre pas à pas.'; return; }
      if (algo.param) {
        if (parts.length < 2 || parts[1].trim() === '' || isNaN(Number(parts[1]))) { msgEl.textContent = 'Ajoute la valeur cherchée après un point-virgule, par exemple 1, 4, 7, 9 ; 7.'; return; }
        p = Number(parts[1]);
      }
      if (algo.trie) {
        for (var q = 1; q < vals.length; q++) if (vals[q] < vals[q - 1]) { msgEl.textContent = 'La dichotomie exige un tableau trié dans l\'ordre croissant.'; return; }
      }
      marquer(null); charger(vals, p);
    }
    bloc.querySelector('.an-ok').addEventListener('click', perso);
    champ.addEventListener('keydown', function (ev) { if (ev.key === 'Enter') { ev.preventDefault(); perso(); } });

    if (presets.length) marquer(presets[0]);
    charger(entrees.length ? entrees[0][1].slice() : [3, 1, 2], entrees.length ? entrees[0][2] : undefined);
  });
})();
