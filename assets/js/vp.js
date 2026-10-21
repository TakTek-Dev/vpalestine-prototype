/* VPalestine — the press.
   stock: white or black paper, remembered per reader
   pull: the first visit in a session prints the front sheet screen by screen (head script decides)
   fitLines: every poster line is set to its sheet's measure through Anybody's width axis
   screen: photographs are printed as halftone dots, sized from the photo, at 45 degrees */
(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const css = (el, p) => getComputedStyle(el).getPropertyValue(p).trim();

  /* ---------- stock ---------- */
  const toggle = document.querySelector('.stock');
  const setStock = (black) => {
    if (black) root.dataset.stock = 'black'; else delete root.dataset.stock;
    toggle && toggle.setAttribute('aria-pressed', String(black));
    try { localStorage.setItem('vp-stock', black ? 'black' : 'white'); } catch (e) {}
    reprint();
  };
  if (toggle) {
    toggle.setAttribute('aria-pressed', String(root.dataset.stock === 'black'));
    toggle.addEventListener('click', () => {
      const black = root.dataset.stock !== 'black';
      if (document.startViewTransition && !reduce) document.startViewTransition(() => setStock(black));
      else setStock(black);
    });
  }

  /* ---------- the pull ---------- */
  if (root.classList.contains('pulling')) {
    try { sessionStorage.setItem('vp-pulled', '1'); } catch (e) {}
    const lead = document.querySelector('.one');
    if (lead) root.style.setProperty('--pull-w', lead.getBoundingClientRect().width + 'px');
    const done = () => { root.classList.remove('pulling'); ['keydown', 'pointerdown', 'wheel', 'touchstart'].forEach((t) => removeEventListener(t, done)); };
    ['keydown', 'pointerdown', 'wheel', 'touchstart'].forEach((t) => addEventListener(t, done, { passive: true }));
    setTimeout(done, 1900);
  }

  /* ---------- set to measure ---------- */
  const MIN = 58, MAX = 150, GROW = 1.7;
  function fitLines(block) {
    const W = block.clientWidth;
    if (!W) return;
    block.classList.add('fitted');
    block.querySelectorAll('.ln').forEach((ln) => {
      ln.style.fontStretch = ''; ln.style.fontSize = '';
      const base = parseFloat(getComputedStyle(ln).fontSize);
      const at = (s) => { ln.style.fontStretch = s + '%'; return ln.getBoundingClientRect().width; };
      if (at(MIN) > W) { ln.style.fontSize = (base * W / at(MIN) * 0.995) + 'px'; return; }
      const wide = at(MAX);
      if (wide < W) { ln.style.fontSize = (base * Math.min(GROW, W / wide) * 0.995) + 'px'; at(MAX); return; }
      let lo = MIN, hi = MAX;
      for (let i = 0; i < 9; i++) { const mid = (lo + hi) / 2; if (at(mid) > W) hi = mid; else lo = mid; }
      ln.style.fontStretch = lo.toFixed(2) + '%';
    });
  }
  const blocks = [...document.querySelectorAll('.lines[data-fit]')];
  const fitAll = () => blocks.forEach(fitLines);

  /* ---------- halftone screens ---------- */
  const plates = [...document.querySelectorAll('.plate')];
  const printed = new Set();
  function screen(fig, k = 1) {
    const img = fig.querySelector('img');
    if (!img || !img.naturalWidth) return;
    let cv = fig.querySelector('canvas');
    if (!cv) { cv = document.createElement('canvas'); cv.setAttribute('aria-hidden', 'true'); fig.appendChild(cv); }
    const w = fig.clientWidth, h = fig.clientHeight;
    if (!w || !h) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const W = Math.round(w * dpr), H = Math.round(h * dpr);
    if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; }
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, W, H);
    // crop like object-fit: cover around the focal point
    const iw = img.naturalWidth, ih = img.naturalHeight;
    const zoom = +fig.dataset.zoom || 1;
    const sc = Math.max(w / iw, h / ih) * zoom;
    const sw = w / sc, sh = h / sc;
    const sx = Math.min(Math.max((+fig.dataset.fx || 0.5) * iw - sw / 2, 0), iw - sw);
    const sy = Math.min(Math.max((+fig.dataset.fy || 0.5) * ih - sh / 2, 0), ih - sh);
    // screen ruling: coarser on big sheets, never under 3.2 css px
    // small plates (thumbnails) screen finer so the subject survives; big sheets keep the coarse poster screen
    const floor = w < 160 ? 1.9 : 3.2;
    const cell = Math.max(floor, Math.min(w / (+fig.dataset.lpi || 118), 8)) * dpr;
    const gw = Math.ceil(W / cell) * 2, gh = Math.ceil(H / cell) * 2;
    const off = document.createElement('canvas'); off.width = gw; off.height = gh;
    const octx = off.getContext('2d', { willReadFrequently: true });
    octx.drawImage(img, sx, sy, sw, sh, 0, 0, gw, gh);
    const px = octx.getImageData(0, 0, gw, gh).data;
    // on black stock the key-only plate is the white underbase: dots carry the light, not the dark
    const gamma = +fig.dataset.gamma || 1;
    const keyPlate = fig.classList.contains('key');
    const night = root.dataset.stock === 'black';
    const light = keyPlate && night;
    ctx.fillStyle = keyPlate ? css(fig, '--key') : css(fig, '--dot') || '#16131A';
    const a = Math.PI / 4, ca = Math.cos(a), sa = Math.sin(a);
    const n = Math.ceil(Math.hypot(W, H) / cell / 2) + 2;
    const cx = W / 2, cy = H / 2, rmax = cell * 0.52 * k;
    ctx.beginPath();
    for (let i = -n; i <= n; i++) {
      for (let j = -n; j <= n; j++) {
        const u = i * cell, v = j * cell;
        const x = cx + u * ca - v * sa, y = cy + u * sa + v * ca;
        if (x < -cell || y < -cell || x > W + cell || y > H + cell) continue;
        const gx = Math.min(gw - 1, Math.max(0, (x / W * gw) | 0)), gy = Math.min(gh - 1, Math.max(0, (y / H * gh) | 0));
        const o = (gy * gw + gx) * 4;
        const L = (px[o] * 0.299 + px[o + 1] * 0.587 + px[o + 2] * 0.114) / 255;
        // tone curve: highlights drop to bare ink, shadows stop short of solid so the ink always shows between dots
        const raw = Math.pow(light ? L : 1 - L, gamma);
        const q = Math.min(1, Math.max(0, (raw - 0.1) / 0.84));
        const t = q * q * (3 - 2 * q);
        const r = rmax * Math.sqrt(t);
        if (r < 0.45 * dpr) continue;
        ctx.moveTo(x + r, y); ctx.arc(x, y, r, 0, Math.PI * 2);
      }
    }
    ctx.fill();
    fig.classList.add('screened');
    fig.dataset.w = w;
  }
  function develop(fig, delay) {
    // the lead's key plate prints during the pull: dots grow from bare ink to full coverage
    const t0 = performance.now() + delay, dur = 650;
    const step = (now) => {
      const p = Math.min(1, Math.max(0, (now - t0) / dur));
      screen(fig, 1 - Math.pow(1 - p, 3));
      if (p < 1 && root.classList.contains('pulling')) requestAnimationFrame(step); else screen(fig, 1);
    };
    requestAnimationFrame(step);
  }
  const whenLoaded = (img) => (img.complete && img.naturalWidth ? Promise.resolve() : new Promise((r) => { img.addEventListener('load', r, { once: true }); img.addEventListener('error', r, { once: true }); }));
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      const fig = e.target, img = fig.querySelector('img');
      if (img.loading === 'lazy') img.loading = 'eager';
      whenLoaded(img).then(() => {
        printed.add(fig);
        if (root.classList.contains('pulling') && fig.closest('.tonight')) develop(fig, fig.closest('.sleeve') ? 1150 : 1050);
        else screen(fig);
      });
    });
  }, { rootMargin: '600px 0px' });
  plates.forEach((p) => io.observe(p));
  function reprint() { printed.forEach((f) => screen(f)); }

  /* ---------- resizing re-sets lines and re-screens plates ---------- */
  let lastW = innerWidth, raf = 0;
  const ro = new ResizeObserver(() => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(() => {
      if (Math.abs(innerWidth - lastW) < 1 && blocks.every((b) => b.dataset.w == b.clientWidth)) return;
      lastW = innerWidth;
      blocks.forEach((b) => { if (b.dataset.w != b.clientWidth) { fitLines(b); b.dataset.w = b.clientWidth; } });
      printed.forEach((f) => { if (Math.abs((+f.dataset.w || 0) - f.clientWidth) > 1) screen(f); });
    });
  });
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => {
    fitAll();
    blocks.forEach((b) => { b.dataset.w = b.clientWidth; ro.observe(b); });
    reprint();
  });

  // the identity book drives the same press from its demos
  window.VP = { fitLines, screen, reprint, printed };

  /* ---------- the Thursday bill (no list behind it yet) ---------- */
  const form = document.querySelector('.signup form');
  if (form) form.addEventListener('submit', (e) => {
    e.preventDefault();
    const note = form.querySelector('.note');
    const input = form.querySelector('input');
    if (!input.value || !input.checkValidity()) { note.textContent = 'That address looks incomplete. Check it and try again.'; note.dataset.state = 'error'; input.focus(); return; }
    note.textContent = 'Prototype: there is no mailing list yet, so nothing was sent or stored.';
    note.dataset.state = 'sent';
  });
})();
