import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# Configure API key
genai.configure(api_key=api_key)

# System prompt for meal planning
system_prompt = """
As a highly knowledgeable nutritionist AI, your task is to design nutrient-rich meals for breakfast, lunch, dinner, and supper based on specific diseases or for non-disease individuals. For non-disease individuals, you will take into account their age, weight, and height to generate a personalized healthy diet plan.

Please provide a structured response with the following sections:

1. **Breakfast**: Nutrient-rich meal recommendations.
2. **Lunch**: Nutrient-rich meal recommendations.
3. **Dinner**: Nutrient-rich meal recommendations.
4. **Supper**: Nutrient-rich meal recommendations.
"""

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Set the page configuration
st.set_page_config(page_title="Healthy Meal Planner", page_icon="🍴", layout="wide")

# Set the logo and title in the sidebar
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfkszn9Inra6fS1IzxmBX5GdD8qJVCUEBUkg&s', width=150)
st.sidebar.title("Healthy Meal Planner 🍴")

# Add header and subheader with some custom styles
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3em;
        color: #2874f0;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .sub-header {
        font-size: 1.5em;
        color: #2874f0;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .input-section {
        background-color: #f7f9fc;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .footer {
        font-size: 0.8em;
        color: #999999;
        text-align: center;
        padding: 20px;
    }
    .stButton>button {
        background-color: #2874f0;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #1e5ab6;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">Welcome to the Healthy Meal Planner!</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">A web application that helps you design nutrient-rich meals based on your health condition or personal details</div>', unsafe_allow_html=True)

# Input fields section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.header("Personal Details")
age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
weight = st.number_input("Enter your weight (in kg):", min_value=0, max_value=200, value=70)
height = st.number_input("Enter your height (in cm):", min_value=0, max_value=250, value=170)
condition = st.selectbox("Select your condition:", ["None", "Diabetes", "Hypertension", "Cardiovascular Disease", "Other"])

# Input fields for additional symptoms (only for other condition)
if condition == "Other":
    symptoms = st.text_area("Enter your symptoms (separated by commas):")
else:
    symptoms = ""
st.markdown('</div>', unsafe_allow_html=True)

# Submit button
st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
submit_button = st.button("Generate Meal Plan")
st.markdown('</div>', unsafe_allow_html=True)

# Display result
if submit_button:
    try:
        # Create prompt based on user inputs
        if condition == "None":
            user_prompt = f"Age: {age}, Weight: {weight} kg, Height: {height} cm. Generate a healthy diet plan."
        else:
            user_prompt = f"Condition: {condition}, Symptoms: {symptoms}. Generate a meal plan to manage this condition."
        
        # Prompt ready
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{user_prompt}\n{system_prompt}"},
                    ],
                },
            ]
        )
        
        # Generate AI response
        response = chat_session.send_message(user_prompt)
        
        # Display the response in Streamlit app
        st.write(response.text)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown('<div class="footer">&copy; 2024 Healthy Meal Planner - Eat Smart, Live Well</div>', unsafe_allow_html=True)
