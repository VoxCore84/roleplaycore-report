(function(){
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── Scroll progress bar ──
  var progressBar = document.querySelector('.scroll-progress');
  if (progressBar) {
    window.addEventListener('scroll', function() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var pct = h > 0 ? (window.scrollY / h) * 100 : 0;
      progressBar.style.width = pct + '%';
    }, { passive: true });
  }

  // ── Scroll reveal with stagger ──
  if (!rm) {
    var obs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) e.target.classList.add('visible'); });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(function(el) { obs.observe(el); });

    document.querySelectorAll('.pillars-grid, .cards-grid').forEach(function(grid) {
      var children = grid.children;
      for (var i = 0; i < children.length; i++) {
        children[i].classList.add('reveal', 'reveal-stagger');
        children[i].style.setProperty('--stagger', (i * 0.1) + 's');
        obs.observe(children[i]);
      }
    });
  } else {
    document.querySelectorAll('.reveal').forEach(function(el) { el.classList.add('visible'); });
  }

  // ── Count-up animation ──
  document.querySelectorAll('[data-countup]').forEach(function(el) {
    if (rm) return;
    var o = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting) { countUp(el, el.getAttribute('data-countup')); o.unobserve(el); }
      });
    }, { threshold: 0.5 });
    o.observe(el);
  });

  function countUp(el, target) {
    var m = target.match(/([~]?)([\d,.]+)(.*)/);
    if (!m) { el.textContent = target; return; }
    var pfx = m[1], num = parseFloat(m[2].replace(/,/g, '')), sfx = m[3];
    var hasDot = m[2].indexOf('.') !== -1, start = performance.now();
    function tick(now) {
      var p = Math.min((now - start) / 1400, 1);
      var e = 1 - Math.pow(1 - p, 3);
      var c = num * e;
      var d = hasDot ? c.toFixed(1) : (num >= 1000 ? Math.floor(c).toLocaleString() : Math.floor(c).toString());
      el.textContent = pfx + d + sfx;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // ── Hero particles ──
  (function initParticles() {
    if (rm) return;
    var container = document.querySelector('.hero-particles');
    if (!container) return;
    for (var i = 0; i < 18; i++) {
      var p = document.createElement('div');
      p.className = 'hero-particle' + (Math.random() > 0.7 ? ' gold' : '');
      p.style.setProperty('--size', (2 + Math.random() * 4) + 'px');
      p.style.setProperty('--duration', (6 + Math.random() * 8) + 's');
      p.style.setProperty('--delay', (Math.random() * 6) + 's');
      p.style.setProperty('--drift-y', (-60 - Math.random() * 120) + 'px');
      p.style.setProperty('--drift-x', (-40 + Math.random() * 80) + 'px');
      p.style.left = (5 + Math.random() * 90) + '%';
      p.style.top = (10 + Math.random() * 80) + '%';
      container.appendChild(p);
    }
  })();

  // ── Pipeline SVG scroll activation ──
  if (!rm) {
    var pipelineSvg = document.querySelector('.pipeline-svg');
    if (pipelineSvg) {
      var pipeObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) {
          if (e.isIntersecting) { pipelineSvg.classList.add('active'); pipeObs.unobserve(pipelineSvg); }
        });
      }, { threshold: 0.3 });
      pipeObs.observe(pipelineSvg);
    }
  }

  // ── Tool Explorer ──
  (function initToolExplorer() {
    var explorer = document.querySelector('.tool-explorer');
    if (!explorer) return;
    var search = explorer.querySelector('.tool-search');
    var chips = explorer.querySelectorAll('.tool-chip');
    var cards = explorer.querySelectorAll('.tool-card');
    var countEl = explorer.querySelector('.tool-count');
    var activeCategory = 'all';

    function filterTools() {
      var query = search ? search.value.toLowerCase() : '';
      var visible = 0;
      cards.forEach(function(card) {
        var name = card.getAttribute('data-name') || '';
        var cat = card.getAttribute('data-cat') || '';
        var desc = card.getAttribute('data-desc') || '';
        var matchCat = activeCategory === 'all' || cat === activeCategory;
        var matchSearch = !query || name.indexOf(query) !== -1 || desc.indexOf(query) !== -1;
        if (matchCat && matchSearch) { card.classList.remove('hidden'); visible++; }
        else { card.classList.add('hidden'); }
      });
      if (countEl) countEl.textContent = visible + ' of ' + cards.length + ' tools';
    }

    chips.forEach(function(chip) {
      chip.addEventListener('click', function() {
        chips.forEach(function(c) { c.classList.remove('active'); });
        chip.classList.add('active');
        activeCategory = chip.getAttribute('data-cat');
        filterTools();
      });
    });
    if (search) search.addEventListener('input', filterTools);
    filterTools();
  })();

  // ── Achievement Toasts ──
  (function initToasts() {
    if (rm) return;
    var toasts = [
      { selector: '[data-countup="~1,004,000"]', text: '1M Rows Imported', icon: '\u2728' },
      { selector: '[data-countup="97.8%"]', text: '97.8% Redundancy Eliminated', icon: '\u26A1' },
      { selector: '[data-countup="~10.6M"]', text: '10.6M Dead Rows Purged', icon: '\uD83D\uDD25' },
      { selector: '[data-countup="75+"]', text: '75+ Tools Built', icon: '\uD83D\uDEE0\uFE0F' }
    ];
    var shown = {};
    toasts.forEach(function(t) {
      var el = document.querySelector(t.selector);
      if (!el) return;
      var toastObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) {
          if (e.isIntersecting && !shown[t.text]) {
            shown[t.text] = true;
            showToast(t.icon, t.text);
            toastObs.unobserve(el);
          }
        });
      }, { threshold: 0.8 });
      toastObs.observe(el);
    });

    function showToast(icon, text) {
      var toast = document.createElement('div');
      toast.className = 'achievement-toast';
      toast.innerHTML = '<span class="toast-icon">' + icon + '</span><div><div class="toast-text">' + text + '</div></div>';
      document.body.appendChild(toast);
      requestAnimationFrame(function() {
        requestAnimationFrame(function() { toast.classList.add('show'); });
      });
      setTimeout(function() {
        toast.classList.remove('show');
        setTimeout(function() { toast.remove(); }, 500);
      }, 3000);
    }
  })();

  // ── Mobile nav ──
  var menuBtn = document.querySelector('.nav-menu-btn');
  var mobileNav = document.querySelector('.mobile-nav');
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', function() {
      mobileNav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', mobileNav.classList.contains('open'));
    });
  }

  // ── Sidebar TOC ──
  var sidebar = document.querySelector('.sidebar');
  if (sidebar) {
    var sections = sidebar.querySelectorAll('.toc-section');
    var isReportSidebar = sections.length > 0;
    sections.forEach(function(section) {
      var toggle = section.querySelector('.toc-toggle');
      if (toggle) {
        toggle.addEventListener('click', function(e) {
          e.preventDefault(); e.stopPropagation();
          section.classList.toggle('expanded');
        });
      }
    });

    var allLinks = sidebar.querySelectorAll('a[href^="#"]');
    var headings = [];
    allLinks.forEach(function(a) {
      var id = a.getAttribute('href');
      if (id && id.length > 1) {
        var el = document.getElementById(id.slice(1));
        if (el) headings.push({ el: el, link: a });
      }
    });
    if (headings.length > 0) {
      var tocObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            allLinks.forEach(function(l) { l.classList.remove('active'); });
            headings.forEach(function(h) {
              if (h.el === entry.target) {
                h.link.classList.add('active');
                if (isReportSidebar) {
                  var ps = h.link.closest('.toc-section');
                  if (ps) ps.classList.add('expanded');
                }
              }
            });
          }
        });
      }, { rootMargin: '-80px 0px -60% 0px' });
      headings.forEach(function(h) { tocObs.observe(h.el); });
    }
  }

  // ── Sidebar toggle (tablet/mobile) ──
  var st = document.querySelector('.sidebar-toggle');
  var sb = document.querySelector('.sidebar');
  if (st && sb) { st.addEventListener('click', function() { sb.classList.toggle('mobile-open'); }); }

  // ── Back to top button ──
  var btt = document.querySelector('.back-to-top');
  if (btt) {
    window.addEventListener('scroll', function() {
      btt.classList.toggle('visible', window.scrollY > 600);
    }, { passive: true });
    btt.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: rm ? 'auto' : 'smooth' });
    });
  }

  // ── Konami Code Easter Egg ──
  var konamiSeq = [38,38,40,40,37,39,37,39,66,65], konamiPos = 0;
  document.addEventListener('keydown', function(e) {
    if (e.keyCode === konamiSeq[konamiPos]) {
      konamiPos++;
      if (konamiPos === konamiSeq.length) {
        konamiPos = 0;
        var flash = document.createElement('div');
        flash.className = 'konami-flash';
        document.body.appendChild(flash);
        setTimeout(function() { flash.remove(); }, 1300);
      }
    } else { konamiPos = 0; }
  });

  // ═══════════════════════════════════════════════════════════════════════════
  //  NEW INTERACTIVE FEATURES
  // ═══════════════════════════════════════════════════════════════════════════

  // ── 3D Card Tilt ──
  if (!rm) {
    document.querySelectorAll('.pillar-card, .card, .tool-card, .timeline-card').forEach(function(card) {
      card.addEventListener('mousemove', function(e) {
        var rect = card.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = 'perspective(800px) rotateY(' + (x * 5) + 'deg) rotateX(' + (-y * 5) + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', function() {
        card.style.transform = '';
      });
    });
  }

  // ── Command Palette (Ctrl+K or /) ──
  (function initCommandPalette() {
    var overlay = document.querySelector('.cmd-overlay');
    if (!overlay) return;
    var input = overlay.querySelector('.cmd-input');
    var resultsEl = overlay.querySelector('.cmd-results');
    var activeIdx = -1;
    var searchIndex = [];
    try {
      var indexEl = document.getElementById('search-index');
      if (indexEl) searchIndex = JSON.parse(indexEl.textContent);
    } catch(e) {}

    function openPalette() {
      overlay.classList.add('open');
      input.value = '';
      input.focus();
      renderResults('');
      activeIdx = -1;
    }
    function closePalette() {
      overlay.classList.remove('open');
      activeIdx = -1;
    }

    function renderResults(query) {
      query = query.toLowerCase().trim();
      var matches = searchIndex;
      if (query) {
        matches = searchIndex.filter(function(item) {
          return item.t.toLowerCase().indexOf(query) !== -1 ||
                 (item.s && item.s.toLowerCase().indexOf(query) !== -1);
        });
      }
      matches = matches.slice(0, 15);
      resultsEl.innerHTML = matches.map(function(item, i) {
        return '<a class="cmd-result' + (i === 0 ? ' active' : '') + '" href="' + item.u + '">' +
          '<span class="cmd-result-title">' + item.t + '</span>' +
          '<span class="cmd-result-page">' + (item.p || '') + '</span></a>';
      }).join('');
      activeIdx = matches.length > 0 ? 0 : -1;
    }

    function navigate(idx) {
      var items = resultsEl.querySelectorAll('.cmd-result');
      items.forEach(function(el) { el.classList.remove('active'); });
      if (idx >= 0 && idx < items.length) {
        items[idx].classList.add('active');
        items[idx].scrollIntoView({ block: 'nearest' });
      }
      activeIdx = idx;
    }

    document.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        overlay.classList.contains('open') ? closePalette() : openPalette();
      }
      if (e.key === '/' && !overlay.classList.contains('open') &&
          document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault(); openPalette();
      }
      if (e.key === 'Escape' && overlay.classList.contains('open')) { closePalette(); }
    });

    input.addEventListener('keydown', function(e) {
      var items = resultsEl.querySelectorAll('.cmd-result');
      if (e.key === 'ArrowDown') { e.preventDefault(); navigate(Math.min(activeIdx + 1, items.length - 1)); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); navigate(Math.max(activeIdx - 1, 0)); }
      else if (e.key === 'Enter') {
        e.preventDefault();
        var active = resultsEl.querySelector('.cmd-result.active');
        if (active) window.location.href = active.href;
      }
    });
    input.addEventListener('input', function() { renderResults(input.value); });
    overlay.addEventListener('click', function(e) { if (e.target === overlay) closePalette(); });
  })();

  // ── Copy Buttons on Code Blocks ──
  document.querySelectorAll('pre').forEach(function(pre) {
    var wrap = document.createElement('div');
    wrap.className = 'code-wrap';
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    var btn = document.createElement('button');
    btn.className = 'code-copy';
    btn.textContent = 'Copy';
    btn.addEventListener('click', function() {
      var code = pre.querySelector('code');
      navigator.clipboard.writeText(code ? code.textContent : pre.textContent).then(function() {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function() { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
      });
    });
    wrap.appendChild(btn);
  });

  // ── Cursor Trail ──
  if (!rm && window.innerWidth > 768) {
    var trail = [], trailCount = 5;
    for (var ti = 0; ti < trailCount; ti++) {
      var dot = document.createElement('div');
      dot.className = 'cursor-dot';
      document.body.appendChild(dot);
      trail.push({ el: dot, x: 0, y: 0 });
    }
    var mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', function(e) { mouseX = e.clientX; mouseY = e.clientY; });
    function animateTrail() {
      var px = mouseX, py = mouseY;
      trail.forEach(function(d, i) {
        d.x += (px - d.x) * (0.28 - i * 0.04);
        d.y += (py - d.y) * (0.28 - i * 0.04);
        d.el.style.left = d.x + 'px';
        d.el.style.top = d.y + 'px';
        d.el.style.opacity = (1 - i / trailCount) * 0.2;
        d.el.style.width = d.el.style.height = (5 - i * 0.7) + 'px';
        px = d.x; py = d.y;
      });
      requestAnimationFrame(animateTrail);
    }
    animateTrail();
  }

  // ── Interactive Timeline ──
  document.querySelectorAll('.timeline-card-header').forEach(function(header) {
    header.addEventListener('click', function() {
      header.closest('.timeline-card').classList.toggle('expanded');
    });
  });

  // ── Expanding Tables ──
  document.querySelectorAll('.data-table').forEach(function(table) {
    var rows = table.querySelectorAll('tbody tr');
    if (rows.length <= 8) return;
    var wrap = table.closest('.table-wrap');
    if (!wrap) return;
    wrap.classList.add('table-expandable', 'collapsed');
    var btn = document.createElement('button');
    btn.className = 'table-expand-btn';
    btn.textContent = 'Show all ' + rows.length + ' rows';
    btn.addEventListener('click', function() {
      wrap.classList.toggle('collapsed');
      btn.textContent = wrap.classList.contains('collapsed') ? 'Show all ' + rows.length + ' rows' : 'Show fewer';
    });
    wrap.appendChild(btn);
  });

  // ── Progress Ring Animation ──
  if (!rm) {
    document.querySelectorAll('.progress-ring-fill').forEach(function(ring) {
      var pct = parseFloat(ring.getAttribute('data-pct') || 0);
      var offset = 226.2 * (1 - pct / 100);
      var ringObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) {
          if (e.isIntersecting) { ring.style.strokeDashoffset = offset; ringObs.unobserve(ring); }
        });
      }, { threshold: 0.5 });
      ringObs.observe(ring);
    });
  }

  // ── Typewriter Effect on Page Titles ──
  if (!rm) {
    var pageH1 = document.querySelector('.page-header h1');
    if (pageH1 && !pageH1.classList.contains('typed')) {
      var fullText = pageH1.textContent;
      pageH1.classList.add('typed');
      pageH1.textContent = '';
      pageH1.style.borderRight = '2px solid var(--arcane)';
      var ci = 0;
      function typeChar() {
        if (ci < fullText.length) {
          pageH1.textContent += fullText[ci];
          ci++;
          setTimeout(typeChar, 25 + Math.random() * 35);
        } else {
          setTimeout(function() {
            pageH1.style.borderRight = '2px solid transparent';
          }, 600);
        }
      }
      setTimeout(typeChar, 300);
    }
  }

  // ── Smooth Page Transitions ──
  document.querySelectorAll('a[href$=".html"]').forEach(function(link) {
    if (link.target === '_blank') return;
    if (link.closest('.cmd-palette')) return;
    try { if (link.hostname && link.hostname !== window.location.hostname) return; } catch(e) { return; }
    link.addEventListener('click', function(e) {
      if (e.ctrlKey || e.metaKey || e.shiftKey) return;
      e.preventDefault();
      var href = link.href;
      document.body.classList.add('page-exit');
      setTimeout(function() { window.location.href = href; }, 180);
    });
  });

  // ── Floating Runes (subtle background) ──
  if (!rm && window.innerWidth > 1024) {
    var runes = ['\u16A0','\u16A2','\u16A6','\u16B1','\u16B7','\u16C1','\u16C7','\u16D2'];
    for (var ri = 0; ri < 5; ri++) {
      var rune = document.createElement('div');
      rune.className = 'rune';
      rune.textContent = runes[Math.floor(Math.random() * runes.length)];
      rune.style.left = (8 + Math.random() * 84) + '%';
      rune.style.top = (5 + Math.random() * 90) + '%';
      rune.style.animationDelay = (Math.random() * 12) + 's';
      rune.style.animationDuration = (18 + Math.random() * 14) + 's';
      rune.style.fontSize = (22 + Math.random() * 14) + 'px';
      document.body.appendChild(rune);
    }
  }

})();
