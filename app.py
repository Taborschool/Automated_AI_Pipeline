from flask import Flask, render_template, request, jsonify
from main_campaign import run_campaign, init_db

app = Flask(__name__)

init_db() 
@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/run_campaign", methods=["POST"])
def campaign():
    data = request.get_json()
    topic = data.get("topic")
    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    result = run_campaign(topic)
    return jsonify(result)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
