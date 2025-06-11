




document.addEventListener('DOMContentLoaded', function () {
  // Initialize Splide
  var splide = new Splide('.splide', {
    type: 'loop',
    padding: '7rem',
    autoplay: true,
    speed: 1000,
    arrows: false,
    gap: '1rem',
    pauseOnFocus: true,
    mediaQuery: 'max',
    breakpoints: {
      640: {
        padding: '0',
      },
    }
  },
  );

  splide.mount();

  // Add fallback image for any failed images inside the Splide carousel
  const fallbackImage = '/static/images/default_image.png';

  document.querySelectorAll('.splide img').forEach(function (img) {
    img.addEventListener('error', function () {
      if (!this.src.includes('default_image.png')) {
        this.src = fallbackImage;
      }
    });

    // Optional: If image was already broken on load
    if (!img.complete || img.naturalWidth === 0) {
      img.src = fallbackImage;
    }
  });
});
