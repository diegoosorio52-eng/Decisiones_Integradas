<script>
/* Script simple que genera gotas aleatorias y ripples dentro de .drops */
(function(){
  const dropsContainer = document.querySelector('.drops');
  if(!dropsContainer) return;

  // función que crea una gota + ripple en posición x aleatoria
  function createDrop() {
    const width = dropsContainer.clientWidth;
    const height = dropsContainer.clientHeight;
    // posición aleatoria horizontal (5% - 95%) dentro del contenedor
    const x = Math.random() * (width * 0.9) + (width * 0.05);
    const y = Math.random() * (height * 0.55) + (height * 0.35); // altura donde cae (parte media-inferior)

    // Crear gota
    const drop = document.createElement('div');
    drop.className = 'drop';
    drop.style.left = x + 'px';
    drop.style.top = (y - 60) + 'px'; // empieza arriba para la animación
    // tamaño y duración levemente aleatorios
    const scale = 0.7 + Math.random() * 0.9;
    drop.style.width = (8 * scale) + 'px';
    drop.style.height = (8 * scale) + 'px';
    dropsContainer.appendChild(drop);

    // Crear ripple (onda) en el punto de impacto después de pequeña demora
    setTimeout(() => {
      const ripple = document.createElement('div');
      ripple.className = 'ripple';
      ripple.style.left = x + 'px';
      ripple.style.top = (y) + 'px';
      dropsContainer.appendChild(ripple);

      // eliminar ripple tras animación
      setTimeout(() => {
        ripple.remove();
      }, 900);
    }, 820);

    // eliminar gota tras animación
    setTimeout(() => {
      drop.remove();
    }, 1400);
  }

  // generar gotas a intervalos aleatorios (no muchas para no saturar)
  function scheduleNext() {
    createDrop();
    const next = 700 + Math.random() * 1800; // entre 0.7s y 2.5s
    setTimeout(scheduleNext, next);
  }

  // arrancar con un ligero retardo
  setTimeout(scheduleNext, 600);
})();
</script>
