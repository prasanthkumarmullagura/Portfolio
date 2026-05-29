// ── Navbar Scroll Effect ─────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) navbar.classList.add('scrolled');
  else navbar.classList.remove('scrolled');
});

// ── Intersection Observer for Scroll Reveals ─────────
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('active');
      if (entry.target.classList.contains('bento-grid')) {
        entry.target.classList.add('in-view');
      }
    }
  });
}, observerOptions);

document.querySelectorAll('.reveal, .bento-grid').forEach(el => observer.observe(el));

// ── Parallax Effect ───────────────────────────────────
document.addEventListener('mousemove', (e) => {
  document.querySelectorAll('.parallax').forEach(el => {
    const speed = el.getAttribute('data-speed');
    const x = (window.innerWidth  - e.pageX * speed) / 100;
    const y = (window.innerHeight - e.pageY * speed) / 100;
    el.style.transform = `translateX(${x}px) translateY(${y}px)`;
  });
});

// ── Bento Hover Mesh Gradient tracking ───────────────
document.querySelectorAll('.bento-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
    card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
  });
});

// ── 3D Tilt Effect ────────────────────────────────────
document.querySelectorAll('.tilt-item').forEach(item => {
  item.addEventListener('mousemove', e => {
    const rect    = item.getBoundingClientRect();
    const rotateX = ((e.clientY - rect.top  - rect.height / 2) / (rect.height / 2)) * -10;
    const rotateY = ((e.clientX - rect.left - rect.width  / 2) / (rect.width  / 2)) *  10;
    item.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02,1.02,1.02)`;
  });
  item.addEventListener('mouseleave', () => {
    item.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1,1,1)`;
  });
});
