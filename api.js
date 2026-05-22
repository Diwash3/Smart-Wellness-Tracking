const API_BASE_URL = "https://YOUR-RENDER-URL.onrender.com"; // replace later

// Get all data
async function fetchData() {
  const res = await fetch(`${API_BASE_URL}/api/data`);
  return await res.json();
}

// Save habit
async function saveHabit(habit) {
  await fetch(`${API_BASE_URL}/api/habits`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(habit)
  });
}

// Save goal
async function saveGoal(goal) {
  await fetch(`${API_BASE_URL}/api/goals`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(goal)
  });
}

// Save health
async function saveHealth(data) {
  await fetch(`${API_BASE_URL}/api/health`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });
}
