document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("reservationForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = Object.fromEntries(new FormData(form).entries());
    try {
      const response = await fetch("https://sixa-hotel-backend.onrender.com/api/reservations/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
// ============================
// Dynamic Section Loader
// ============================
document.addEventListener("DOMContentLoaded", async () => {
  const includes = document.querySelectorAll("[data-include]");
  for (const el of includes) {
    const file = el.getAttribute("data-include");
    try {
      const response = await fetch(file);
      if (response.ok) {
        el.innerHTML = await response.text();
      } else {
        el.innerHTML = "<p>⚠️ Section failed to load.</p>";
      }
    } catch (err) {
      console.error(`Error loading ${file}:`, err);
      el.innerHTML = "<p>⚠️ Network error while loading section.</p>";
    }
  }

  // ============================
  // Reservation Form Logic
  // ============================
  const form = document.getElementById("reservationForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = Object.fromEntries(new FormData(form).entries());
    try {
      const response = await fetch("https://sixa-hotel-backend.onrender.com/api/reservations/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (response.ok && result.ok) {
        alert("✅ Reservation submitted! We'll contact you shortly.");
        form.reset();
      } else {
        alert(`❌ ${result.error || "Unable to process reservation."}`);
      }
    } catch (err) {
      console.error(err);
      alert("⚠️ Network error. Please try again later.");
    }
  });

  // ============================
  // Autofill room type from URL
  // ============================
  const urlParams = new URLSearchParams(window.location.search);
  const roomType = urlParams.get("room");
  if (roomType) {
    const roomSelect = document.getElementById("room_id");
    if (roomSelect) {
      Array.from(roomSelect.options).forEach(opt => {
        if (opt.text.toLowerCase() === roomType.toLowerCase()) {
          opt.selected = true;
        }
      });
    }
  }
});

      const result = await response.json();
      if (response.ok && result.ok) {
        alert("✅ Reservation submitted! We'll contact you shortly.");
        form.reset();
      } else {
        alert(`❌ ${result.error || "Unable to process reservation."}`);
      }
    } catch (err) {
      console.error(err);
      alert("⚠️ Network error. Please try again later.");
    }
  });

  // Autofill room type from URL param
  const urlParams = new URLSearchParams(window.location.search);
  const roomType = urlParams.get("room");
  if (roomType) {
    const roomSelect = document.getElementById("room_id");
    Array.from(roomSelect.options).forEach(opt => {
      if (opt.text.toLowerCase() === roomType.toLowerCase()) {
        opt.selected = true;
      }
    });
  }
});
