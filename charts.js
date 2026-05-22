function readStore() {
  const health = JSON.parse(localStorage.getItem("health") || '{"bp":[],"hr":[],"sleep":[],"steps":[]}');
  const logs = JSON.parse(localStorage.getItem("logs") || "{}");
  const habits = JSON.parse(localStorage.getItem("habits") || "[]");
  return { health, logs, habits };
}

let bpChart, hrChart, sleepChart, stepsChart, habitChart;

const commonOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { labels: { color: "#e5e7eb" } } },
  scales: {
    x: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(148,163,184,0.12)" } },
    y: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(148,163,184,0.12)" } }
  }
};

function rebuildChart(existing, ctx, config) {
  if (!ctx) return null;
  if (existing) existing.destroy();
  return new Chart(ctx, config);
}

function buildCharts() {
  const { health, logs, habits } = readStore();

  bpChart = rebuildChart(bpChart, document.getElementById("bpChart"), {
    type: "line",
    data: {
      labels: health.bp.map((_, i) => `R${i + 1}`),
      datasets: [
        { label: "Systolic", data: health.bp.map(r => r.s), borderColor: "#22c55e", backgroundColor: "rgba(34,197,94,0.18)", tension: 0.35 },
        { label: "Diastolic", data: health.bp.map(r => r.d), borderColor: "#38bdf8", backgroundColor: "rgba(56,189,248,0.18)", tension: 0.35 }
      ]
    },
    options: commonOptions
  });

  hrChart = rebuildChart(hrChart, document.getElementById("hrChart"), {
    type: "line",
    data: {
      labels: health.hr.map((_, i) => `R${i + 1}`),
      datasets: [{ label: "Heart Rate", data: health.hr.map(r => r.value), borderColor: "#f97316", backgroundColor: "rgba(249,115,22,0.18)", tension: 0.35 }]
    },
    options: commonOptions
  });

  sleepChart = rebuildChart(sleepChart, document.getElementById("sleepChart"), {
    type: "bar",
    data: {
      labels: health.sleep.map((_, i) => `D${i + 1}`),
      datasets: [{ label: "Sleep Hours", data: health.sleep.map(r => r.hours), backgroundColor: "#6366f1" }]
    },
    options: commonOptions
  });

  stepsChart = rebuildChart(stepsChart, document.getElementById("stepsChart"), {
    type: "bar",
    data: {
      labels: health.steps.map((_, i) => `D${i + 1}`),
      datasets: [{ label: "Steps", data: health.steps.map(r => r.value), backgroundColor: "#22c55e" }]
    },
    options: commonOptions
  });

  const dates = Object.keys(logs).sort();
  const completion = dates.map(d => Math.round((logs[d].length / (habits.length || 1)) * 100));
  habitChart = rebuildChart(habitChart, document.getElementById("habitChart"), {
    type: "line",
    data: {
      labels: dates,
      datasets: [{ label: "Habit Completion %", data: completion, borderColor: "#a855f7", backgroundColor: "rgba(168,85,247,0.18)", tension: 0.35 }]
    },
    options: commonOptions
  });
}

document.addEventListener("DOMContentLoaded", buildCharts);
document.addEventListener("data-updated", buildCharts);
setTimeout(buildCharts, 1200);
