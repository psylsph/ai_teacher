# AI Teacher
A custom AI teaching assistant powered by Google's Gemini AI models. This application helps students learn through interactive conversations, providing explanations, examples, and practice problems across various subjects.

## Features

- Interactive conversations with AI tutor
- Personalized learning experience
- Explanations of complex topics in simple terms
- Custom practice problems and solutions
- Progress tracking and learning path suggestions
- Support for multiple subjects (Math, Science, Programming, etc.)
- Real-time feedback and adaptive learning

## Prerequisites

- Python 3.8 or higher
- [Google API Key](https://ai.google.dev/gemini-api/docs/api-key) for Gemini AI models
- Internet connection

## Installation

1. Clone repository:
```sh
git clone https://github.com/psylsph/ai_teacher
cd ai_teacher
```

2. Install packages:
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

## Usage

1. Set your Google API key as an environment variable:

```sh
export GOOGLE_API_KEY=your_api_key_here  # Linux/Mac
# or
set GOOGLE_API_KEY=your_api_key_here     # Windows
```

2. Run the application:

```sh
streamlit run ai_teacher.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

4. Start learning by selecting a subject and engaging with the AI tutor

## License
[MIT License](./LICENSE.md)