
// Rotador simple: alterna las frases cada 4s
(function rotator() {
  const items = document.querySelectorAll('#hero-rotator .rotator-item');
  if (!items.length) return;
  let i = 0;
  items.forEach((el, idx) => el.style.display = idx === 0 ? 'flex' : 'none');
  setInterval(() => {
    items[i].style.display = 'none';
    i = (i + 1) % items.length;
    items[i].style.display = 'flex';
  }, 4000);
})();

// Animación de métricas circulares
(function metrics() {
  const circles = document.querySelectorAll('.metric .fg');
  if (!circles.length) return;
  const R = 50; // radio SVG
  const C = 2 * Math.PI * R; // circunferencia
  circles.forEach(c => {
    const p = parseFloat(c.dataset.percent || '0'); // porcentaje
    c.style.strokeDasharray = `${C}`;
    c.style.strokeDashoffset = `${C}`; // inicia vacío
    requestAnimationFrame(() => {
      c.style.transition = 'stroke-dashoffset 1.2s ease';
      c.style.strokeDashoffset = `${C * (1 - p / 100)}`;
    });
  });
})();
