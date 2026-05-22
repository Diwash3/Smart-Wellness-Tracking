const express = require("express");
const fs = require("fs");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const DATA_FILE = "./data.json";

// Read data
function readData() {
  const data = fs.readFileSync(DATA_FILE);
  return JSON.parse(data);
}

// Write data
function writeData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

// GET all data
app.get("/api/data", (req, res) => {
  const data = readData();
  res.json(data);
});

// POST habit
app.post("/api/habits", (req, res) => {
  const data = readData();
  data.habits.push(req.body);
  writeData(data);
  res.json({ message: "Habit saved" });
});

// POST goal
app.post("/api/goals", (req, res) => {
  const data = readData();
  data.goals.push(req.body);
  writeData(data);
  res.json({ message: "Goal saved" });
});

// POST health
app.post("/api/health", (req, res) => {
  const data = readData();
  data.health.push(req.body);
  writeData(data);
  res.json({ message: "Health data saved" });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
