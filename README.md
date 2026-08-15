✨ AI BRAND VOICE GENERATOR

🚀 Project Overview

AI Brand Voice Generator is a web application that uses Generative AI to create a complete brand voice guide from a short description of a brand.

The user provides:

- Brand description
- Brand tone
- Target audience

The application then generates:

- Brand personality
- Communication style
- Words to use
- Words to avoid
- Example brand messages

The project uses Flask + LangChain + Gemini API for the AI-powered backend and HTML, CSS, and JavaScript for the frontend.

---

🎯 Project Goal

The goal of this project is to make brand-voice creation simple and fast.

Instead of manually creating a brand guideline, users can enter a few details and receive an AI-generated voice guide within seconds.

---

🛠️ TECHNOLOGIES USED

💻 Frontend

- HTML5
- CSS3
- JavaScript

🐍 Backend

- Python
- Flask

🤖 AI

- Gemini API
- LangChain

📦 Python Packages

- Flask
- Gunicorn
- LangChain
- Gemini integration package

🧑‍💻 Development Environment

- Visual Studio Code (VS Code)

☁️ Deployment

- GitHub
- Render

---

🎨 BRAND TONE OPTIONS

The application provides the following tone options:

- Friendly
- Professional
- Bold
- Playful
- Luxury
- Minimal

The selected tone is passed to the backend and used by the AI when creating the brand voice.

---

👥 TARGET AUDIENCE OPTIONS

The application provides these target-audience options:

- General audience
- Young adults
- Professionals
- Entrepreneurs
- Creators
- Businesses

The selected audience helps the AI generate communication that is appropriate for the intended users.

---

⭐ MAIN FEATURES

✨ 1. Brand Description

Users enter information about their brand in a text area.

Example:

«EcoGlow is a modern skincare brand that creates natural, affordable skincare products using plant-based ingredients.»

The application supports up to 500 characters in the brand description.

🎨 2. Tone Selection

Users can choose the personality of their brand from the available tone options.

👥 3. Target Audience Selection

Users select who the brand is communicating with.

🤖 4. AI Brand Voice Generation

The Flask backend sends the user's information through LangChain to the Gemini API.

📋 5. Generated Brand Personality

The AI creates a description of how the brand should sound and behave.

💬 6. Communication Style

The application generates practical communication guidelines such as:

- Use clear language.
- Keep sentences easy to understand.
- Sound human.
- Focus on value.
- Maintain a consistent personality.

✅ 7. Words to Use

The AI recommends words and phrases that fit the brand.

❌ 8. Words to Avoid

The AI identifies language that may not fit the selected brand personality.

💡 9. Example Messages

The application generates example marketing messages based on the brand voice.

📋 10. Copy Result

Users can copy the generated brand voice to their clipboard.

---

🧠 HOW LANGCHAIN IS USED

LangChain acts as the AI application framework between the Flask backend and the Gemini model.

The basic flow is:

User Input
    ↓
JavaScript
    ↓
Flask API
    ↓
LangChain
    ↓
Gemini API
    ↓
Generated Brand Voice
    ↓
Flask JSON Response
    ↓
JavaScript
    ↓
Website Result

LangChain helps organize the AI interaction instead of directly handling the entire AI request inside the Flask route.

---

📁 PROJECT STRUCTURE

ai-brand-voice-generator/
│
├── app.py
│
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js

📄 app.py

Contains the Flask application, API route, LangChain logic, Gemini integration, and response handling.

📄 requirements.txt

Contains the Python dependencies required by the project.

📄 index.html

Contains the main website structure and user interface.

📄 style.css

Controls the visual design, layout, colors, cards, buttons, and responsive appearance.

📄 script.js

Handles user interaction, API requests, loading states, generated results, character counting, and copy functionality.

---

🔐 ENVIRONMENT VARIABLES

The Gemini API key should not be written directly inside the Python source code.

Instead, it is stored as an environment variable on Render.

Example:

GEMINI_API_KEY=your_api_key_here

This keeps the API key separate from the source code.

Never upload your real API key to GitHub or include it in screenshots.

---

💻 LOCAL DEVELOPMENT WITH VS CODE

Step 1 — Open the project

Open the project folder in Visual Studio Code.

Step 2 — Install dependencies

Open the VS Code terminal and run:

pip install -r requirements.txt

Step 3 — Configure the API key

Set your Gemini API key as an environment variable.

Step 4 — Run Flask

python app.py

The application can then be opened in a browser using the local Flask address.

---

☁️ DEPLOYMENT

The project is deployed using:

GitHub → Render

The deployment process is:

VS Code
   ↓
GitHub
   ↓
Render
   ↓
Live Website

Whenever the updated project is pushed to GitHub, Render can deploy the latest version.

---

🌐 LIVE DEMO

Live Website:

https://ai-brand-voice-generator.onrender.com/

The same Render URL can continue to be used as the project demo link even when the code is updated.

---

🧪 SAMPLE INPUT

Brand Description

«EcoGlow is a modern skincare brand that creates natural, affordable skincare products using plant-based ingredients. We want to help young adults build simple and healthy skincare routines.»

Tone

Friendly

Target Audience

Young adults

Expected Output

The AI generates a complete brand voice containing:

- Personality
- Communication style
- Words to use
- Words to avoid
- Example messages

---

📌 API ENDPOINT

POST "/generate"

The frontend sends:

{
  "description": "A modern skincare brand...",
  "tone": "Friendly",
  "audience": "Young adults"
}

The Flask backend processes the request and returns the generated brand voice as JSON.

---

🔄 ERROR HANDLING

The application handles situations such as:

- Empty brand description
- Missing API key
- AI API errors
- Invalid API responses
- Failed generation requests

The frontend displays an appropriate error message instead of crashing the entire application.

---

📱 RESPONSIVE DESIGN

The interface is designed to work on both:

- 📱 Mobile devices
- 💻 Desktop devices

The project was tested using the deployed Render website on a mobile browser.

---

🏆 WHAT I LEARNED

Through this project, I learned how to:

- Build a full-stack AI application
- Create a Flask REST API
- Connect a frontend with a Python backend
- Work with Gemini API
- Use LangChain in an AI application
- Handle JSON requests and responses
- Manage environment variables
- Deploy a Python application with Render
- Connect GitHub with deployment
- Create a responsive AI-powered interface
- Handle API errors and loading states

---

🚀 FUTURE IMPROVEMENTS

Possible future features include:

- Save generated brand voices
- User accounts
- Download brand guidelines as PDF
- Multiple languages
- More brand-tone options
- Custom tone input
- Brand-name input
- Logo/brand-color suggestions
- Regenerate individual sections
- AI-powered social-media captions
- AI-powered marketing copy generator

---

🎓 PROJECT SUMMARY

AI Brand Voice Generator demonstrates how modern Generative AI can be integrated into a practical web application.

The project combines:

Python + Flask + LangChain + Gemini + JavaScript + HTML + CSS + GitHub + Render

to create a complete AI-powered brand-voice generation system.

It is a practical example of using Generative AI, LLM integration, prompt engineering, API development, and cloud deployment in one project.
