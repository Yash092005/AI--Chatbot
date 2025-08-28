from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3, json, os
from calc import calc_water
from kb_search import kb_search

app = FastAPI()

DB = os.path.join(os.path.dirname(__file__), '..', 'database.sqlite')

class Message(BaseModel):
    user_id: str
    text: str
    locale: str = "en"

def get_conn():
    return sqlite3.connect(DB)

def log_message(user_id, sender, text):
    conn = get_conn()
    c = conn.cursor()
    # Simple session handling: use session_id = 1 for demo
    c.execute("INSERT INTO messages (session_id, sender, text) VALUES (1, ?, ?)", (sender, text))
    conn.commit()
    conn.close()

@app.post("/api/chat")
def chat(m: Message):
    t = m.text.lower()
    if "calculate" in t or "footprint" in t or "water use" in t:
        reply = "Please provide details like: people=3, showers=1, minutes=7, flushes=4, laundry=3, dish=15, garden=30"
    elif "rain" in t or "harvest" in t:
        reply = "Rainwater harvesting: clean roof, install first-flush, storage tank. Formula: roof_area (m2) * rainfall (m) * 0.8 (efficiency)."
    elif "leak" in t:
        reply = "Leak check: Close all taps, note meter, wait 30 min. If meter moved, you have a leak. For cistern leaks, add food coloring to tank and see if bowl shows color."
    else:
        reply = kb_search(t)
    log_message(m.user_id, "user", m.text)
    log_message(m.user_id, "bot", reply)
    return {"reply": reply}

@app.post("/api/calc")
def calc_endpoint(payload: dict):
    # Accept either JSON inputs or a simple key=value string in 'text'
    inputs = payload
    result = calc_water(inputs)
    # Optionally log to calc_runs (not required for demo)
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO calc_runs (user_id, inputs_json, result_lpd, top_sources_json) VALUES (?,?,?,?)",
                  (1, json.dumps(inputs), float(result.get('total_lpd',0)), json.dumps(result.get('top_sources',[]))))
        conn.commit()
        conn.close()
    except Exception:
        pass
    return result
