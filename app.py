# Import necessary libraries
from flask import Flask, render_template, request
import google.generativeai as genai
import os

# Initialize Flask app
app = Flask(__name__)

# Configure the Gemini API with your API key
# Set your Gemini API key here
GEMINI_API_KEY = "AIzaSyCY3U9OCQLwqXaS_qHm0L9at9LtlpJtcdE"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash",system_instruction="You are a helpful and knowledgeable Rural Education Chatbot. Your purpose is to assist users by providing information, resources, and advice on rural education, including best practices, learning tools, and general support for students and teachers in rural areas.")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Hello! This is the Rural Education Chatbot. I'm here to help you learn about educational resources, best practices for rural learning, and more. What would you like to know today?"},
    ]
)

# Define a function to generate a response using Gemini API
def get_gemini_response(user_input):
    try:
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"Sorry, I am unable to process your request at the moment: {str(e)}. Please try again later."

# Define routes for the web app
@app.route("/")
def home():
    return render_template("i.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_text = request.form["msg"]
    bot_response = get_gemini_response(user_text)
    return bot_response

# HTML template for chatbot UI
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rural Education Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        #chat-container {
            width: 50%;
            margin: 50px auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            padding: 20px;
        }
        #chatbox {
            width: 100%;
            height: 300px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
        }
        #user-input {
            width: 75%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        #send-btn {
            padding: 10px 15px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        #send-btn:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <h1>Rural Education Chatbot</h1>
        <div id="chatbox"></div>
        <input id="user-input" type="text" placeholder="Type your message here...">
        <button id="send-btn">Send</button>
    </div>
    <script>
        document.getElementById("send-btn").addEventListener("click", function() {
            var userInput = document.getElementById("user-input").value;
            document.getElementById("chatbox").innerHTML += "<div><b>You:</b> " + userInput + "</div>";
            document.getElementById("user-input").value = "";

            fetch("/get", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: "msg=" + userInput
            }).then(response => response.text()).then(data => {
                document.getElementById("chatbox").innerHTML += "<div><b>Bot:</b> " + data + "</div>";
            }).catch(error => {
                document.getElementById("chatbox").innerHTML += "<div><b>Bot:</b> Sorry, there was an error processing your request.</div>";
            });
        });
    </script>
</body>
</html>
"""

# Write the HTML to a file
with open("i.html", "w") as f:
    f.write(html_template)

# Run the Flask web server
if __name__ == "__main__":
    app.run(debug=True)
