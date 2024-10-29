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

document.addEventListener('DOMContentLoaded', function() {
  const observerTarget = document.body; 
  
  if (observerTarget instanceof Node) {
    const observer = new MutationObserver(setImageErrorHandling);
    observer.observe(observerTarget, {
      childList: true,  // Observe direct children
      subtree: true,    // Observe all descendants
    });
  }
});