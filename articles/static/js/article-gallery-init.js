
var splide = new Splide( '.splide', {
  perPage: 3,
  rewind : true,
  gap: '1rem',
  height: '18rem',
  breakpoints: {
    640: {
      perPage: 1,
      height: '18rem',
    },
  },
} );

splide.mount();
