/* Navigation d'un module : une étape à la fois, sommaire généré, progression gardée sur l'appareil.
   Repris du « Parcours Algèbre linéaire » et du site « Fondements MCS ». */
(function(){
  var lessons = Array.prototype.slice.call(document.querySelectorAll('section.lesson'));
  if (!lessons.length) return;

  var module_ = document.body.dataset.module || 'x';
  var CLE = 'complexite-progression-' + module_;
  var ids = lessons.map(function(s){ return s.id; });

  var done = {};
  try { done = JSON.parse(localStorage.getItem(CLE) || '{}') || {}; } catch(e){ done = {}; }
  function save(){ try { localStorage.setItem(CLE, JSON.stringify(done)); } catch(e){} }

  // ----- sommaire -----
  var nav = document.getElementById('nav'), html = '', partie = null, n = 0;
  lessons.forEach(function(s){
    var p = s.dataset.part || '';
    if (p !== partie){
      if (partie !== null) html += '</ul>';
      if (p) html += '<p class="nav-part">' + p + '</p>';
      html += '<ul class="nav-list">';
      partie = p;
    }
    var num = s.dataset.num || (s.dataset.part ? String(++n) : '·');
    html += '<li><a href="#' + s.id + '" data-id="' + s.id + '">' +
            '<span class="nav-n">' + num + '</span><span>' + s.dataset.title + '</span></a></li>';
  });
  html += '</ul>';
  nav.innerHTML = html;

  var links = Array.prototype.slice.call(nav.querySelectorAll('a'));
  var progFill = document.getElementById('prog-fill'),
      progTxt  = document.getElementById('prog-txt'),
      mini     = document.getElementById('mini-prog');

  function refreshProgress(){
    var total = 0, fait = 0;
    lessons.forEach(function(s){ if (s.dataset.part){ total++; if (done[s.id]) fait++; } });
    var pct = total ? Math.round(fait / total * 100) : 0;
    if (progFill) progFill.style.width = pct + '%';
    if (progTxt) progTxt.textContent = fait + ' sur ' + total + ' étapes validées';
    if (mini) mini.textContent = fait + '/' + total;
    links.forEach(function(a){ a.classList.toggle('done', !!done[a.dataset.id]); });
  }

  // ----- MathJax : une section à la fois -----
  var typeset = {};
  function renderMath(el){
    if (!el || typeset[el.id]) return;
    if (!(window.MathJax && MathJax.typesetPromise)) return;
    typeset[el.id] = true;
    MathJax.typesetPromise([el]).catch(function(){ typeset[el.id] = false; });
  }

  // ----- menu mobile -----
  var side = document.getElementById('side'), scrim = document.getElementById('scrim'), menuBtn = document.getElementById('menu-btn');
  function closeMenu(){ side.classList.remove('open'); scrim.hidden = true; menuBtn.setAttribute('aria-expanded','false'); }
  if (menuBtn){
    menuBtn.addEventListener('click', function(){
      var o = !side.classList.contains('open');
      side.classList.toggle('open', o); scrim.hidden = !o; menuBtn.setAttribute('aria-expanded', String(o));
    });
    scrim.addEventListener('click', closeMenu);
  }

  // ----- affichage d'une étape -----
  var prev = document.getElementById('prev'), next = document.getElementById('next'), doneNote = document.getElementById('done-note');
  var current = 0;
  function show(id, scroll){
    var i = ids.indexOf(id); if (i < 0) i = 0;
    current = i;
    document.querySelectorAll('video').forEach(function(v){ try { v.pause(); } catch(e){} });
    lessons.forEach(function(s, k){ s.hidden = k !== i; });
    links.forEach(function(a){ if (a.dataset.id === ids[i]) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });
    renderMath(lessons[i]);
    prev.hidden = i === 0;
    if (i > 0) prev.setAttribute('href', '#' + ids[i-1]);
    var last = i === ids.length - 1;
    var suite = document.body.dataset.suivant || '';
    if (last && suite){ next.setAttribute('href', suite); next.textContent = 'Module suivant →'; }
    else { next.setAttribute('href', last ? '#' + ids[0] : '#' + ids[i+1]);
           var aTest = !!lessons[i].querySelector('.qcm[data-role="sortie"]');
           next.textContent = i === 0 ? 'Commencer ce module →' : (last ? 'Revenir au début' : (aTest ? 'Étape suivante →' : "J'ai compris, étape suivante →")); }
    doneNote.hidden = !done[ids[i]] || i === 0;
    closeMenu();
    if (scroll) window.scrollTo(0, 0);
  }
  next.addEventListener('click', function(){
    if (current > 0 && !lessons[current].querySelector('.qcm[data-role="sortie"]')){
      done[ids[current]] = true; save(); refreshProgress();
    }
  });
  window.addEventListener('hashchange', function(){ show(location.hash.slice(1), true); });

  // ----- corrections : formules rendues à l'ouverture -----
  document.querySelectorAll('.exo details').forEach(function(d){
    d.addEventListener('toggle', function(){
      if (!d.open || !d.classList.contains('tex2jax_ignore')) return;
      d.classList.remove('tex2jax_ignore');
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([d]).catch(function(){});
    });
  });

  // ----- les quatre temps d'un nœud -----
  function ouvrirTemps(section, t, defiler){
    var onglets = section.querySelectorAll('.onglet'), panneaux = section.querySelectorAll('.panneau');
    onglets.forEach(function(o){
      var actif = Number(o.dataset.t) === t;
      o.setAttribute('aria-selected', String(actif));
      if (actif) o.classList.add('vu');
    });
    panneaux.forEach(function(p){ p.hidden = Number(p.dataset.t) !== t; });
    if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([section]).catch(function(){});
    if (defiler){ var bloc = section.querySelector('.temps'); if (bloc) bloc.scrollIntoView({block:'start'}); }
  }
  lessons.forEach(function(section){
    section.querySelectorAll('.onglet').forEach(function(o){
      o.addEventListener('click', function(){ ouvrirTemps(section, Number(o.dataset.t), false); });
    });
    section.querySelectorAll('.aller').forEach(function(b){
      b.addEventListener('click', function(){ ouvrirTemps(section, Number(b.dataset.t), true); });
    });
    var premier = section.querySelector('.onglet'); if (premier) premier.classList.add('vu');
  });

  // ----- validation d'un nœud : toutes ses épreuves (QCM de sortie, atelier de code) -----
  var CLE_ETATS = CLE + '-epreuves', etats = {};
  try { etats = JSON.parse(localStorage.getItem(CLE_ETATS) || '{}') || {}; } catch(e){ etats = {}; }
  function exigences(section){
    var e = [];
    if (section.querySelector('.qcm[data-role="sortie"]')) e.push('qcm');
    if (section.querySelector('.atelier')) e.push('atelier');
    return e;
  }
  function etape(section, cle){
    if (!section) return [];
    var id = section.id; etats[id] = etats[id] || {}; etats[id][cle] = true;
    try { localStorage.setItem(CLE_ETATS, JSON.stringify(etats)); } catch(e){}
    var manque = exigences(section).filter(function(k){ return !etats[id][k]; });
    if (!manque.length){ done[id] = true; save(); refreshProgress(); doneNote.hidden = false; }
    return manque;
  }
  window.MCS = { etape: etape };
  window.CX = window.MCS;

  // ----- QCM d'entrée et de sortie -----
  document.querySelectorAll('form.qcm').forEach(function(f){
    f.addEventListener('submit', function(ev){
      ev.preventDefault();
      var questions = f.querySelectorAll('.qcm-q'), bonnes = 0, repondues = 0;
      questions.forEach(function(q){
        var bonne = Number(q.dataset.bonne), choisi = q.querySelector('input:checked');
        q.querySelectorAll('.qcm-o').forEach(function(l){ l.classList.remove('juste','faux'); });
        if (!choisi) return;
        repondues++;
        var ok = Number(choisi.value) === bonne;
        if (ok) bonnes++;
        choisi.closest('.qcm-o').classList.add(ok ? 'juste' : 'faux');
        q.querySelectorAll('.qcm-o')[bonne].classList.add('juste');
        q.querySelector('.qcm-x').hidden = false;
      });
      var res = f.querySelector('.qcm-res'), seuil = Number(f.dataset.seuil), section = f.closest('section.lesson');
      res.hidden = false;
      if (repondues < questions.length){ res.className = 'qcm-res ko'; res.textContent = 'Réponds à toutes les questions.'; return; }
      var reussi = bonnes >= seuil;
      res.className = 'qcm-res ' + (reussi ? 'ok' : 'ko');
      if (f.dataset.role === 'entree'){
        res.textContent = reussi
          ? bonnes + ' sur ' + questions.length + ' : tu maîtrises déjà l\'essentiel. Va directement au temps 4, ou passe à l\'étape suivante.'
          : bonnes + ' sur ' + questions.length + ' : cette étape est faite pour toi. Commence par le temps 1.';
      } else {
        var manque = reussi ? etape(section, 'qcm') : [];
        res.textContent = !reussi
          ? bonnes + ' sur ' + questions.length + ' : reprends les explications ci-dessus, puis réessaie.'
          : (manque.indexOf('atelier') >= 0
              ? bonnes + ' sur ' + questions.length + ' : test réussi. Il reste l\'atelier de code (temps 3) pour valider l\'étape.'
              : bonnes + ' sur ' + questions.length + ' : étape validée ✓');
      }
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([f]).catch(function(){});
    });
  });

  // ----- blocs repliés hors exercices : formules rendues à l'ouverture -----
  document.querySelectorAll('.preuve > details, .atoi > details, .exo .indice').forEach(function(d){
    d.addEventListener('toggle', function(){
      if (!d.open || !d.classList.contains('tex2jax_ignore')) return;
      d.classList.remove('tex2jax_ignore');
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([d]).catch(function(){});
    });
  });

  // ----- bouton copier du code -----
  document.querySelectorAll('.copier').forEach(function(b){
    b.addEventListener('click', function(){
      var pre = b.closest('.code').querySelector('pre');
      var txt = pre ? pre.innerText : '';
      var ok = function(){ var a = b.textContent; b.textContent = 'copié'; setTimeout(function(){ b.textContent = a; }, 1400); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, function(){});
      else { try { var t = document.createElement('textarea'); t.value = txt; document.body.appendChild(t); t.select(); document.execCommand('copy'); document.body.removeChild(t); ok(); } catch(e){} }
    });
  });

  refreshProgress();
  show(location.hash.slice(1) || ids[0], false);
  var tries = 0, wait = setInterval(function(){
    if (window.MathJax && MathJax.typesetPromise){ clearInterval(wait); renderMath(lessons[current]); }
    else if (++tries > 100) clearInterval(wait);
  }, 150);
})();
