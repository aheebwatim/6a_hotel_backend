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
