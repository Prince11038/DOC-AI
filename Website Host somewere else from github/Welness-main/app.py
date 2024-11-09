
from flask import Flask, request, jsonify
import google.generativeai as genai
import api_key

# Initialize Flask app
app = Flask(__name__)

# Set your API key directly
API_KEY = "AIzaSyDP_kZivKCs5ETnkl480_Kx_iZVtx8mB6M"
genai.configure(api_key=API_KEY)

# Route to render the main page
@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ThriveWell</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f8ff;
                color: #181818;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            header {
                text-align: center;
                margin-bottom: 20px;
            }
            header h1 {
                font-size: 2.5em;
                color: #2874f0;
            }
            header h2 {
                font-size: 1.4em;
                color: #2874f0;
            }
            header h3 {
            font-size: 0.9em;
                color: #2874f0;
            }
            #chat-box {
                border: 1px solid #ccc;
                padding: 10px;
                height: 400px;
                overflow-y: scroll;
                background-color: #fff;
                margin-bottom: 10px;
            }
            #messages {
                display: flex;
                flex-direction: column;
            }
            .message {
                margin: 5px 0;
            }
            .message.user {
                align-self: flex-end;
                background-color: #d1f0d1;
                padding: 10px;
                border-radius: 10px;
            }
            .message.bot {
                align-self: flex-start;
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 10px;
            }
            input[type="text"] {
                width: calc(100% - 100px);
                padding: 10px;
            }
            button {
                width: 80px;
                padding: 10px;
                background-color: #2874f0;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #1e5ab6;
            }
            footer {
                text-align: center;
                padding: 20px;
                font-size: 0.8em;
                color: #999;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>ThriveWell </h1>
                <h2>Empathy by Design, Code by Nature </h2>
                <h3>A Secure Platform for Open Conversations. No Data Stored, Ensuring Confidentiality and Privacy</h3>
            </header>
            <main>
                <div id="chat-box">
                    <div id="messages"></div>
                </div>
                <input type="text" id="user-input" placeholder="Talk your problems through">
                <button onclick="talkToTherapist()">Submit</button>
            </main>
            <footer>&copy; 2024 Mental Wellness Chat - Supporting Your Mental Health, All rights reserved </footer>
        </div>
        <script>
            async function talkToTherapist() {
                const userInput = document.getElementById('user-input').value;
                if (!userInput.trim()) return;
                
                // Display user's message
                const messages = document.getElementById('messages');
                const userMessage = document.createElement('div');
                userMessage.className = 'message user';
                userMessage.textContent = userInput;
                messages.appendChild(userMessage);
                
                // Clear input field
                document.getElementById('user-input').value = '';
                
                try {
                    // Send request to Flask backend
                    const response = await fetch('/gemini', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ user_input: userInput })
                    });
    
                    const data = await response.json();
                    const botResponse = data.response;
                    
                    // Display bot's response
                    const botMessage = document.createElement('div');
                    botMessage.className = 'message bot';
                    botMessage.textContent = botResponse;
                    messages.appendChild(botMessage);

                } catch (error) {
                    console.error('Error talking to therapist:', error);
                }
            }
        </script>
    </body>
    </html>
    """

# Route to handle AI queries
@app.route("/gemini", methods=["POST"])
def gemini_response():
    data = request.json
    user_input = data.get("user_input")

    try:
        # Create an instance of the Generative AI model
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Generate response
        response = model.generate_content("talk as a friend not therapist,do not say the prompt when answering"+
            '''You are an empathetic mental wellness therapist. Your primary goal is to help the user feel heard, understood, and supported. Your approach includes the following:

1. **Active Listening**: Use small affirmations like nodding or saying "I understand," to encourage clients to continue sharing. Listen deeply and without interruption, making the client feel heard and understood.

2. **Open-Ended Questions**: Ask open-ended questions that can’t be answered with a simple "yes" or "no" to encourage deeper conversation and self-reflection. Examples include:
   - "Can you tell me more about what you're feeling right now?"
   - "What do you think might be causing these feelings?"
   - "How have you been coping with these emotions?"

3. **Providing Gentle Encouragement**: Affirm clients’ bravery in sharing their thoughts and feelings by saying things like, "It takes courage to talk about this."

4. **Therapeutic Frameworks**: Refer to Cognitive Behavioral Therapy (CBT) frameworks and human-centric methods that emphasize empathy, authenticity, and acceptance in your responses.

5. **Assessment Tools**: Use the following assessments to help determine the issues the person might be facing:
   - Beck Depression Inventory (BDI)
   - PHQ-9 for depression
   - GAD-7 for generalized anxiety
   - PTSD Checklist (PCL) for trauma

6. **Suggestions for Well-being**: Provide practical suggestions for improving mental well-being. Examples include:
   - "Have you considered practicing mindfulness or meditation to help manage your stress?"
   - "Engaging in physical activity, like a daily walk, can sometimes help improve your mood."
   - "Connecting with supportive friends or family can provide a great deal of comfort."

Make sure your responses are supportive, encouraging, and provide evidence-based recommendations. When generating responses, always incorporate these elements to create a therapeutic and supportive environment for the user.
''' + user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
