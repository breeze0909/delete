from flask import Flask, request, jsonify, render_template
import sqlite3
import json
import os

# Flask app setup
app = Flask(__name__, template_folder="templates")
DB_FILE = "uam.db"

# ---------- Initialize Database ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            hostname TEXT,
            ip TEXT,
            os TEXT,
            user TEXT,
            active_window TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            usb_devices TEXT,
            recent_files TEXT,
            browsing_activity TEXT,
            vpn_processes TEXT,
            running_processes TEXT,
            login_events TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- API Endpoint (Agents → Server) ----------
@app.route("/api/logs", methods=["POST"])
def receive_logs():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Insert into DB
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (
                timestamp, hostname, ip, os, user, active_window,
                cpu_percent, memory_percent, usb_devices, recent_files,
                browsing_activity, vpn_processes, running_processes, login_events
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("timestamp"),
            data.get("hostname"),
            data.get("ip"),
            data.get("os"),
            data.get("user"),
            data.get("active_window"),
            data.get("cpu_percent"),
            data.get("memory_percent"),
            json.dumps(data.get("usb_devices")),
            json.dumps(data.get("recent_files")),
            json.dumps(data.get("browsing_activity")),
            json.dumps(data.get("vpn_processes")),
            json.dumps(data.get("running_processes")),
            json.dumps(data.get("login_events"))
        ))
        conn.commit()
        conn.close()

        print(f"[+] Log received from {data.get('hostname')}")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

# ---------- Dashboard ----------
@app.route("/")
def dashboard():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Fetch hosts
    cursor.execute("SELECT DISTINCT hostname FROM logs")
    hosts = [row[0] for row in cursor.fetchall()]

    # Fetch last 20 logs
    cursor.execute("""
        SELECT hostname, user, active_window, cpu_percent, memory_percent, timestamp
        FROM logs ORDER BY id DESC LIMIT 20
    """)
    rows = cursor.fetchall()

    # Fetch recent login/logoff events
    cursor.execute("SELECT login_events FROM logs ORDER BY id DESC LIMIT 10")
    login_raw = cursor.fetchall()
    login_events = []
    for row in login_raw:
        try:
            login_events.extend(json.loads(row[0]))
        except:
            pass

    # Fetch recent file activity
    cursor.execute("SELECT recent_files FROM logs ORDER BY id DESC LIMIT 10")
    file_raw = cursor.fetchall()
    file_events = []
    for row in file_raw:
        try:
            file_events.extend(json.loads(row[0]))
        except:
            pass

    conn.close()

    # Prepare HTML chunks
    logs_html = "<table><tr><th>Host</th><th>User</th><th>Active Window</th><th>CPU%</th><th>Memory%</th><th>Time</th></tr>"
    for row in rows:
        logs_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"
    logs_html += "</table>"

    login_html = "<table><tr><th>Type</th><th>Time</th><th>Source</th></tr>"
    for ev in login_events:
        login_html += f"<tr><td>{ev.get('type')}</td><td>{ev.get('time')}</td><td>{ev.get('source')}</td></tr>"
    login_html += "</table>"

    file_html = "<table><tr><th>Name</th><th>Path</th><th>Size (bytes)</th></tr>"
    for f in file_events:
        file_html += f"<tr><td>{f.get('name')}</td><td>{f.get('path')}</td><td>{f.get('size')}</td></tr>"
    file_html += "</table>"

    return render_template("dashboard.html",
                           hosts=hosts,
                           selected_host="All",
                           logs=logs_html,
                           login_html=login_html,
                           file_html=file_html)

# ---------- Run Server ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
