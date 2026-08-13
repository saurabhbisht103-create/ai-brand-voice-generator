from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json() or {}

    description = data.get("description", "").strip()
    tone = data.get("tone", "Friendly")
    audience = data.get("audience", "General audience")

    if not description:
        return jsonify({
            "error": "Please describe your brand."
        }), 400

    # DEMO AI RESULT
    result = {
        "personality": (
            f"Warm, {tone.lower()}, approachable and human. "
            f"The brand should feel trustworthy and easy for "
            f"{audience.lower()} to connect with."
        ),

        "communication_style": [
            "Use clear and simple language.",
            "Keep sentences easy to understand.",
            "Sound human rather than overly corporate.",
            "Focus on benefits and real value.",
            f"Keep the {tone.lower()} personality consistent."
        ],

        "words_to_use": [
            "Simple",
            "Fresh",
            "Create",
            "Discover",
            "Better",
            "Built for you",
            "Let's create something great"
        ],

        "words_to_avoid": [
            "Complicated jargon",
            "Overly formal language",
            "Empty marketing promises",
            "Aggressive sales language",
            "Unnecessary technical terms"
        ],

        "example_messages": [
            "Create something people remember.",
            "Simple ideas. Powerful results.",
            "Built to help you bring your best ideas to life."
        ]
    }

    return jsonify({
        "result": result
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )