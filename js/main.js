// Mobile nav toggle
const burger = document.querySelector('.site-nav__burger');
if (burger) {
  burger.addEventListener('click', () => {
    const open = document.body.classList.toggle('nav-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
}

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
