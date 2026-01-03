// ===============================
// Geo-Plant AI — Frontend Logic
// ===============================

// -------------------------------
// DOM Elements
// -------------------------------
const cityInput = document.getElementById("cityInput");
const latInput = document.getElementById("latInput");
const lonInput = document.getElementById("lonInput");
const questionInput = document.getElementById("questionInput");
const imageInput = document.getElementById("imageInput");
const sendBtn = document.getElementById("sendBtn");
const answerBox = document.getElementById("answerBox");
const envCards = document.getElementById("envCards");

// -------------------------------
// Map Initialization (Leaflet)
// -------------------------------
const map = L.map("map").setView([26.9124, 75.7873], 6);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap",
}).addTo(map);

let marker = L.marker([26.9124, 75.7873], { draggable: true }).addTo(map);

// -------------------------------
// Helpers
// -------------------------------
async function geocodeCity(city) {
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(city)}`;
  const res = await fetch(url);
  const data = await res.json();

  if (!data.length) return null;
  return {
    lat: parseFloat(data[0].lat),
    lon: parseFloat(data[0].lon),
  };
}

async function reverseGeocode(lat, lon) {
  const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`;
  const res = await fetch(url);
  const data = await res.json();
  return data.address?.city || data.address?.town || data.address?.state || "";
}

function renderEnvironmentCards(env) {
  envCards.innerHTML = `
    <div class="env-card">🌡 Temp: ${env.temperature_c ?? "NA"} °C</div>
    <div class="env-card">💧 Humidity: ${env.humidity ?? "NA"}%</div>
    <div class="env-card">🌫 AQI: ${env.aqi ?? "NA"}</div>
    <div class="env-card">🧪 PM2.5: ${env.pm25 ?? "NA"}</div>
    <div class="env-card">🌪 PM10: ${env.pm10 ?? "NA"}</div>
  `;
}

// -------------------------------
// City → Lat/Lon → Map
// -------------------------------
cityInput.addEventListener("blur", async () => {
  if (!cityInput.value) return;

  const geo = await geocodeCity(cityInput.value);
  if (!geo) return;

  latInput.value = geo.lat.toFixed(5);
  lonInput.value = geo.lon.toFixed(5);

  marker.setLatLng([geo.lat, geo.lon]);
  map.setView([geo.lat, geo.lon], 10);
});

// -------------------------------
// Map Drag → Lat/Lon → City
// -------------------------------
marker.on("dragend", async () => {
  const { lat, lng } = marker.getLatLng();
  latInput.value = lat.toFixed(5);
  lonInput.value = lng.toFixed(5);

  const city = await reverseGeocode(lat, lng);
  if (city) cityInput.value = city;
});

// -------------------------------
// Ask Button → Chat API
// -------------------------------
sendBtn.addEventListener("click", async () => {
  answerBox.innerText = "Thinking...";
  envCards.innerHTML = "";

  const formData = new FormData();
  formData.append("session_id", "ui-session-1");
  formData.append("latitude", latInput.value || "0");
  formData.append("longitude", lonInput.value || "0");

  if (questionInput.value.trim()) {
    formData.append("question", questionInput.value.trim());
  }

  if (imageInput.files.length > 0) {
    formData.append("image", imageInput.files[0]);
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Backend error ${res.status}: ${text}`);
    }

    const data = await res.json();
    console.log("Chat response:", data);

    answerBox.innerText = data.answer || "No answer returned.";

    if (data.environment) {
      renderEnvironmentCards(data.environment);
    }
  } catch (err) {
    console.error("Chat failed:", err);
    answerBox.innerText = "⚠️ Failed to get response. Check console.";
  }
});