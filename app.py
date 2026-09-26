import os
import sqlite3
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


app = Flask(__name__)

# =========================================================
# FLASK CONFIGURATION
# =========================================================

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "change-this-secret-key"
)

DATABASE = "users.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def init_db():

    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


# =========================================================
# LOGIN PROTECTION
# =========================================================

def login_required(route):

    @wraps(route)
    def protected_route(*args, **kwargs):

        if "user_id" not in session:

            return redirect(
                url_for("login")
            )

        return route(*args, **kwargs)

    return protected_route


# =========================================================
# HOME
# =========================================================

@app.route("/")
@login_required
def home():

    return render_template(
        "index.html",
        user_name=session.get("user_name")
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not email or not password:

            return render_template(
                "login.html",
                error="Please enter your email and password."
            )

        connection = get_db()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["user_email"] = user["email"]

            return redirect(
                url_for("home")
            )

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


# =========================================================
# SIGN UP
# =========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not name or not email or not password:

            return render_template(
                "signup.html",
                error="Please fill in all fields."
            )

        if len(password) < 6:

            return render_template(
                "signup.html",
                error="Password must contain at least 6 characters."
            )

        hashed_password = generate_password_hash(
            password
        )

        connection = get_db()

        try:

            connection.execute(
                """
                INSERT INTO users
                (name, email, password)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    hashed_password
                )
            )

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return render_template(
                "signup.html",
                error="An account with this email already exists."
            )

        connection.close()

        return redirect(
            url_for("login")
        )

    return render_template("signup.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# AI BRAND VOICE GENERATOR
# =========================================================

@app.route("/generate", methods=["POST"])
@login_required
def generate():

    data = request.get_json(
        silent=True
    ) or {}

    description = data.get(
        "description",
        ""
    )

    tone = data.get(
        "tone",
        "Friendly"
    )

    audience = data.get(
        "audience",
        "General audience"
    )

    # -----------------------------------------------------
    # CLEAN INPUT
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
    # VERY LARGE REQUEST PROTECTION
    # -----------------------------------------------------

    # This is NOT the Gemini context limit.
    # It simply prevents accidentally enormous HTTP requests.

    MAX_DESCRIPTION_CHARACTERS = 2_000_000

    if len(description) > MAX_DESCRIPTION_CHARACTERS:

        return jsonify({
            "error": (
                "The brand description is extremely large. "
                "Please reduce it and try again."
            )
        }), 413


    # -----------------------------------------------------
    # API KEY
    # -----------------------------------------------------

    # Use GEMINI_API_KEY because this is the variable
    # you configured during deployment.

    google_api_key = os.environ.get(
        "GEMINI_API_KEY"
    )

    if not google_api_key:

        return jsonify({
            "error": (
                "Gemini API key is not configured. "
                "Please add GEMINI_API_KEY to your "
                "deployment environment variables."
            )
        }), 500


    # =====================================================
    # GEMINI
    # =====================================================

    try:

        model = ChatGoogleGenerativeAI(

            model="gemini-2.5-flash",

            google_api_key=google_api_key,

            temperature=0.7,

            max_retries=2
        )


        # -------------------------------------------------
        # STRUCTURED OUTPUT
        # -------------------------------------------------

        structured_model = model.with_structured_output(
            {
                "type": "object",
                "properties": {

                    "personality": {
                        "type": "string"
                    },

                    "communication_style": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },

                    "words_to_use": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },

                    "words_to_avoid": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },

                    "example_messages": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },

                "required": [
                    "personality",
                    "communication_style",
                    "words_to_use",
                    "words_to_avoid",
                    "example_messages"
                ]
            }
        )


        # -------------------------------------------------
        # PROMPT
        # -------------------------------------------------

        prompt = ChatPromptTemplate.from_messages([

            (
                "system",
                """
You are an expert brand strategist and brand voice specialist.

Your job is to analyze the COMPLETE brand information supplied
by the user.

The user may provide a very long description.

IMPORTANT:

1. Do not ignore useful information near the beginning or end.
2. Do not shorten the user's brand information yourself.
3. Understand the brand, products, values, audience, personality,
   communication preferences and examples.
4. Create a practical brand voice guide.
5. Keep the output clear and useful.
6. Follow the requested tone and audience.
7. Return the requested structured format only.

Generate:

- personality
- communication_style
- words_to_use
- words_to_avoid
- example_messages

The example messages should sound like the actual brand.
"""
            ),

            (
                "human",
                """
Here is the complete brand information.

================ BRAND DESCRIPTION ================

{description}

================ BRAND TONE ================

{tone}

================ TARGET AUDIENCE ================

{audience}

================ END BRAND INFORMATION ================

Analyze the complete information above and generate the
brand voice guide.
"""
            )
        ])


        # -------------------------------------------------
        # CREATE CHAIN
        # -------------------------------------------------

        chain = prompt | structured_model


        # -------------------------------------------------
        # GENERATE
        # -------------------------------------------------

        result = chain.invoke({

            "description": description,

            "tone": tone,

            "audience": audience
        })


        # -------------------------------------------------
        # RETURN RESULT
        # -------------------------------------------------

        return jsonify({
            "result": result
        })


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as error:

        print(
            "Gemini/LangChain error:",
            repr(error)
        )

        error_text = str(error).lower()


        # -----------------------------------------------
        # CONTEXT / TOKEN ERROR
        # -----------------------------------------------

        if (
            "token" in error_text
            or "context" in error_text
            or "too long" in error_text
            or "maximum" in error_text
        ):

            return jsonify({
                "error": (
                    "The prompt is larger than the model can "
                    "process in one request. Please reduce the "
                    "brand information and try again."
                )
            }), 413


        # -----------------------------------------------
        # API / AUTHENTICATION ERROR
        # -----------------------------------------------

        if (
            "api key" in error_text
            or "permission" in error_text
            or "authentication" in error_text
            or "unauthorized" in error_text
        ):

            return jsonify({
                "error": (
                    "There is a problem with the Gemini API key. "
                    "Check your GEMINI_API_KEY environment variable."
                )
            }), 500


        # -----------------------------------------------
        # GENERAL ERROR
        # -----------------------------------------------

        return jsonify({
            "error": (
                "Could not generate the brand voice. "
                "Please try again."
            )
        }), 500


# =========================================================
# START APPLICATION
# =========================================================

init_db()


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True
)
