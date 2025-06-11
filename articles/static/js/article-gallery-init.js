document.addEventListener('DOMContentLoaded', function () {
  // Initialize Splide
  var splide = new Splide('.splide', {
    perPage: 3,
    rewind: true,
    gap: '1rem',
    height: '18rem',
    breakpoints: {
      640: {
        perPage: 1,
        height: '18rem',
      },
    },
  });

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
