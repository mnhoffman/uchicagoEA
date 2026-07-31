// Slide-out sidebar navigation
const toggle = document.querySelector('.nav-toggle');
const scrim = document.querySelector('.nav-scrim');

function setNav(open) {
  document.body.classList.toggle('nav-open', open);
  toggle?.setAttribute('aria-expanded', open ? 'true' : 'false');
}

toggle?.addEventListener('click', () => setNav(!document.body.classList.contains('nav-open')));
scrim?.addEventListener('click', () => setNav(false));
document.querySelector('.sidebar__close')?.addEventListener('click', () => setNav(false));
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setNav(false); });
document.querySelectorAll('.sidebar a').forEach((a) => a.addEventListener('click', () => setNav(false)));

// Reveal-on-scroll (editorial sections)
const revealEls = document.querySelectorAll('.ed-reveal');
if (revealEls.length) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.15 });
  revealEls.forEach((el) => io.observe(el));
}

// Photo strip arrows
document.querySelectorAll('.ed-strip').forEach((strip) => {
  const track = strip.querySelector('.ed-strip__track');
  const step = () => {
    const img = track.querySelector('img');
    return img ? img.getBoundingClientRect().width + 16 : track.clientWidth * 0.8;
  };
  strip.querySelector('.ed-strip__arrow--prev')?.addEventListener('click', () => {
    track.scrollBy({ left: -step(), behavior: 'smooth' });
  });
  strip.querySelector('.ed-strip__arrow--next')?.addEventListener('click', () => {
    track.scrollBy({ left: step(), behavior: 'smooth' });
  });
});

// Carousel arrows (alumni section)
document.querySelectorAll('.carousel').forEach((carousel) => {
  const track = carousel.querySelector('.carousel__track');
  const step = () => {
    const card = track.querySelector('.card');
    return card ? card.getBoundingClientRect().width + 34 : track.clientWidth;
  };
  carousel.querySelector('.carousel__arrow--prev')?.addEventListener('click', () => {
    track.scrollBy({ left: -step(), behavior: 'smooth' });
  });
  carousel.querySelector('.carousel__arrow--next')?.addEventListener('click', () => {
    track.scrollBy({ left: step(), behavior: 'smooth' });
  });
});
