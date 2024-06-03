from flask import Flask, render_template, redirect, request

# Add OpenAI API
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values

# Load API_KEY
load_dotenv()

# Establish a connection with OpenAI
connection = OpenAI()

# Configure Flask app
app = Flask(__name__)

# Enable auto-reload
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Create main route in code, loading index.html page
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the POST request
        # Start by getting prompt and validating it
        prompt = request.form.get("prompt")
        if not prompt:
            print("You forgot the prompt!")
            return redirect("/")
        
        # API
        # Handle sending this prompt tp ChatGPT's API
        output = askAI(prompt)
        return render_template('index.html', output=output)
    else:
        # GET method
        return render_template('index.html')
    
# Handle API Requests
def askAI(prompt):
    completion = connection.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role":"user",
                "content": prompt
            },
            {
                "role":"system",
                "content":"Answer each question through rhyming! Like a poem"
            }
        ]
    )
    # Get the best response from the completion variable from the API call.
    response = completion.choices[0].message.content
    return response