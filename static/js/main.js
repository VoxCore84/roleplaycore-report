(function(){
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── Scroll reveal ──
  if (!rm) {
    var obs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) e.target.classList.add('visible'); });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(function(el) { obs.observe(el); });
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

    // Toggle expand/collapse on triangle click (report sidebar)
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

    // Scroll-spy: collect all local anchor links
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
            // Clear active on local links only
            allLinks.forEach(function(l) { l.classList.remove('active'); });

            headings.forEach(function(h) {
              if (h.el === entry.target) {
                h.link.classList.add('active');

                // Auto-expand the parent toc-section if in report sidebar
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
