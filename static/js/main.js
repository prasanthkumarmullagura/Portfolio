// Navbar Scroll Effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if(window.scrollY > 50) navbar.classList.add('scrolled');
  else navbar.classList.remove('scrolled');
});

// Intersection Observer for Scroll Reveals
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if(entry.isIntersecting) {
      entry.target.classList.add('active');
      if(entry.target.classList.contains('bento-grid')) {
        entry.target.classList.add('in-view');
      }
    }
  });
}, observerOptions);

document.querySelectorAll('.reveal, .bento-grid').forEach(el => observer.observe(el));

// Parallax Effect
document.addEventListener('mousemove', (e) => {
  document.querySelectorAll('.parallax').forEach(el => {
    const speed = el.getAttribute('data-speed');
    const x = (window.innerWidth - e.pageX * speed) / 100;
    const y = (window.innerHeight - e.pageY * speed) / 100;
    el.style.transform = `translateX(${x}px) translateY(${y}px)`;
  });
});

// Bento Hover Mesh Gradient tracking
document.querySelectorAll('.bento-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--mouse-x', `${x}px`);
    card.style.setProperty('--mouse-y', `${y}px`);
  });
});

// 3D Tilt Effect
const tiltItems = document.querySelectorAll('.tilt-item');
tiltItems.forEach(item => {
  item.addEventListener('mousemove', e => {
    const rect = item.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -10;
    const rotateY = ((x - centerX) / centerX) * 10;
    
    item.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
  });
  
  item.addEventListener('mouseleave', () => {
    item.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
  });
});

// Toast Notification Logic
const toast = document.getElementById('toast-bar');
let toastTimeout;

document.querySelectorAll('.nav-links a, .btn-primary, .btn-outline').forEach(link => {
  link.addEventListener('click', (e) => {
    const target = e.currentTarget.getAttribute('href');
    if(target && target.startsWith('#')) {
      const sectionName = target.replace('#', '');
      const titles = { 'about': 'About Me Details', 'education': 'Education Details', 'skills': 'Technical Skills', 'projects': 'Featured Work', 'contact': 'Contact Let\'s Talk' };
      
      const text = titles[sectionName] || sectionName;
      if (text) {
          toast.innerText = `Viewing: ${text}`;
          toast.classList.add('show');
          clearTimeout(toastTimeout);
          toastTimeout = setTimeout(() => toast.classList.remove('show'), 3000);
      }
    }
  });
});
