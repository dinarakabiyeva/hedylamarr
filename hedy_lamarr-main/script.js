document.addEventListener('DOMContentLoaded', () => {
  // 1) Reveal-on-scroll с учётом уже видимых элементов
  const revealElems = document.querySelectorAll('.knowledge-card, .work-list > div, .plots img');
  const revealObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        obs.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  revealElems.forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      el.classList.add('visible');
    } else {
      revealObserver.observe(el);
    }
  });

  // 2) Подсветка активного пункта меню при скролле
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    sections.forEach(sec => {
      const top = sec.offsetTop - 80;
      const bottom = top + sec.offsetHeight;
      const id = sec.getAttribute('id');
      if (scrollY >= top && scrollY < bottom) {
        navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === `#${id}`));
      }
    });
  });

  // 3) Кнопка "Back to Top"
  const backBtn = document.createElement('button');
  backBtn.id = 'back-to-top';
  backBtn.textContent = '▲';
  document.body.append(backBtn);
  backBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  window.addEventListener('scroll', () => {
    backBtn.classList.toggle('show', window.scrollY > 400);
  });

  // 4) Mobile menu toggle (если понадобится)
  const menuBtn = document.querySelector('.menu-toggle');
  if (menuBtn) {
    const nav = document.querySelector('.nav-links');
    menuBtn.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
  }
});
