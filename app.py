from js import localStorage, document, Event
import json
from datetime import date
from random import randint, uniform


def el(element_id):
    return document.getElementById(element_id)


def write(element_id, value):
    node = el(element_id)
    if node:
        node.innerHTML = str(value)


def load_data(key, default):
    data = localStorage.getItem(key)
    if data:
        try:
            return json.loads(data)
        except Exception:
            return default
    return default


def save_data(key, value):
    localStorage.setItem(key, json.dumps(value))


habits = load_data("habits", [])
logs = load_data("logs", {})
health = load_data("health", {"bp": [], "hr": [], "sleep": [], "steps": []})


def trigger_charts():
    document.dispatchEvent(Event.new("data-updated"))


def render_today():
    today = str(date.today())
    write("today-date", today)
    write("log-date", today)
    done = len(logs.get(today, []))
    total = len(habits)
    write("today-habits-summary", f"{done} / {total}")

    bp_text = "--"
    if health["bp"]:
        latest = health["bp"][-1]
        bp_text = f"{latest['s']}/{latest['d']}"
    write("today-bp", bp_text)

    hr_text = "--"
    if health["hr"]:
        hr_text = f"{health['hr'][-1]['value']} bpm"
    write("today-hr", hr_text)

    steps_text = "--"
    if health["steps"]:
        steps_text = f"{health['steps'][-1]['value']} steps"
    write("today-steps", steps_text)


def render_habits():
    list_node = el("habit-list")
    log_node = el("log-habits-container")
    today = str(date.today())
    today_done = logs.get(today, [])

    if not habits:
        if list_node:
            list_node.innerHTML = "<p class='muted'>No habits yet. Add one above.</p>"
        if log_node:
            log_node.innerHTML = "<p class='muted'>Add habits first to log them.</p>"
        render_today()
        trigger_charts()
        return

    habit_html = "<ul>"
    for i, habit in enumerate(habits):
        habit_html += f"""
        <li>
          <strong>{habit['name']}</strong>
          <span class='muted'>[{habit['category']}]</span>
          <button class='delete-btn' py-click='delete_habit({i})'>Delete</button>
        </li>
        """
    habit_html += "</ul>"
    list_node.innerHTML = habit_html

    log_html = ""
    for i, habit in enumerate(habits):
        checked = "checked" if i in today_done else ""
        log_html += f"""
        <label>
          <input type='checkbox' id='log-habit-{i}' {checked} />
          {habit['name']} <span class='muted'>({habit['category']})</span>
        </label>
        """
    log_node.innerHTML = log_html
    render_today()
    trigger_charts()


def add_habit(event=None):
    name_node = el("habit-name")
    category_node = el("habit-category")
    name = name_node.value.strip() if name_node else ""
    category = category_node.value if category_node else "Personal"

    if not name:
        return

    habits.append({"name": name, "category": category})
    save_data("habits", habits)
    name_node.value = ""
    render_habits()


def delete_habit(index):
    index = int(index)
    if 0 <= index < len(habits):
        habits.pop(index)
        for log_date in list(logs.keys()):
            logs[log_date] = [i for i in logs[log_date] if i != index]
        save_data("habits", habits)
        save_data("logs", logs)
        render_habits()


def save_today_log(event=None):
    today = str(date.today())
    done_ids = []
    for i in range(len(habits)):
        checkbox = el(f"log-habit-{i}")
        if checkbox and checkbox.checked:
            done_ids.append(i)
    logs[today] = done_ids
    save_data("logs", logs)
    render_today()
    trigger_charts()


def classify_bp(s, d):
    if s < 120 and d < 80:
        return "Normal"
    if s < 130 and d < 80:
        return "Elevated"
    return "High / Needs attention"


def add_bp_reading(event=None):
    s_node = el("bp-systolic")
    d_node = el("bp-diastolic")
    if not s_node.value or not d_node.value:
        return
    s = int(s_node.value)
    d = int(d_node.value)
    health["bp"].append({"date": str(date.today()), "s": s, "d": d})
    save_data("health", health)
    write("bp-status", classify_bp(s, d))
    s_node.value = ""
    d_node.value = ""
    render_today()
    trigger_charts()


def classify_hr(v):
    if v < 60:
        return "Below resting"
    if v <= 100:
        return "Normal resting"
    return "High / Active"


def add_hr_reading(event=None):
    node = el("hr-value")
    if not node.value:
        return
    v = int(node.value)
    health["hr"].append({"date": str(date.today()), "value": v})
    save_data("health", health)
    write("hr-zone", classify_hr(v))
    node.value = ""
    render_today()
    trigger_charts()


def add_sleep_record(event=None):
    node = el("sleep-hours")
    if not node.value:
        return
    hours = float(node.value)
    health["sleep"].append({"date": str(date.today()), "hours": hours})
    save_data("health", health)
    score = 100 if 7 <= hours <= 9 else 75 if 6 <= hours <= 10 else 50
    write("sleep-score", score)
    node.value = ""
    trigger_charts()


def add_steps_record(event=None):
    node = el("steps-value")
    if not node.value:
        return
    steps = int(node.value)
    health["steps"].append({"date": str(date.today()), "value": steps})
    save_data("health", health)
    pct = min(100, int((steps / 10000) * 100))
    write("steps-progress", f"{pct}% of 10,000")
    node.value = ""
    render_today()
    trigger_charts()


def generate_mock_health_data(event=None):
    health["bp"].append({"date": str(date.today()), "s": randint(110, 135), "d": randint(70, 90)})
    health["hr"].append({"date": str(date.today()), "value": randint(60, 105)})
    health["sleep"].append({"date": str(date.today()), "hours": round(uniform(5.5, 9.0), 1)})
    health["steps"].append({"date": str(date.today()), "value": randint(3500, 12000)})
    save_data("health", health)
    latest_bp = health["bp"][-1]
    write("bp-status", classify_bp(latest_bp["s"], latest_bp["d"]))
    write("hr-zone", classify_hr(health["hr"][-1]["value"]))
    write("sleep-score", "Generated")
    write("steps-progress", "Generated")
    render_today()
    trigger_charts()


render_habits()
render_today()
trigger_charts()
