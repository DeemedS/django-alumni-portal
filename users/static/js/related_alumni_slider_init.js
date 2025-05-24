$(document).ready(function () {
  splide = new Splide('.splide', {
    perPage: 1,
    perMove: 1,
    autoWidth: true,
    autoplay: false,
    speed: 1000,
    arrows: true,
    gap: '0.5rem',
    pauseOnFocus: true,
    pagination: false,
    type: 'loop',
    trimSpace: false,
  }).mount();

  fetchRelatedAlumni(null, 10);
});