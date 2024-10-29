// Load default image if image not found

function setImageErrorHandling() {
  document.querySelectorAll("img").forEach((img) => {
    img.onerror = function () {
      console.error(`Failed to load image: ${this.src}`);
      this.src = '/static/images/default_image.png';
    };
  });
}

setImageErrorHandling();

const observer = new MutationObserver(setImageErrorHandling);
observer.observe(document.body, {
  childList: true,
  subtree: true,
});

document.addEventListener('DOMContentLoaded', setImageErrorHandling);
  