import os
import json

from flask import Flask, render_template, request, jsonify
from google import genai

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

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "error": "Gemini API key is not configured on the server."
        }), 500

    prompt = f"""
Create a professional brand voice guide.

Brand description:
{description}

Brand tone:
{tone}

Target audience:
{audience}

Return ONLY valid JSON with exactly these keys:

{{
  "personality": "A concise description of the brand personality.",
  "communication_style": [
    "Style point 1",
    "Style point 2",
    "Style point 3",
    "Style point 4",
    "Style point 5"
  ],
  "words_to_use": [
    "Word or phrase 1",
    "Word or phrase 2",
    "Word or phrase 3",
    "Word or phrase 4",
    "Word or phrase 5",
    "Word or phrase 6",
    "Word or phrase 7"
  ],
  "words_to_avoid": [
    "Word or phrase 1",
    "Word or phrase 2",
    "Word or phrase 3",
    "Word or phrase 4",
    "Word or phrase 5"
  ],
  "example_messages": [
    "Example brand message 1",
    "Example brand message 2",
    "Example brand message 3"
  ]
}}

Make the result specific to the brand description, tone and audience.
Return JSON only.
"""

    try:

        client = genai.Client(api_key=api_key)

        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt
        )

        output_text = interaction.output_text.strip()

        if output_text.startswith("```"):
            output_text = output_text.replace("```json", "", 1)
            output_text = output_text.replace("```", "")
            output_text = output_text.strip()

        result = json.loads(output_text)

        return jsonify({
            "result": result
        })

    except json.JSONDecodeError:
        print("Gemini returned invalid JSON:", output_text)

        return jsonify({
            "error": "The AI returned an invalid response."
        }), 500

    except Exception as e:
        print("Gemini error:", str(e))

        return jsonify({
            "error": "Could not generate the brand voice. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
