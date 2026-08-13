# AI Brand Voice Generator

An AI-powered web application that generates a professional brand voice guide from a brand description, tone, and target audience.

## Live Demo

https://ai-brand-voice-generator.onrender.com

## Features

- Generate an AI-powered brand personality
- Define a communication style
- Generate words and phrases to use
- Generate words and phrases to avoid
- Create example brand messages
- Copy the generated brand voice
- Simple, clean, responsive interface
- Flask backend with Gemini AI integration
- Deployed online with Render

## Tech Stack

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- Google Gemini API
- GitHub
- Render

## How It Works

1. The user enters a description of their brand.
2. The user selects a brand tone.
3. The user selects the target audience.
4. The frontend sends the information to the Flask `/generate` endpoint.
5. Flask sends a structured prompt to the Gemini API.
6. Gemini generates a brand voice guide in JSON format.
7. Flask returns the result to the frontend.
8. JavaScript displays the generated brand voice in the result card.

## Generated Output

The application generates:

- **Personality** — A short description of the brand personality.
- **Communication Style** — Practical guidelines for how the brand should communicate.
- **Words to Use** — Recommended words and phrases.
- **Words to Avoid** — Words and styles that do not fit the brand.
- **Example Messages** — Sample brand messages that match the generated voice.

## Project Structure

```text
ai-brand-voice-generator/
├── app.py
├── requirements.txt
├── Procfile
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Requirements

- Python 3
- Flask
- Google Gemini API key
- A GitHub account for repository hosting
- A Render account for deployment

## Local Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-brand-voice-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set the Gemini API key

Create an environment variable named:

```text
GEMINI_API_KEY
```

Set its value to your Gemini API key.

**Never put your API key directly inside `app.py` or commit it to GitHub.**

### 4. Run the application

```bash
python app.py
```

Then open:

```text
http://localhost:5000
```

## Deployment

The project is deployed using Render.

The application uses the following environment variable on the server:

```text
GEMINI_API_KEY
```

The `Procfile` is used to start the Flask application in production.

## API Endpoint

### `POST /generate`

The frontend sends:

```json
{
  "description": "A modern eco-friendly skincare brand",
  "tone": "Friendly",
  "audience": "Environmentally conscious adults"
}
```

The backend returns a structured JSON result containing:

```json
{
  "result": {
    "personality": "...",
    "communication_style": [],
    "words_to_use": [],
    "words_to_avoid": [],
    "example_messages": []
  }
}
```

## Security

The Gemini API key is stored as a server-side environment variable.

Do not:

- Commit API keys to GitHub
- Put API keys in frontend JavaScript
- Share API keys publicly
- Include API keys in screenshots or documentation

## Future Improvements

Possible future improvements include:

- User accounts and saved brand voices
- Multiple brand voice templates
- Export to PDF
- Download generated brand guides
- More tone and audience options
- Brand voice history
- Custom color and branding controls
- Additional AI providers
- Improved prompt customization

## Project Goal

This project was built as a practical AI-powered web application demonstrating frontend development, Python/Flask backend development, API integration, JSON data handling, and cloud deployment.

## Author

Built as an AI web development project.

## License

This project is available for educational and portfolio purposes.
