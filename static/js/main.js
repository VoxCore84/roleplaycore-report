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

    // Apply stagger delays to grid children
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
    var count = 18;
    for (var i = 0; i < count; i++) {
      var p = document.createElement('div');
      p.className = 'hero-particle' + (Math.random() > 0.7 ? ' gold' : '');
      var size = 2 + Math.random() * 4;
      p.style.setProperty('--size', size + 'px');
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
          if (e.isIntersecting) {
            pipelineSvg.classList.add('active');
            pipeObs.unobserve(pipelineSvg);
          }
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
        if (matchCat && matchSearch) {
          card.classList.remove('hidden');
          visible++;
        } else {
          card.classList.add('hidden');
        }
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
      { selector: '[data-countup="65+"]', text: '65+ Tools Built', icon: '\uD83D\uDEE0\uFE0F' },
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
  var btn = document.querySelector('.nav-menu-btn');
  var mn = document.querySelector('.mobile-nav');
  if (btn && mn) {
    btn.addEventListener('click', function() {
      mn.classList.toggle('open');
      btn.setAttribute('aria-expanded', mn.classList.contains('open'));
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
          e.preventDefault();
          e.stopPropagation();
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
                  var parentSection = h.link.closest('.toc-section');
                  if (parentSection) parentSection.classList.add('expanded');
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
  if (st && sb) {
    st.addEventListener('click', function() {
      sb.classList.toggle('mobile-open');
    });
  }

  // ── Back to top button ──
  var btt = document.querySelector('.back-to-top');
  if (btt) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 600) {
        btt.classList.add('visible');
      } else {
        btt.classList.remove('visible');
      }
    }, { passive: true });
    btt.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: rm ? 'auto' : 'smooth' });
    });
  }

  // ── Konami Code Easter Egg ──
  var konamiSeq = [38,38,40,40,37,39,37,39,66,65];
  var konamiPos = 0;
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
    } else {
      konamiPos = 0;
    }
  });
})();
