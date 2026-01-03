const BASE = "http://127.0.0.1:8000/compliance";

async function load(endpoint, elementId) {
  const res = await fetch(`${BASE}/${endpoint}`);
  const data = await res.json();
  document.getElementById(elementId).textContent =
    JSON.stringify(data, null, 2);
}

load("safety", "safety");
load("knowledge", "knowledge");
load("human-reviews", "reviews");
load("metrics", "metrics");