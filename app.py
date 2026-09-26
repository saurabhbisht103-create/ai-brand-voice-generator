import os
import json

from flask import Flask, render_template, request, jsonify

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# AI BRAND VOICE GENERATOR
# =========================================================

@app.route("/generate", methods=["POST"])
def generate():

    # -----------------------------------------------------
    # GET JSON DATA
    # -----------------------------------------------------

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid request. Please send JSON data."
        }), 400


    # -----------------------------------------------------
    # GET USER INPUT
    # -----------------------------------------------------

    description = data.get("description", "")
    tone = data.get("tone", "Friendly")
    audience = data.get(
        "audience",
        "General audience"
    )


    # -----------------------------------------------------
    # VALIDATE TEXT
    # -----------------------------------------------------

    if not isinstance(description, str):
        return jsonify({
            "error": "Brand description must be text."
        }), 400

    if not isinstance(tone, str):
        tone = "Friendly"

    if not isinstance(audience, str):
        audience = "General audience"


    description = description.strip()
    tone = tone.strip()
    audience = audience.strip()


    # -----------------------------------------------------
    # EMPTY DESCRIPTION
    # -----------------------------------------------------

    if not description:

        return jsonify({
            "error": "Please describe your brand."
        }), 400


    # -----------------------------------------------------
    # LARGE PROMPT PROTECTION
    # -----------------------------------------------------

    # Gemini 2.5 Flash supports a very large context window.
    #
    # This limit is intentionally much larger than a normal
    # brand description, while preventing accidental gigantic
    # HTTP requests from crashing the server.

    MAX_DESCRIPTION_CHARACTERS = 3_500_000

    if len(description) > MAX_DESCRIPTION_CHARACTERS:

        return jsonify({
            "error": (
                "Your brand description is extremely large. "
                "Please reduce the text slightly and try again."
            )
        }), 413


    # =====================================================
    # GEMINI API KEY
    # =====================================================

    # IMPORTANT:
    #
    # Render environment variable:
    #
    # GEMINI_API_KEY
    #
    # The name here must match exactly.

    google_api_key = os.environ.get(
        "GEMINI_API_KEY"
    )


    if not google_api_key:

        return jsonify({
            "error": (
                "GEMINI_API_KEY is not configured. "
                "Please add it in Render Environment Variables."
            )
        }), 500


    # =====================================================
    # GEMINI MODEL
    # =====================================================

    try:

        model = ChatGoogleGenerativeAI(

            model="gemini-3.8-flash",

            google_api_key=google_api_key,

            temperature=0.7,

            max_retries=5
        )


        # =================================================
        # PROMPT
        # =================================================

        prompt = ChatPromptTemplate.from_messages([

            (
                "system",
                """
You are an expert brand strategist and brand voice specialist.

Your task is to analyze the COMPLETE brand information provided
by the user and create a professional brand voice guide.

The user's description may be very long.

IMPORTANT RULES:

1. Analyze the complete information.
2. Do not intentionally ignore information from the beginning,
   middle, or end of the description.
3. Extract important brand values, personality, positioning,
   audience, products, services, communication preferences,
   and examples.
4. Respect the requested brand tone.
5. Make the result practical and useful.
6. Do not invent facts that contradict the user's description.
7. If the user provides examples of how the brand communicates,
   use them to understand the brand voice.
8. Return ONLY valid JSON.
9. Do not use Markdown code fences.

The JSON must contain exactly these keys:

personality
communication_style
words_to_use
words_to_avoid
example_messages

Data types:

personality:
string

communication_style:
array of strings

words_to_use:
array of strings

words_to_avoid:
array of strings

example_messages:
array of strings
"""
            ),

            (
                "human",
                """
COMPLETE BRAND INFORMATION

--------------------------------------------------

Brand description:

{description}

--------------------------------------------------

Preferred brand tone:

{tone}

--------------------------------------------------

Target audience:

{audience}

--------------------------------------------------

END OF BRAND INFORMATION

Now analyze the complete information and generate the
brand voice guide.
"""
            )

        ])


        # =================================================
        # CREATE CHAIN
        # =================================================

        chain = prompt | model


        # =================================================
        # SEND REQUEST TO GEMINI
        # =================================================

        response = chain.invoke({

            "description": description,

            "tone": tone,

            "audience": audience
        })


        # =================================================
        # GET MODEL RESPONSE
        # =================================================

        content = response.content


        # Sometimes LangChain can return a list of content
        # blocks instead of a simple string.

        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, str):

                    text_parts.append(item)

                elif isinstance(item, dict):

                    if "text" in item:

                        text_parts.append(
                            str(item["text"])
                        )

            content = "".join(text_parts)


        content = str(content).strip()


        # =================================================
        # REMOVE MARKDOWN JSON FENCES
        # =================================================

        if content.startswith("```json"):

            content = content[
                len("```json"):
            ].strip()

        elif content.startswith("```"):

            content = content[
                len("```"):
            ].strip()


        if content.endswith("```"):

            content = content[:-3].strip()


        # =================================================
        # CONVERT JSON TEXT TO PYTHON OBJECT
        # =================================================

        try:

            result = json.loads(content)

        except json.JSONDecodeError:

            # Sometimes the model may place extra text
            # around the JSON. Try to find the JSON object.

            start = content.find("{")
            end = content.rfind("}")

            if start == -1 or end == -1:

                return jsonify({
                    "error": (
                        "Gemini returned an invalid response. "
                        "Please try again."
                    )
                }), 500

            try:

                result = json.loads(
                    content[start:end + 1]
                )

            except json.JSONDecodeError:

                return jsonify({
                    "error": (
                        "Gemini returned an invalid JSON response. "
                        "Please try again."
                    )
                }), 500


        # =================================================
        # BASIC RESULT VALIDATION
        # =================================================

        required_keys = [

            "personality",

            "communication_style",

            "words_to_use",

            "words_to_avoid",

            "example_messages"
        ]


        for key in required_keys:

            if key not in result:

                result[key] = []


        # =================================================
        # RETURN RESULT TO FRONTEND
        # =================================================

        return jsonify({
            "result": result
        })


    # =====================================================
    # TOKEN / CONTEXT ERROR
    # =====================================================

    except Exception as error:

        error_text = str(error)

        print(
            "========================================"
        )

        print(
            "GEMINI ERROR:"
        )

        print(
            error_text
        )

        print(
            "========================================"
        )


        lower_error = error_text.lower()


        # -------------------------------------------------
        # CONTEXT / TOKEN LIMIT
        # -------------------------------------------------

        if (
            "token" in lower_error
            or "context" in lower_error
            or "too long" in lower_error
            or "maximum" in lower_error
            or "413" in lower_error
        ):

            return jsonify({
                "error": (
                    "The brand description is larger than "
                    "Gemini can process in one request. "
                    "Please reduce the text and try again."
                )
            }), 413


        # -------------------------------------------------
        # API KEY / AUTHENTICATION
        # -------------------------------------------------

        if (
            "api key" in lower_error
            or "permission" in lower_error
            or "authentication" in lower_error
            or "unauthorized" in lower_error
            or "401" in lower_error
            or "403" in lower_error
        ):

            return jsonify({
                "error": (
                    "There is a problem with the Gemini API key. "
                    "Please check GEMINI_API_KEY in Render."
                )
            }), 500


        # -------------------------------------------------
        # RATE LIMIT
        # -------------------------------------------------

        if (
            "429" in lower_error
            or "rate limit" in lower_error
            or "quota" in lower_error
        ):

            return jsonify({
                "error": (
                    "Gemini API limit has been reached. "
                    "Please wait and try again."
                )
            }), 429


        # -------------------------------------------------
        # GENERAL ERROR
        # -------------------------------------------------

        return jsonify({
            "error": (
                "Could not generate the brand voice. "
                "Please try again."
            )
        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
