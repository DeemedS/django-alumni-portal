// Load default image if image not found
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll("img").forEach((img) => {
    img.onerror = function () {
      console.error(`Failed to load image: ${this.src}`);
      setTimeout(() => {
        this.src = '/static/images/default_image.png';
      }, 1000);
    };
  });
});

  