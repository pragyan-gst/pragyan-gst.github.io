(function () {
  "use strict";

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c];
    });
  }

  // Shared scoring used by both the Ctrl K overlay and the standalone
  // /search.html page, so the two surfaces never rank a query differently.
  // Title matches score higher than a hit anywhere else in the record.
  function rank(items, query, limit) {
    var terms = query.split(/\s+/);
    return items
      .map(function (x) {
        var haystack = (x.title + ' ' + x.description + ' ' + (x.tags || []).join(' ') + ' ' + (x.text || '')).toLowerCase();
        var score = terms.reduce(function (n, t) {
          return haystack.indexOf(t) > -1 ? n + (x.title.toLowerCase().indexOf(t) > -1 ? 4 : 1) : -99;
        }, 0);
        return { x: x, s: score };
      })
      .filter(function (z) { return z.s >= terms.length; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, limit || 18)
      .map(function (z) { return z.x; });
  }

  function renderResult(x) {
    return '<a class="search-result" href="' + esc(x.url) + '">' +
      '<span class="search-kind">' + esc(x.kind) + '</span>' +
      '<strong>' + esc(x.title) + '</strong>' +
      '<span>' + esc(x.description || '') + '</span></a>';
  }

  // Exposed so /search.html (and any other page) can reuse the exact same
  // ranking and escaping instead of keeping a second, drifting copy.
  window.PragyanSearch = { esc: esc, rank: rank, renderResult: renderResult };

  var overlay, input, results, indexPromise;

  function idx() {
    return indexPromise || (indexPromise = fetch('search-index.json', { cache: 'no-store' }).then(function (r) { return r.json(); }));
  }

  function openSearch() {
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'search-overlay';
      overlay.innerHTML = '<div class="search-backdrop" data-search-close></div>' +
        '<section class="search-dialog" role="dialog" aria-modal="true" aria-labelledby="search-title">' +
        '<div class="search-head"><div><span class="eyebrow dark">GST Pragyan search</span>' +
        '<h2 id="search-title">Find a provision, date, article or tool</h2></div>' +
        '<button class="icon-close" type="button" data-search-close aria-label="Close search">×</button></div>' +
        '<label class="search-input-wrap"><span class="sr-only">Search</span>' +
        '<input id="site-search-input" type="search" placeholder="Try Section 50, GSTR-3B, limitation or late fee"><span>Ctrl K</span></label>' +
        '<div class="search-status" id="site-search-status">Start typing to search the site.</div>' +
        '<div class="search-results" id="site-search-results"></div></section>';
      document.body.appendChild(overlay);
      input = overlay.querySelector('#site-search-input');
      results = overlay.querySelector('#site-search-results');
      input.addEventListener('input', search);
      overlay.addEventListener('click', function (e) {
        if (e.target.closest('[data-search-close]')) closeSearch();
      });
    }
    overlay.hidden = false;
    document.body.classList.add('search-open');
    setTimeout(function () { input.focus(); }, 10);
  }

  function closeSearch() {
    if (!overlay) return;
    overlay.hidden = true;
    document.body.classList.remove('search-open');
  }

  function search() {
    var q = input.value.trim().toLowerCase();
    var st = overlay.querySelector('#site-search-status');
    if (!q) { results.innerHTML = ''; st.textContent = 'Start typing to search the site.'; return; }
    idx().then(function (a) {
      var out = rank(a, q, 18);
      st.textContent = out.length ? out.length + ' result' + (out.length === 1 ? '' : 's') + ' found.' : 'No match found.';
      results.innerHTML = out.map(renderResult).join('');
    });
  }

  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-search-open]')) { e.preventDefault(); openSearch(); }
    if (e.target.closest('[data-print-table]')) {
      e.preventDefault();
      var b = e.target.closest('[data-print-table]');
      var box = b.parentNode.nextElementSibling;
      var w = window.open('', '_blank');
      if (w) {
        w.document.write('<html><head><title>GST Pragyan reference table</title><style>body{font-family:Arial;padding:25px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:6px;text-align:left}th{background:#0B2440;color:#fff}</style></head><body>' +
          box.innerHTML + '<p>Printed from GST Pragyan. Verify the applicable legal position before reliance.</p><script>window.onload=function(){window.print()}<\/script></body></html>');
        w.document.close();
      }
    }
    if (e.target.closest('[data-copy-work]')) {
      e.preventDefault();
      var el = document.getElementById(e.target.closest('[data-copy-work]').getAttribute('data-copy-work'));
      if (el && navigator.clipboard) navigator.clipboard.writeText(el.innerText);
    }
  });

  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
    if (e.key === 'Escape') closeSearch();
  });

  document.querySelectorAll('[data-table-filter]').forEach(function (inp) {
    inp.addEventListener('input', function () {
      var q = inp.value.toLowerCase();
      var box = inp.closest('.table-tools').nextElementSibling;
      box.querySelectorAll('tbody tr').forEach(function (tr) {
        tr.hidden = q && tr.innerText.toLowerCase().indexOf(q) === -1;
      });
    });
  });
})();
