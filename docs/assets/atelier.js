/* Ateliers de code : l'étudiant écrit, teste contre des cas cachés, puis vérifie avec SageMath. */
(function () {
  var ateliers = document.querySelectorAll('.atelier');
  if (!ateliers.length) return;

  var worker = null, pret = false, enAttente = null, minuteur = null;
  var DELAI = 10000;

  function lancerWorker(surPret) {
    worker = new Worker('assets/atelier-worker.js');
    pret = false;
    worker.onmessage = function (ev) {
      if (ev.data.type === 'pret') { pret = true; if (surPret) surPret(); }
      else if (ev.data.type === 'panne') { if (enAttente) enAttente({ erreur: 'Python n\'a pas pu se charger : ' + ev.data.message }); enAttente = null; }
      else if (ev.data.type === 'resultat') {
        clearTimeout(minuteur);
        var f = enAttente; enAttente = null;
        if (f) f(JSON.parse(ev.data.json));
      }
    };
    worker.onerror = function () {
      clearTimeout(minuteur);
      var f = enAttente; enAttente = null; worker = null;
      if (f) f({ erreur: 'Python n\'a pas pu se charger. Vérifie ta connexion, puis réessaie.' });
    };
  }

  function executer(code, tests, etat, retour) {
    if (location.protocol === 'file:') {
      retour({ erreur: 'L\'atelier a besoin que le site soit servi par un serveur. Ouvre la version en ligne, ou lance « python3 -m http.server » dans le dossier du site.' });
      return;
    }
    function envoyer() {
      etat('Exécution…');
      enAttente = retour;
      minuteur = setTimeout(function () {
        worker.terminate(); worker = null; enAttente = null;
        retour({ erreur: 'Arrêté après ' + (DELAI / 1000) + ' secondes : ton programme ne termine pas. Cherche une boucle dont la condition ne devient jamais fausse.' });
      }, DELAI);
      worker.postMessage({ code: code, tests: tests });
    }
    if (worker && pret) envoyer();
    else { etat('Chargement de Python (une dizaine de Mo la première fois)…'); lancerWorker(envoyer); }
  }

  function echapper(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  window.CXatelier = { executer: executer };

  ateliers.forEach(function (a) {
    var id = a.dataset.id, cle = 'complexite-atelier-' + id;
    var zone = a.querySelector('textarea'), depart = zone.value;
    var tests = JSON.parse(a.querySelector('script.atelier-tests').textContent);
    var res = a.querySelector('.atelier-res'), etatEl = a.querySelector('.atelier-etat');
    var corrige = a.querySelector('.atelier-corrige');
    try { var garde = localStorage.getItem(cle); if (garde) zone.value = garde; } catch (e) {}
    try { if (localStorage.getItem(cle + '-essai')) corrige.hidden = false; } catch (e) {}

    zone.addEventListener('input', function () { try { localStorage.setItem(cle, zone.value); } catch (e) {} });
    zone.addEventListener('keydown', function (ev) {
      var d = zone.selectionStart, f = zone.selectionEnd, v = zone.value;
      if (ev.key === 'Tab') {
        ev.preventDefault();
        zone.value = v.slice(0, d) + '    ' + v.slice(f); zone.selectionStart = zone.selectionEnd = d + 4;
        zone.dispatchEvent(new Event('input'));
      } else if (ev.key === 'Enter') {
        var debut = v.lastIndexOf('\n', d - 1) + 1, ligne = v.slice(debut, d);
        var retrait = (ligne.match(/^ */) || [''])[0] + (/:\s*$/.test(ligne) ? '    ' : '');
        ev.preventDefault();
        zone.value = v.slice(0, d) + '\n' + retrait + v.slice(f); zone.selectionStart = zone.selectionEnd = d + 1 + retrait.length;
        zone.dispatchEvent(new Event('input'));
      }
    });

    function etat(t) { etatEl.textContent = t; }
    function boutons(actifs) { a.querySelectorAll('.atelier-b button').forEach(function (b) { b.disabled = !actifs; }); }

    function afficher(r, avecTests) {
      boutons(true); etat('');
      var h = '';
      if (r.erreur) h += '<p class="at-ko">' + echapper(r.erreur) + '</p>';
      if (r.sortie) h += '<p class="lab">Ce que ton programme a affiché</p><pre class="at-sortie">' + echapper(r.sortie) + '</pre>';
      if (!r.erreur && !avecTests && !r.sortie) h += '<p class="at-info">Aucune erreur, et rien n\'a été affiché. Ajoute un <code>print(...)</code> pour voir un résultat.</p>';
      if (avecTests && r.tests && r.tests.length) {
        var ok = r.tests.filter(function (t) { return t.ok; }).length, tout = ok === r.tests.length;
        h += '<p class="' + (tout ? 'at-ok' : 'at-ko') + '">' + ok + ' test' + (ok > 1 ? 's' : '') + ' sur ' + r.tests.length + ' réussi' + (ok > 1 ? 's' : '') + (tout ? ' ✓' : '') + '</p><ul class="at-tests">';
        r.tests.forEach(function (t) {
          h += '<li class="' + (t.ok ? 'ok' : 'ko') + '"><code>' + echapper(t.appel) + '</code>' +
               (t.ok ? '' : '<br>attendu : ' + echapper(t.attendu) + '<br>obtenu : <code>' + echapper(t.obtenu) + '</code>') + '</li>';
        });
        h += '</ul>';
        if (tout) {
          var manque = window.MCS ? window.MCS.etape(a.closest('section.lesson'), 'atelier') : [];
          h += '<p class="at-ok">' + (manque.indexOf('qcm') >= 0
            ? 'Atelier réussi. Il reste le test de sortie (temps 4) pour valider l\'étape.'
            : 'Atelier réussi : étape validée ✓') + '</p>';
        }
      }
      res.innerHTML = h; res.hidden = false;
      if (avecTests) { corrige.hidden = false; try { localStorage.setItem(cle + '-essai', '1'); } catch (e) {} }
    }

    a.querySelector('.at-executer').addEventListener('click', function () {
      boutons(false); executer(zone.value, [], etat, function (r) { afficher(r, false); });
    });
    a.querySelector('.at-tester').addEventListener('click', function () {
      boutons(false); executer(zone.value, tests, etat, function (r) { afficher(r, true); });
    });
    a.querySelector('.at-reinit').addEventListener('click', function () {
      zone.value = depart; try { localStorage.removeItem(cle); } catch (e) {}
      res.hidden = true;
    });
  });

  // ----- cellules SageMath : chargées à la demande depuis le service SageMathCell -----
  var sageCharge = null;
  function chargerSage() {
    if (!sageCharge) sageCharge = new Promise(function (ok, ko) {
      var s = document.createElement('script');
      s.src = 'https://sagecell.sagemath.org/static/embedded_sagecell.js';
      s.onload = function () { ok(); }; s.onerror = function () { sageCharge = null; ko(); };
      document.head.appendChild(s);
    });
    return sageCharge;
  }
  document.querySelectorAll('.sage-atelier').forEach(function (bloc) {
    var bouton = bloc.querySelector('.sage-ouvrir'), cellule = bloc.querySelector('.sage-cellule'), msg = bloc.querySelector('.sage-msg');
    bouton.addEventListener('click', function () {
      bouton.disabled = true; msg.textContent = 'Connexion à SageMathCell…';
      chargerSage().then(function () {
        window.sagecell.makeSagecell({ inputLocation: cellule, evalButtonText: 'Exécuter', languages: ['sage'], hide: ['permalink', 'fullScreen'] });
        cellule.hidden = false; bouton.hidden = true;
        msg.textContent = 'Modifie le code, puis clique sur Exécuter. Le calcul se fait sur les serveurs du projet SageMath.';
      }, function () {
        bouton.disabled = false;
        msg.textContent = 'SageMathCell est injoignable pour le moment. Réessaie plus tard, ou colle ce code sur sagecell.sagemath.org.';
        cellule.hidden = false;
      });
    });
  });
})();
