from flask import Flask, request, jsonify, send_from_directory
from ai import analyze_complaint
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/report")
def report():
    return send_from_directory(".", "report.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory(".", "dashboard.html")
@app.route("/dashboard-data")
def dashboard_data():
    conn = sqlite3.connect("civicbridge.db")
    conn.row_factory = sqlite3.Row

    total = conn.execute(
        "SELECT COUNT(*) FROM complaints"
    ).fetchone()[0]

    high = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE LOWER(priority) = 'high'"
    ).fetchone()[0]

    medium = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE LOWER(priority) = 'medium'"
    ).fetchone()[0]

    low = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE LOWER(priority) = 'low'"
    ).fetchone()[0]
    
    waste = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE LOWER(category) LIKE '%waste%'"
    ).fetchone()[0]

    rows = conn.execute("""
        SELECT id, category, location, priority, authority
        FROM complaints
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return jsonify({
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "waste": waste,
        "complaints": [dict(row) for row in rows]
    })
@app.route("/recurring-complaints")
def recurring_complaints():
    conn = sqlite3.connect("civicbridge.db")
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT
            category,
            location,
            COUNT(*) AS complaint_count
        FROM complaints
        GROUP BY LOWER(TRIM(category)), LOWER(TRIM(location))
        HAVING COUNT(*) > 1
        ORDER BY complaint_count DESC
    """).fetchall()

    conn.close()

    return jsonify({
        "recurring_count": len(rows),
        "recurring_complaints": [dict(row) for row in rows]
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    description = data.get("description")
    location = data.get("location")
    category = data.get("category")

    print("Description:", description)
    print("Location:", location)
    print("Category:", category)

    ai_result = analyze_complaint(description, location)

    # Save complaint to database
    conn = sqlite3.connect("civicbridge.db")

    conn.execute("""
        INSERT INTO complaints
        (description, location, category, priority, summary, authority)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        description,
        location,
        ai_result["category"],
        ai_result["priority"],
        ai_result["summary"],
        ai_result["authority"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Complaint analyzed successfully!",
        "description": description,
        "location": location,
        "category": ai_result["category"],
        "priority": ai_result["priority"],
        "summary": ai_result["summary"],
        "authority": ai_result["authority"]
    })


if __name__ == "__main__":
    app.run(debug=True)