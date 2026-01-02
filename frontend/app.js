// ================= CONFIG =================
const BACKEND_URL = "http://localhost:8000/chat";
// ================= ELEMENTS =================
const cityInput = document.getElementById("cityInput");
const latInput = document.getElementById("latInput");
const lonInput = document.getElementById("lonInput");
const questionInput = document.getElementById("questionInput");
const imageInput = document.getElementById("imageInput");
const sendBtn = document.getElementById("sendBtn");
const answerBox = document.getElementById("answerBox");

// ================= MAP =================
const map = L.map("map").setView([20.5937, 78.9629], 5);
const marker = L.marker([20.5937, 78.9629]).addTo(map);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap"
}).addTo(map);

// ================= HELPERS =================
function updateLocation(lat, lon) {
  latInput.value = lat;
  lonInput.value = lon;
  marker.setLatLng([lat, lon]);
  map.setView([lat, lon], 12);
}

// ================= GEOCODING =================
async function geocodeCity(city) {
  if (!city) return;

  const res = await fetch(
    `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(city)}`,
    {
      headers: {
        "User-Agent": "GeoPlantAI/1.0"
      }
    }
  );

  const data = await res.json();
  if (!data.length) return;

  updateLocation(data[0].lat, data[0].lon);
}

async function reverseGeocode(lat, lon) {
  const res = await fetch(
    `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`,
    {
      headers: {
        "User-Agent": "GeoPlantAI/1.0"
      }
    }
  );

  const data = await res.json();
  if (data.address?.city) cityInput.value = data.address.city;
  else if (data.address?.town) cityInput.value = data.address.town;
}

// ================= EVENTS =================
cityInput.addEventListener("change", () => {
  geocodeCity(cityInput.value);
});

latInput.addEventListener("change", () => {
  if (latInput.value && lonInput.value) {
    updateLocation(latInput.value, lonInput.value);
    reverseGeocode(latInput.value, lonInput.value);
  }
});

lonInput.addEventListener("change", () => {
  if (latInput.value && lonInput.value) {
    updateLocation(latInput.value, lonInput.value);
    reverseGeocode(latInput.value, lonInput.value);
  }
});

map.on("click", (e) => {
  updateLocation(e.latlng.lat, e.latlng.lng);
  reverseGeocode(e.latlng.lat, e.latlng.lng);
});

// ================= SUBMIT =================
sendBtn.addEventListener("click", async () => {
  answerBox.innerText = "Thinking…";

  if (!latInput.value || !lonInput.value) {
    answerBox.innerText = "Please select a location first.";
    return;
  }

  if (!questionInput.value && imageInput.files.length === 0) {
    answerBox.innerText =
      "Please ask a question or upload a plant image.";
    return;
  }

  const formData = new FormData();
  formData.append("session_id", "demo");
  formData.append("latitude", latInput.value);
  formData.append("longitude", lonInput.value);

  if (questionInput.value)
    formData.append("question", questionInput.value);

  if (imageInput.files.length > 0)
    formData.append("image", imageInput.files[0]);

  try {
    const res = await fetch(BACKEND_URL, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    console.log("Backend response:", data);

    answerBox.innerText = data.answer || "No answer returned.";

  } catch (err) {
    console.error(err);
    answerBox.innerText = "Backend connection failed.";
  }
});