/* Identity book demos: the press (drag music over film), the measure, the screen ruling, the pull. */
(() => {
  const ready = (fn) => (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => setTimeout(fn, 60));

  /* the press: the music screen moves; on black stock the overprint is printed as its own screen */
  const press = document.getElementById('press');
  if (press) {
    const music = press.querySelector('.music');
    const film = press.querySelector('.film');
    const ov = document.createElement('i'); ov.className = 'ov'; press.appendChild(ov);
    const place = (pct) => {
      pct = Math.max(0, Math.min(54, pct));
      music.style.setProperty('--x', pct + '%');
      music.setAttribute('aria-valuenow', Math.round(pct / 54 * 100));
      const W = press.clientWidth, fr = film.offsetLeft + film.offsetWidth, ml = pct / 100 * W;
      ov.style.left = ml + 'px'; ov.style.width = Math.max(0, fr - ml) + 'px';
    };
    let drag = null;
    music.addEventListener('pointerdown', (e) => { drag = { x: e.clientX, start: parseFloat(getComputedStyle(music).left) }; music.setPointerCapture(e.pointerId); });
    music.addEventListener('pointermove', (e) => { if (!drag) return; place((drag.start + e.clientX - drag.x) / press.clientWidth * 100); });
    music.addEventListener('pointerup', () => { drag = null; });
    music.addEventListener('keydown', (e) => {
      const now = parseFloat(music.style.getPropertyValue('--x')) || 46;
      if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') { place(now - 3); e.preventDefault(); }
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') { place(now + 3); e.preventDefault(); }
    });
    place(46);
    addEventListener('resize', () => place(parseFloat(music.style.getPropertyValue('--x')) || 46));
  }

  /* the measure: narrow the sheet and every line is re-set to it */
  const measure = document.getElementById('measure'), box = document.getElementById('measure-box');
  if (measure && box) {
    const out = document.getElementById('measure-out');
    const set = () => { box.style.width = measure.value + '%'; out.textContent = measure.value + '%'; };
    measure.addEventListener('input', () => { set(); requestAnimationFrame(() => window.VP && VP.fitLines(box.querySelector('.lines'))); });
    box.addEventListener('transitionend', () => window.VP && VP.fitLines(box.querySelector('.lines')));
    set();
  }

  /* the screen ruling */
  const ruling = document.getElementById('ruling');
  if (ruling) {
    const out = document.getElementById('ruling-out');
    const plates = document.querySelectorAll('.ht-plates .plate');
    ruling.addEventListener('input', () => {
      out.textContent = ruling.value;
      plates.forEach((p) => { p.dataset.lpi = ruling.value; if (window.VP) VP.screen(p); });
    });
  }

  /* the pull, again */
  const demo = document.getElementById('pull-demo'), replay = document.getElementById('replay');
  const run = () => { if (!demo) return; demo.classList.remove('run'); void demo.offsetWidth; demo.classList.add('run'); };
  if (replay) replay.addEventListener('click', run);
  if (demo && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { run(); io.disconnect(); } }), { threshold: 0.6 });
    io.observe(demo);
  }
  ready(() => {});
})();
