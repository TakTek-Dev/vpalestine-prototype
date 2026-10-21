/* Inner-page behaviour: What's on filters, search over the edition's index, the send-us-a-screening form. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ---------- What's on: desk, city, expected ---------- */
  const cal = $('.cal');
  if (cal) {
    const rows = $$('.tour .row', cal), years = $$('.tour .year', cal);
    const chips = $$('.chip[data-desk]', cal), city = $('#city'), due = $('#due'), count = $('#count'), empty = $('#empty');
    let desk = 'all';
    const apply = () => {
      let n = 0;
      rows.forEach((r) => {
        const ok = (desk === 'all' || r.dataset.desk === desk) && (!city.value || r.dataset.city === city.value) && (due.checked || r.dataset.state !== 'due');
        r.hidden = !ok; if (ok) n++;
      });
      // a month heading prints only when one of its dates does
      years.forEach((y) => { let el = y.nextElementSibling, any = false; while (el && !el.classList.contains('year')) { if (!el.hidden) any = true; el = el.nextElementSibling; } y.hidden = !any; });
      count.textContent = n === 1 ? '1 date' : n + ' dates';
      empty.hidden = n > 0;
    };
    chips.forEach((c) => c.addEventListener('click', () => { desk = c.dataset.desk; chips.forEach((x) => x.setAttribute('aria-pressed', String(x === c))); apply(); }));
    city.addEventListener('change', apply); due.addEventListener('change', apply);
    apply();
  }

  /* ---------- search ---------- */
  const results = $('#results');
  if (results) {
    const q = $('#q'), count = $('#count'), none = $('#none');
    const chips = $$('.facets .chip');
    let desk = 'all', idx = [];
    const params = new URLSearchParams(location.search);
    q.value = params.get('q') || '';
    const mark = (text, terms) => {
      let out = esc(text);
      terms.forEach((t) => { if (t.length > 1) out = out.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<mark>$1</mark>'); });
      return out;
    };
    const snippet = (text, terms) => {
      const low = text.toLowerCase();
      const at = terms.map((t) => low.indexOf(t)).filter((i) => i >= 0).sort((a, b) => a - b)[0];
      if (at === undefined || at < 90) return text.length > 240 ? text.slice(0, 240).replace(/\s\S*$/, '') + '…' : text;
      const s = text.slice(Math.max(0, at - 80)).replace(/^\S*\s/, '');
      return '…' + (s.length > 220 ? s.slice(0, 220).replace(/\s\S*$/, '') + '…' : s);
    };
    const MON = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ');
    const render = () => {
      const terms = q.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      const hits = idx.filter((r) => { const hay = (r.title + ' ' + r.text + ' ' + r.tags).toLowerCase(); return terms.every((t) => hay.includes(t)); });
      const counts = { all: hits.length, film: hits.filter((r) => r.desk === 'film').length, music: hits.filter((r) => r.desk === 'music').length };
      chips.forEach((c) => { c.querySelector('span').textContent = counts[c.dataset.desk]; });
      const shown = hits.filter((r) => desk === 'all' || r.desk === desk);
      results.innerHTML = shown.map((r) => {
        const [y, m, d] = r.date.split('-').map(Number);
        const v = document.querySelector(`.facets .chip[data-desk="${r.desk}"] svg`);
        const th = r.img ? `<figure class="plate th ${r.desk === 'music' ? 'ink-music' : 'ink-film'}" data-fx="0.5" data-fy="0.4" data-lpi="30"><img src="assets/img/photo/${r.img}.webp" alt="" loading="lazy"></figure>` : '';
        return `<li class="res ${r.desk === 'music' ? 'ink-music' : 'ink-film'}${r.state === 'due' ? ' due' : ''}${th ? ' has-th' : ''}"><p class="dt"><b>${d}</b><small>${MON[m - 1]}${y !== 2026 ? ' ' + y : ''}</small></p>${th}`
          + `<div><h2 class="hed"><a href="${r.href}">${mark(r.title, terms)}</a></h2><p class="copy">${mark(snippet(r.text, terms), terms)}</p></div>${v ? v.outerHTML : ''}</li>`;
      }).join('');
      count.textContent = terms.length ? `${shown.length} ${shown.length === 1 ? 'story' : 'stories'} for “${q.value.trim()}”` : `All ${shown.length} stories, by date`;
      none.hidden = shown.length > 0;
      if (window.VP) results.querySelectorAll('.plate').forEach((f) => { const img = f.querySelector('img'); const go = () => VP.screen(f); if (img.complete && img.naturalWidth) go(); else img.addEventListener('load', go, { once: true }); });
      if (window.VP) document.querySelectorAll('.noresult .lines[data-fit]').forEach((b) => VP.fitLines(b));
      const url = new URL(location); if (q.value.trim()) url.searchParams.set('q', q.value.trim()); else url.searchParams.delete('q'); history.replaceState(null, '', url);
    };
    let t = 0;
    q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(render, 120); });
    $('.sfield').addEventListener('submit', (e) => { e.preventDefault(); render(); });
    chips.forEach((c) => c.addEventListener('click', () => { desk = c.dataset.desk; chips.forEach((x) => x.setAttribute('aria-pressed', String(x === c))); render(); }));
    fetch('assets/data/search.json').then((r) => r.json()).then((d) => { idx = d; render(); }).catch(() => { count.textContent = 'Search could not load its index.'; });
  }

  /* ---------- send us a screening ---------- */
  const send = $('#send-form');
  if (send) send.addEventListener('submit', (e) => {
    e.preventDefault();
    const note = $('.note', send);
    const bad = $$('input[required]', send).find((i) => !i.checkValidity());
    if (bad) { note.textContent = 'Some details are missing or look wrong: ' + (bad.closest('label').querySelector('.label').textContent).toLowerCase() + '.'; note.dataset.state = 'error'; bad.focus(); return; }
    note.textContent = 'Prototype: nothing was sent. On the live site this goes to the editors, who check the link before listing it.';
    note.dataset.state = 'sent';
  });
})();
