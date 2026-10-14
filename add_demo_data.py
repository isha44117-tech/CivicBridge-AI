import sqlite3

DATABASE = "civicbridge.db"

demo_complaints = [
    {
        "description": "[DEMO] A pothole has formed on the road.",
        "location": "Sector 22, Chandigarh",
        "category": "Road / Pothole",
        "priority": "High",
        "summary": "[DEMO] Road damage reported in Sector 22.",
        "authority": "Municipal Corporation"
    },
    {
        "description": "[DEMO] Water is leaking from a pipeline.",
        "location": "Sector 35, Chandigarh",
        "category": "Water",
        "priority": "Medium",
        "summary": "[DEMO] Water leakage reported in Sector 35.",
        "authority": "Water Supply Department"
    },
    {
        "description": "[DEMO] A streetlight is not working.",
        "location": "Sector 43, Chandigarh",
        "category": "Streetlight",
        "priority": "Medium",
        "summary": "[DEMO] Streetlight issue reported in Sector 43.",
        "authority": "Municipal Corporation"
    },
    {
        "description": "[DEMO] Garbage collection has been delayed.",
        "location": "Industrial Area, Chandigarh",
        "category": "Waste Management",
        "priority": "Low",
        "summary": "[DEMO] Waste collection issue in Industrial Area.",
        "authority": "Municipal Corporation"
    }
]

def main():
    conn = sqlite3.connect(DATABASE)

    try:
        existing_columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(complaints)")
        }

        required_columns = {
            "description", "location", "category",
            "priority", "summary", "authority"
        }

        if not required_columns.issubset(existing_columns):
            print("Database schema mismatch. No demo records added.")
            return

        added = 0

        for complaint in demo_complaints:
            exists = conn.execute(
                """
                SELECT 1 FROM complaints
                WHERE description = ?
                  AND location = ?
                LIMIT 1
                """,
                (complaint["description"], complaint["location"])
            ).fetchone()

            if exists:
                print("Already exists:", complaint["location"])
                continue

            conn.execute(
                """
                INSERT INTO complaints
                (description, location, category, priority, summary, authority)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    complaint["description"],
                    complaint["location"],
                    complaint["category"],
                    complaint["priority"],
                    complaint["summary"],
                    complaint["authority"]
                )
            )
            added += 1

        conn.commit()
        print(f"\nAdded {added} demo complaints.")
        print("Existing complaint records were preserved.")

        total = conn.execute(
            "SELECT COUNT(*) FROM complaints"
        ).fetchone()[0]

        print("Total complaints in database:", total)

    except sqlite3.Error as error:
        conn.rollback()
        print("Database error. Changes rolled back:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    main()