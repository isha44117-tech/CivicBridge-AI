from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/report")
def report():
    return send_from_directory(".", "report.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    description = data.get("description")
    location = data.get("location")
    category = data.get("category")

    print("Description:", description)
    print("Location:", location)
    print("Category:", category)

    return jsonify({
        "message": "Complaint received successfully!",
        "description": description,
        "location": location,
        "category": category
    })


if __name__ == "__main__":
    app.run(debug=True)