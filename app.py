import os
import json

from flask import Flask, render_template, request, jsonify
from openai import OpenAI

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

    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify({
            "error": "AI API key is not configured."
        }), 500
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
  "personality": "A short description of the brand personality.",
  "communication_style": [
    "style point 1",
    "style point 2",
    "style point 3",
    "style point 4",
    "style point 5"
  ],
  "words_to_use": [
    "word or phrase 1",
    "word or phrase 2",
    "word or phrase 3",
    "word or phrase 4",
    "word or phrase 5",
    "word or phrase 6",
    "word or phrase 7"
  ],
  "words_to_avoid": [
    "word or phrase 1",
    "word or phrase 2",
    "word or phrase 3",
    "word or phrase 4",
    "word or phrase 5"
  ],
  "example_messages": [
    "example message 1",
    "example message 2",
    "example message 3"
  ]
}}

Make the result specific to the brand description, tone, and audience.
Do not use generic filler.
"""

    try:
        response = client.responses.create(
            model="gpt-5.5",
            instructions="You are an expert brand strategist and copywriter.",
            input=prompt
        )

        result = json.loads(response.output_text)

        return jsonify({
            "result": result
        })

    except json.JSONDecodeError:
        return jsonify({
            "error": "The AI returned an invalid response. Please try again."
        }), 500

    except Exception as e:
        print("AI ERROR:", e)

        return jsonify({
            "error": "Something went wrong while generating the brand voice."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
