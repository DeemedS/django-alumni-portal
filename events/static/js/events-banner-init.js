
var splide = new Splide( '.splide', {
  type   : 'loop',
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