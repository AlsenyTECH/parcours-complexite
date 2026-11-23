/* Animateur pas à pas : l'algorithme tourne instruction par instruction,
   avec le nombre d'exécutions de chaque ligne et les tⱼ, comme dans un tableau d'analyse de coût.
   La trace complète est calculée d'avance : on peut avancer, reculer, rejouer. */
(function () {
  var blocs = document.querySelectorAll('.anim');
  if (!blocs.length) return;

  function ech(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  // ─────────────────────────────────────────────────────────────────────────
  // Algorithmes connus. trace(T) renvoie la liste des états successifs.
  // Lignes numérotées comme dans l'énoncé de l'examen.
  // ─────────────────────────────────────────────────────────────────────────
  var ALGOS = {
    insertion: {
      titre: 'Tri par insertion',
      lignes: [
        'Pour j = 2 à n',
        '  clé = T[j]',
        '  ▹ insérer T[j] dans T[1..j−1] trié',
        '  i = j − 1',
        '  tant que i > 0 et T[i] > clé',
        '    T[i+1] = T[i]',
        '    i = i − 1',
        '  T[i+1] = clé'
      ],
      commentaires: [3],
      trace: function (T0) {
        var T = [null].concat(T0), n = T0.length, cpt = [0, 0, 0, 0, 0, 0, 0, 0, 0], tj = {};
        var etats = [], j = 2, i = null, cle = null, t = 0;
        function note(ligne, msg, extra) {
          etats.push({ ligne: ligne, T: T.slice(1), j: j, i: i, cle: cle, cpt: cpt.slice(), tj: JSON.parse(JSON.stringify(tj)),
                       msg: msg, decale: extra && extra.decale, place: extra && extra.place, fini: extra && extra.fini });
        }
        note(0, 'Départ : n = ' + n + '. Clique sur « Pas suivant » pour exécuter la première instruction.');
        for (;;) {
          cpt[1]++;
          if (j > n) { note(1, 'Test de la boucle Pour : j = ' + j + ' > n = ' + n + ', la boucle s\'arrête. Ce dernier test compte aussi : la ligne 1 s\'exécute n fois.', { fini: true }); break; }
          note(1, 'Test de la boucle Pour : j = ' + j + ' ≤ n = ' + n + ', on entre dans la boucle.');
          cle = T[j]; cpt[2]++;
          note(2, 'clé = T[' + j + '] = ' + cle + '. C\'est la carte qu\'on va ranger.');
          i = j - 1; cpt[4]++; t = 0;
          note(4, 'i = j − 1 = ' + i + '. On va comparer la clé aux éléments déjà triés, de droite à gauche.');
          for (;;) {
            cpt[5]++; t++; tj[j] = t;
            var vrai = i > 0 && T[i] > cle;
            var pourquoi = i > 0
              ? 'i = ' + i + ' > 0 et T[' + i + '] = ' + T[i] + (vrai ? ' > ' : ' ≤ ') + 'clé = ' + cle
              : 'i = 0 : on est arrivé au début du tableau';
            note(5, 'Test n° ' + t + ' de la ligne 5 (t' + sub(j) + ' vaut maintenant ' + t + ') : ' + pourquoi + (vrai ? ' → vrai, on décale.' : ' → faux, on sort de la boucle.'));
            if (!vrai) break;
            T[i + 1] = T[i]; cpt[6]++;
            note(6, 'T[' + (i + 1) + '] = T[' + i + '] = ' + T[i] + ' : l\'élément plus grand que la clé glisse d\'une case à droite.', { decale: i + 1 });
            i = i - 1; cpt[7]++;
            note(7, 'i = i − 1 = ' + i + '.');
          }
          T[i + 1] = cle; cpt[8]++;
          note(8, 'T[' + (i + 1) + '] = clé = ' + cle + '. La clé est à sa place : T[1..' + j + '] est trié. Bilan : t' + sub(j) + ' = ' + t + '.', { place: i + 1 });
          j++; i = null; cle = null;
        }
        return etats;
      },
      bilan: function (e, n) {
        var s = 0; for (var k in e.tj) s += e.tj[k];
        var total = e.cpt.reduce(function (a, b) { return a + b; }, 0);
        var formule = 3 * s + 2 * n - 1;
        return 'Σ tⱼ = ' + s + '. En comptant c par instruction simple : T(' + n + ') = c × ' + total +
               ' = ' + total + 'c. La formule T(n) = c(3 Σ tⱼ + 2n − 1) donne c(3×' + s + ' + 2×' + n + ' − 1) = ' + formule + 'c' +
               (formule === total ? ' ✓' : ' ✗');
      }
    }
  };

  function sub(k) {
    return String(k).split('').map(function (c) { return '₀₁₂₃₄₅₆₇₈₉'[+c]; }).join('');
  }

  blocs.forEach(function (bloc) {
    var algo = ALGOS[bloc.dataset.algo];
    if (!algo) return;
    var entrees = JSON.parse(bloc.dataset.entrees || '[]');

    var choix = entrees.map(function (e, k) {
      return '<button type="button" class="an-preset" data-k="' + k + '">' + ech(e[0]) + '</button>';
    }).join('');
    bloc.insertAdjacentHTML('beforeend',
      '<div class="an-entree"><span class="an-l">Entrée :</span>' + choix +
      '<label class="an-perso">ou la tienne <input type="text" inputmode="numeric" placeholder="ex. 5, 1, 4, 2" aria-label="Ton tableau, valeurs séparées par des virgules"></label>' +
      '<button type="button" class="an-ok btn ghost">Charger</button></div>' +
      '<div class="an-scene">' +
        '<div class="an-code" aria-label="Pseudo-code"><table><thead><tr><th>n°</th><th>instruction</th><th title="nombre d\'exécutions">exéc.</th></tr></thead><tbody></tbody></table></div>' +
        '<div class="an-droite"><div class="an-tab" aria-live="off"></div><div class="an-vars"></div><div class="an-tj"></div></div>' +
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
    var tabEl = bloc.querySelector('.an-tab'), varsEl = bloc.querySelector('.an-vars'), tjEl = bloc.querySelector('.an-tj');
    var msgEl = bloc.querySelector('.an-msg'), compteEl = bloc.querySelector('.an-compte'), bilanEl = bloc.querySelector('.an-bilan');
    var autoBtn = bloc.querySelector('.an-auto');

    var etats = [], k = 0, n = 0, minuteur = null;

    function charger(T) {
      stop();
      n = T.length; etats = algo.trace(T); k = 0; dessiner();
    }

    function dessiner() {
      var e = etats[k];
      lignesEl.forEach(function (tr, idx) {
        var l = idx + 1;
        tr.classList.toggle('ici', l === e.ligne);
        var c = tr.querySelector('.an-n'); if (!tr.classList.contains('com')) c.textContent = e.cpt[l];
      });
      var h = '<div class="an-cases">';
      e.T.forEach(function (v, idx) {
        var p = idx + 1, cls = 'an-case';
        if (e.fini || p < e.j || (e.place && p <= e.j)) cls += ' trie';
        if (p === e.decale) cls += ' bouge';
        if (p === e.place) cls += ' pose';
        var marques = '';
        if (!e.fini && e.j === p) marques += '<span class="mq j">j</span>';
        if (e.i !== null && e.i === p) marques += '<span class="mq i">i</span>';
        h += '<div class="' + cls + '"><span class="v">' + ech(v) + '</span><span class="idx">' + p + '</span><span class="mqs">' + marques + '</span></div>';
      });
      h += '</div>';
      tabEl.innerHTML = h;
      varsEl.innerHTML = '<span>n = <b>' + n + '</b></span>' +
        '<span>j = <b>' + (e.fini || e.j === null ? '—' : e.j) + '</b></span>' +
        '<span>i = <b>' + (e.i === null ? '—' : e.i) + '</b></span>' +
        '<span class="an-cle">clé = <b>' + (e.cle === null ? '—' : ech(e.cle)) + '</b></span>';
      var cles = Object.keys(e.tj);
      tjEl.innerHTML = cles.length
        ? '<table><tr><th>j</th>' + cles.map(function (x) { return '<td>' + x + '</td>'; }).join('') + '</tr>' +
          '<tr><th>t<sub>j</sub></th>' + cles.map(function (x) { return '<td>' + e.tj[x] + '</td>'; }).join('') + '</tr></table>'
        : '<p class="an-vide">Les t<sub>j</sub> (nombre de tests de la ligne 5 pour chaque j) s\'afficheront ici.</p>';
      msgEl.textContent = e.msg;
      compteEl.textContent = 'pas ' + k + ' / ' + (etats.length - 1);
      bloc.querySelector('.an-prec').disabled = k === 0;
      bloc.querySelector('.an-debut').disabled = k === 0;
      bloc.querySelector('.an-suiv').disabled = k === etats.length - 1;
      bloc.querySelector('.an-fin').disabled = k === etats.length - 1;
      bilanEl.hidden = !e.fini;
      if (e.fini) bilanEl.textContent = algo.bilan(e, n);
      if (k === etats.length - 1) stop();
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
      b.addEventListener('click', function () { marquer(b); charger(entrees[+b.dataset.k][1].slice()); });
    });
    var champ = bloc.querySelector('.an-perso input');
    function perso() {
      var vals = champ.value.split(/[,;\s]+/).filter(Boolean).map(Number);
      if (!vals.length || vals.some(isNaN)) { msgEl.textContent = 'Écris des nombres séparés par des virgules, par exemple 5, 1, 4, 2.'; return; }
      if (vals.length > 12) { msgEl.textContent = 'Douze valeurs au plus : au-delà, la trace devient trop longue à suivre pas à pas.'; return; }
      marquer(null); charger(vals);
    }
    bloc.querySelector('.an-ok').addEventListener('click', perso);
    champ.addEventListener('keydown', function (ev) { if (ev.key === 'Enter') { ev.preventDefault(); perso(); } });

    if (presets.length) { marquer(presets[0]); }
    charger(entrees.length ? entrees[0][1].slice() : [3, 1, 2]);
  });
})();
