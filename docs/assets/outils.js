/* Outils communs à toutes les pages : thème clair / sombre, progression affichée sur l'accueil. */
(function () {
  var racine = document.documentElement;

  // ----- thème -----
  function themeEffectif() {
    if (racine.dataset.theme) return racine.dataset.theme;
    return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function majBoutons() {
    var sombre = themeEffectif() === 'dark';
    document.querySelectorAll('.theme-btn').forEach(function (b) {
      b.textContent = sombre ? 'Thème clair' : 'Thème sombre';
      b.setAttribute('aria-pressed', String(sombre));
    });
  }
  document.querySelectorAll('.theme-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = themeEffectif() === 'dark' ? 'light' : 'dark';
      racine.dataset.theme = t;
      try { localStorage.setItem('complexite-theme', t); } catch (e) {}
      majBoutons();
    });
  });
  majBoutons();

  // ----- accueil : progression de chaque module -----
  var cartes = document.querySelectorAll('.mod-carte[data-module]');
  if (!cartes.length) return;
  var total = 0, valide = 0;
  cartes.forEach(function (c) {
    var fait = {};
    try { fait = JSON.parse(localStorage.getItem('complexite-progression-' + c.dataset.module) || '{}') || {}; } catch (e) {}
    var ids = (c.dataset.etapes || '').split(' ').filter(Boolean);
    var n = ids.filter(function (id) { return fait[id]; }).length;
    total += ids.length; valide += n;
    var barre = c.querySelector('.mod-prog i');
    if (barre) barre.style.width = (ids.length ? Math.round(100 * n / ids.length) : 0) + '%';
    var txt = c.querySelector('.mod-prog-txt');
    if (txt && n) txt.textContent = n + '/' + ids.length + ' validées';
    c.querySelectorAll('li[data-id]').forEach(function (li) { if (fait[li.dataset.id]) li.classList.add('fait'); });
  });
  var g = document.getElementById('prog-globale');
  if (g) g.textContent = valide
    ? valide + ' étape' + (valide > 1 ? 's' : '') + ' validée' + (valide > 1 ? 's' : '') + ' sur ' + total + '. Reprends où tu t\'es arrêté.'
    : 'Aucune étape validée pour l\'instant. Commence par le module 0, ou va directement à l\'étape pilote 3.3.';
})();
