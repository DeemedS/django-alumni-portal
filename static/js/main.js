// Load default image if image not found
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("img").forEach((img) => {
    img.onerror = function () {
      console.error(`Failed to load image: ${this.src}`);
      this.src = "/static/images/default_image.png";
      this.onerror = null;
    };
  });
});
  

document.querySelectorAll("img").forEach((img) => {
  img.onerror = function () {
    console.error(`Failed to load image: ${this.src}`);
    this.src = "/static/images/default_image.png";
    this.onerror = null;
  };
});