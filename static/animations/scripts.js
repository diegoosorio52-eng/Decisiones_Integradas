
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