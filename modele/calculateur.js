/* Calculateurs : temps d'exécution selon la complexité, taille maximale traitable, coût d'une attaque.
   Tous les calculs se font en logarithme décimal : 2^1000 ou 1000! restent manipulables. */
(function () {
  var LN10 = Math.LN10;
  function lgamma(x) { // Stirling-Lanczos, suffisant pour log10(n!)
    if (x < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * x)) - lgamma(1 - x);
    var g = 7, c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
      -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
    x -= 1; var a = c[0], t = x + g + 0.5;
    for (var i = 1; i < 9; i++) a += c[i] / (x + i);
    return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
  }
  // log10 de f(n), pour n ≥ 1
  var FONCTIONS = [
    ['log₂ n', function (n) { var v = Math.log2(n); return v > 0 ? Math.log10(v) : -Infinity; }],
    ['√n', function (n) { return 0.5 * Math.log10(n); }],
    ['n', function (n) { return Math.log10(n); }],
    ['n log₂ n', function (n) { var v = Math.log2(n); return v > 0 ? Math.log10(n) + Math.log10(v) : -Infinity; }],
    ['n²', function (n) { return 2 * Math.log10(n); }],
    ['n³', function (n) { return 3 * Math.log10(n); }],
    ['n⁵', function (n) { return 5 * Math.log10(n); }],
    ['2ⁿ', function (n) { return n * Math.log10(2); }],
    ['n!', function (n) { return lgamma(n + 1) / LN10; }]
  ];
  var AN = 3.15576e7, UNIVERS = 13.8e9 * AN;

  function sci(l) { // affiche 10^l joliment
    if (l < 6) return Math.round(Math.pow(10, l)).toLocaleString('fr-FR');
    var e = Math.floor(l), m = Math.pow(10, l - e);
    if (m >= 9.995) { m = 1; e++; }
    return m.toFixed(2).replace('.', ',') + ' × 10<sup>' + e + '</sup>';
  }
  function duree(ls) { // ls = log10(secondes)
    if (ls === -Infinity) return '0';
    var s = Math.pow(10, ls);
    if (ls > Math.log10(UNIVERS)) return '<span class="cal-astro">' + sci(ls - Math.log10(AN)) + ' ans</span><br><small>' + sci(ls - Math.log10(UNIVERS)) + ' × l\'âge de l\'Univers</small>';
    if (s < 1e-6) return (s * 1e9).toPrecision(2).replace('.', ',') + ' ns';
    if (s < 1e-3) return (s * 1e6).toPrecision(3).replace('.', ',') + ' µs';
    if (s < 1) return (s * 1e3).toPrecision(3).replace('.', ',') + ' ms';
    if (s < 60) return s.toPrecision(3).replace('.', ',') + ' s';
    if (s < 3600) return (s / 60).toPrecision(3).replace('.', ',') + ' min';
    if (s < 86400) return (s / 3600).toPrecision(3).replace('.', ',') + ' h';
    if (s < AN) return (s / 86400).toPrecision(3).replace('.', ',') + ' jours';
    if (s < 100 * AN) return (s / AN).toPrecision(3).replace('.', ',') + ' ans';
    return '<span class="cal-astro">' + sci(ls - Math.log10(AN * 100)) + ' siècles</span>';
  }
  function niveau(ls) { return ls < 0 ? 'ok' : ls < Math.log10(3600) ? 'moyen' : ls < Math.log10(AN) ? 'long' : 'impossible'; }

  // ----- 1. combien de temps ? -----
  var t1 = document.getElementById('cal-temps');
  if (t1) {
    var vit = t1.querySelector('.cal-vitesse'), ns = t1.querySelector('.cal-n'), sortie = t1.querySelector('.cal-sortie');
    function maj1() {
      var v = Math.log10(Number(vit.value));
      var liste = ns.value.split(/[,;\s]+/).map(Number).filter(function (x) { return x >= 1 && isFinite(x); }).slice(0, 5);
      if (!liste.length) { sortie.innerHTML = '<p>Indique au moins une taille n.</p>'; return; }
      var h = '<div class="table-wrap"><table class="cal-tab"><thead><tr><th>Coût</th>' +
        liste.map(function (n) { return '<th>n = ' + n.toLocaleString('fr-FR') + '</th>'; }).join('') + '</tr></thead><tbody>';
      FONCTIONS.forEach(function (f) {
        h += '<tr><th>' + f[0] + '</th>' + liste.map(function (n) {
          var ls = f[1](n) - v; return '<td class="' + niveau(ls) + '">' + duree(ls) + '</td>';
        }).join('') + '</tr>';
      });
      sortie.innerHTML = h + '</tbody></table></div>';
    }
    vit.addEventListener('change', maj1); ns.addEventListener('input', maj1); maj1();
  }

  // ----- 2. quelle taille dans un temps donné ? -----
  var t2 = document.getElementById('cal-taille');
  if (t2) {
    var vit2 = t2.querySelector('.cal-vitesse'), sortie2 = t2.querySelector('.cal-sortie');
    var BUDGETS = [['1 seconde', 1], ['1 minute', 60], ['1 heure', 3600], ['1 jour', 86400], ['1 an', AN], ['1 siècle', 100 * AN]];
    function nmax(f, lb) { // plus grand n entier avec f(n) ≤ 10^lb
      if (f(1) > lb && f(2) > lb) return 0;
      var lo = 1, hi = 2;
      while (f(hi) <= lb && hi < 1e300) hi *= 2;
      if (hi >= 1e300) return Infinity;
      while (hi - lo > 1 && hi / lo > 1 + 1e-12) { var mid = Math.floor((lo + hi) / 2); if (f(mid) <= lb) lo = mid; else hi = mid; }
      return lo;
    }
    function aff(n) {
      if (n === Infinity) return '∞';
      if (n < 1e6) return n.toLocaleString('fr-FR');
      return sci(Math.log10(n));
    }
    function maj2() {
      var v = Math.log10(Number(vit2.value));
      var h = '<div class="table-wrap"><table class="cal-tab"><thead><tr><th>Coût</th>' +
        BUDGETS.map(function (b) { return '<th>en ' + b[0] + '</th>'; }).join('') + '</tr></thead><tbody>';
      FONCTIONS.forEach(function (f) {
        if (f[0] === 'log₂ n') return;
        h += '<tr><th>' + f[0] + '</th>' + BUDGETS.map(function (b) { return '<td>' + aff(nmax(f[1], v + Math.log10(b[1]))) + '</td>'; }).join('') + '</tr>';
      });
      sortie2.innerHTML = h + '</tbody></table></div>';
    }
    vit2.addEventListener('change', maj2); maj2();
  }

  // ----- 3. le coût d'une attaque -----
  var t3 = document.getElementById('cal-attaque');
  if (t3) {
    var bits = t3.querySelector('.cal-bits'), vit3 = t3.querySelector('.cal-vitesse'), sortie3 = t3.querySelector('.cal-sortie');
    var rsa = t3.querySelector('.cal-rsa'), sortieRsa = t3.querySelector('.cal-sortie-rsa');
    function maj3() {
      var k = Number(bits.value), v = Math.log10(Number(vit3.value));
      var lMoy = (k - 1) * Math.log10(2) - v, lPire = k * Math.log10(2) - v;
      sortie3.innerHTML = '<p>Il y a 2<sup>' + k + '</sup> ≈ ' + sci(k * Math.log10(2)) + ' clés. En moyenne, on trouve la bonne après en avoir essayé la moitié :</p>' +
        '<p class="cal-gros ' + niveau(lMoy) + '">' + duree(lMoy) + '</p>' +
        '<p class="cal-note">Au pire cas (la bonne clé est la dernière essayée) : ' + duree(lPire) + '.</p>';
    }
    function majRsa() {
      var b = Number(rsa.value), lnN = b * Math.LN2, c = Math.cbrt(64 / 9);
      var lnL = c * Math.cbrt(lnN) * Math.pow(Math.log(lnN), 2 / 3);
      var bitsSec = lnL / Math.LN2;
      sortieRsa.innerHTML = '<p>Pour un module N de ' + b + ' bits, L<sub>N</sub>[1/3, (64/9)<sup>1/3</sup>] ≈ 2<sup>' + bitsSec.toFixed(1).replace('.', ',') + '</sup> opérations, soit environ <b>' + Math.round(bitsSec) + ' bits de sécurité</b> si l\'on oublie le o(1) de la formule.</p>' +
        '<p class="cal-note">Les tables officielles (NIST, ANSSI), qui tiennent compte des constantes réelles du crible, retiennent ' +
        ({ 1024: '80', 2048: '112', 3072: '128', 7680: '192', 15360: '256' }[b] || '—') + ' bits pour cette taille : la formule asymptotique donne l\'ordre de grandeur, pas la valeur exacte.</p>';
    }
    bits.addEventListener('input', maj3); vit3.addEventListener('change', maj3); rsa.addEventListener('change', majRsa);
    maj3(); majRsa();
  }
})();
