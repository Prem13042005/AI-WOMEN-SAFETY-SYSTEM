// Track Location
function trackLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      const { latitude, longitude } = position.coords;
      document.getElementById("locationDisplay").innerText =
        `Your Location:\nLat: ${latitude}, Lng: ${longitude}`;
    });
  } else {
    alert("Geolocation is not supported by your browser.");
  }
}

// Logout Modal Logic
function confirmLogout() {
  document.getElementById("logoutModal").style.display = "flex";
}

function closeLogoutModal() {
  document.getElementById("logoutModal").style.display = "none";
}

function proceedLogout() {
  localStorage.clear();
  closeLogoutModal();
  setTimeout(() => window.location.href = "/", 300);
}

// Profile Modal Logic
function openProfileModal() {
  document.getElementById("profileModal").style.display = "block";
}
function closeProfileModal() {
  document.getElementById("profileModal").style.display = "none";
}

// Register Form Handler (✅ uses JSON)
document.addEventListener('DOMContentLoaded', () => {
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', async function (e) {
      e.preventDefault();

      const data = {
        name: this.name.value,
        email: this.email.value,
        phone: this.phone.value,
        password: this.password.value
      };

      const res = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await res.json();
      const msgBox = document.getElementById('registerMsg');
      msgBox.textContent = result.message;
      msgBox.style.color = res.ok ? 'green' : 'red';

      if (res.ok) {
        setTimeout(() => window.location.href = '/login', 1500);
      }
    });
  }

  // Login Form Handler (✅ uses JSON)
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async function (e) {
      e.preventDefault();

      const data = {
        email: this.email.value,
        password: this.password.value
      };

      const res = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await res.json();
      const msgBox = document.getElementById('loginMsg');
      msgBox.textContent = result.message;
      msgBox.style.color = res.ok ? 'green' : 'red';

      if (res.ok) {
        localStorage.setItem('user_id', result.user_id);
        setTimeout(() => window.location.href = '/dashboard', 1500);
      }
    });
  }
});

// SOS Button Trigger
const sosBtn = document.getElementById('sosBtn');
if (sosBtn) {
  sosBtn.addEventListener('click', () => {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const user_id = localStorage.getItem('user_id');
      const payload = {
        user_id,
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      };

      const res = await fetch('/sos/trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      alert(data.message || "SOS triggered!");
    });
  });
}

// Add Contact (Profile modal form)
const contactForm = document.getElementById("contactForm");
if (contactForm) {
  contactForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const contact = {
      name: formData.get("contact_name"),
      number: formData.get("contact_number"),
      user_id: localStorage.getItem("user_id")
    };

    const res = await fetch("/sos/add_contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(contact)
    });

    const data = await res.json();
    alert(data.message || "Contact saved.");
  });
}

// VOICE SOS
function startVoiceRecognition() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-IN';
  recognition.onresult = function (event) {
    const command = event.results[0][0].transcript.toLowerCase();
    if (command.includes("help")) {
      triggerSOS();
    }
  };
  recognition.start();
}

// Trigger SOS with Location (generic)
function triggerSOS() {
  navigator.geolocation.getCurrentPosition(position => {
    const data = {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      user_id: localStorage.getItem('user_id'),
      message: "SOS triggered by user"
    };

    fetch('/sos/trigger', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => alert("✅ SOS alert sent!"))
    .catch(err => alert("❌ SOS failed!"));
  });
}

// AI Danger Prediction (⛑️ shows risk level)
function predictDanger() {
  if (!navigator.geolocation) {
    alert("❌ Geolocation not supported.");
    return;
  }

  navigator.geolocation.getCurrentPosition(async (position) => {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const timestamp = new Date().toISOString();

    try {
      const response = await fetch('/predict/danger_level', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude, longitude, timestamp }),
      });

      const data = await response.json();

      if (data.status === "success") {
        document.getElementById('dangerResult').innerHTML = `
          <p><strong>Risk Level:</strong> ${data.risk_level}</p>
          <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</p>
          <p>🕐 Hour: ${data.details.hour} | 🌙 Night: ${data.details.night_time ? "Yes" : "No"}</p>
          <p>📍 Location Type Code: ${data.details.location_type}</p>
        `;
      } else {
        document.getElementById('dangerResult').innerHTML = "❌ Prediction failed.";
      }
    } catch (err) {
      console.error("Prediction error:", err);
      document.getElementById('dangerResult').innerHTML = "❌ Error contacting prediction server.";
    }
  });
}
