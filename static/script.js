// Funcionalidades adicionales para la página
document.addEventListener('DOMContentLoaded', function() {
  // Efecto de scroll suave para los enlaces de navegación
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const targetSection = document.querySelector(targetId);
      
      if (targetSection) {
        window.scrollTo({
          top: targetSection.offsetTop - 20,
          behavior: 'smooth'
        });
      } else {
        window.location.href = this.href;
      }
    });
  });
  
  // Efecto de carga progresiva para los elementos
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, observerOptions);
  
  // Observar elementos para animación de aparición
  document.querySelectorAll('.intro, .nav-link').forEach(el => {
    el.style.opacity = '0';
    el.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
    observer.observe(el);
  });
  
  // Solución alternativa para el logo si no carga
  const logo = document.querySelector('.logo img');
  if (logo) {
    logo.addEventListener('error', function() {
      this.src = 'https://placehold.co/120x60/00B0F0/white?text=DI+Logo';
      this.alt = 'Logo de placeholder';
    });
  }
});

// Añadir clase visible a los elementos cuando están en viewport
document.addEventListener('DOMContentLoaded', function() {
  const elements = document.querySelectorAll('.intro, .nav-link');
  
  elements.forEach(el => {
    el.classList.add('visible');
  });
});