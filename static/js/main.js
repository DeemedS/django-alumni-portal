// Load default image if image not found

document.querySelectorAll("img").forEach((img) => {
  img.onerror = function () {
    console.error(`Failed to load image: ${this.src}`);
    this.src = '/static/images/default_image.png';
  };
});


document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("img").forEach((img) => {
    img.onerror = function () {
      console.error(`Failed to load image: ${this.src}`);
      this.src = "/static/images/default_image.png";
      this.onerror = null; // Prevent infinite loop in case default image is missing
    };
  });
});


  