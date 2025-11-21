// Crear partículas de energía
function createEnergyParticles() {
    const container = document.getElementById('energyParticles');
    const count = 20;

    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.classList.add('energy-particle');

        const size = Math.random() * 20 + 5;
        const left = Math.random() * 100;
        const delay = Math.random() * 8;
        const duration = Math.random() * 10 + 5;

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${left}%`;
        particle.style.animationDelay = `${delay}s`;
        particle.style.animationDuration = `${duration}s`;

        // Color aleatorio de partícula
        const colors = ['var(--neon-blue)', 'var(--neon-purple)', 'var(--neon-green)', 'var(--neon-pink)'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];

        container.appendChild(particle);
    }
}

// Crear partículas alrededor del logo
function createLogoParticles() {
    const container = document.getElementById('logoParticles');
    const count = 12;

    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');

        const angle = (i / count) * 360;
        const distance = Math.random() * 30 + 10;

        const tx = Math.cos(angle * Math.PI / 180) * distance;
        const ty = Math.sin(angle * Math.PI / 180) * distance;

        particle.style.setProperty('--tx', `${tx}px`);
        particle.style.setProperty('--ty', `${ty}px`);

        particle.style.left = '50%';
        particle.style.top = '50%';
        particle.style.animationDelay = `${Math.random() * 4}s`;

        container.appendChild(particle);
    }
}

// Crear burbujas flotantes
function createBubbles() {
    const container = document.getElementById('bubbles');
    const count = 15;

    for (let i = 0; i < count; i++) {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');

        const size = Math.random() * 60 + 20;
        const left = Math.random() * 100;
        const delay = Math.random() * 15;
        const duration = Math.random() * 20 + 10;

        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        bubble.style.left = `${left}%`;
        bubble.style.animationDelay = `${delay}s`;
        bubble.style.animationDuration = `${duration}s`;

        container.appendChild(bubble);
    }
}

// Animación de aparición al hacer scroll
function checkScroll() {
    const elements = document.querySelectorAll('.ff-card, .training-block, .bim-block');

    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;

        if (elementTop < windowHeight - 100) {
            element.classList.add('visible');
        }
    });
}

// Menú hamburguesa para móviles
function setupMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const cyberLinks = document.getElementById('cyberLinks');

    menuToggle.addEventListener('click', function () {
        this.classList.toggle('active');
        cyberLinks.classList.toggle('active');
    });

    // Cerrar menú al seleccionar un enlace
    const links = cyberLinks.querySelectorAll('.cyber-link');
    links.forEach(link => {
        link.addEventListener('click', function () {
            menuToggle.classList.remove('active');
            cyberLinks.classList.remove('active');
        });
    });
}

// Inicialización
document.addEventListener('DOMContentLoaded', function () {
    createEnergyParticles();
    createBubbles();
    createLogoParticles();
    checkScroll();
    setupMobileMenu();

    window.addEventListener('scroll', checkScroll);
});


fetch('header.html')
  .then(r => r.text())
  .then(html => {
    document.getElementById('header-container').innerHTML = html;
    initHeaderScripts(); // Llamas aquí a tus funciones
  });

function initHeaderScripts() {
    createEnergyParticles();
    createBubbles();
    createLogoParticles();
    checkScroll();
    setupMobileMenu();
    window.addEventListener('scroll', checkScroll);
}


const sections = document.querySelectorAll('.page');
const navItems = document.querySelectorAll('.pagination li');

window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.clientHeight;
    if (pageYOffset >= sectionTop - sectionHeight / 3) {
      current = section.getAttribute('id');
    }
  });

  navItems.forEach((li, index) => {
    li.classList.remove('active');
    if (current === `page${index + 1}`) {
      li.classList.add('active');
    }
  });
});

navItems.forEach((li, index) => {
  li.addEventListener('click', () => {
    document.getElementById(`page${index + 1}`).scrollIntoView({ behavior: 'smooth' });
  });
});