console.log("Inject script loaded");

document.addEventListener("DOMContentLoaded", () => {
  // Inject HTML from data-include attributes
  document.querySelectorAll("[data-include]").forEach(async (el) => {
    const file = el.getAttribute("data-include");
    try {
      const res = await fetch(file);
      if (res.ok) {
        const html = await res.text();
        el.innerHTML = html;

        // Once injected, run active link check
        highlightActiveLink();

        // Then activate lightbox if this page contains a gallery
        activateLightbox();
      } else {
        el.innerHTML = `<p>⚠️ Failed to load ${file}</p>`;
      }
    } catch (err) {
      el.innerHTML = `<p>⚠️ Error loading ${file}</p>`;
    }
  });
});

function highlightActiveLink() {
  const path = window.location.pathname.split("/").pop();
  const links = document.querySelectorAll(".nav-link");

  links.forEach(link => {
    if (link.getAttribute("href") === path) {
      link.classList.add("active");
    }
  });
}

function activateLightbox() {
  const modal = document.getElementById("lightbox-modal");
  const modalImg = document.getElementById("lightbox-img");
  const closeBtn = document.querySelector(".lightbox-close");
  const prevBtn = document.querySelector(".lightbox-prev");
  const nextBtn = document.querySelector(".lightbox-next");
  const images = Array.from(document.querySelectorAll(".grid-layout img"));

  let currentIndex = -1;

  if (!modal || !modalImg || !closeBtn) return;

  function showImage(index) {
    if (index < 0) index = images.length - 1;
    if (index >= images.length) index = 0;
    currentIndex = index;
    modalImg.src = images[currentIndex].src;
    modalImg.alt = images[currentIndex].alt;
    modal.style.display = "block";
  }

  images.forEach((img, index) => {
    img.addEventListener("click", () => showImage(index));
  });

  nextBtn.onclick = () => showImage(currentIndex + 1);
  prevBtn.onclick = () => showImage(currentIndex - 1);
  closeBtn.onclick = () => modal.style.display = "none";

  window.addEventListener("keydown", (e) => {
    if (modal.style.display !== "block") return;
    if (e.key === "ArrowRight") showImage(currentIndex + 1);
    if (e.key === "ArrowLeft") showImage(currentIndex - 1);
    if (e.key === "Escape") modal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
  });
}
