import os
from dotenv import load_dotenv
import google.generativeai as genai # type: ignore
from flask import Flask, render_template, request

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(question)
    return response.text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input', "")

        prompt = f"""
        You are a medical information assistant providing 
        general educational information, NOT professional medical advice.

        User Query: {user_input}

        Requirements:
        - Provide general medical information in paragraph format.
        - Do not diagnose, prescribe, or give medical advice.
        - Do not request tests, imaging, or medications.
        - Explain symptoms, possible causes, and common management approaches.
        - Keep the language clear and informative.
        - No bullet points, no headings — only a paragraph.
        """

        gemini_response = get_gemini_response(prompt)

        return render_template('index.html',
                               user_input=user_input,
                               response=gemini_response)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
