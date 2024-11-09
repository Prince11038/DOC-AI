import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# Configure API key
genai.configure(api_key=api_key)

# System prompt for disease prediction
system_prompt = """
As a highly knowledgeable medical AI, your task is to predict possible diseases based on the provided symptoms. Your response should include the following sections:

1. **Mild Threat**: Diseases that are not life-threatening and can be treated with simple remedies or lifestyle changes.
2. **Moderate Threat**: Diseases that require medical attention but are not immediately life-threatening.
3. **Severe Threat**: Diseases that are serious and require immediate medical attention.

Please provide a structured response with these headings. Narrow down the possible diseases with each additional symptom.
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
st.set_page_config(page_title="Disease Predictor", page_icon=":hospital:", layout="wide")

# Set the logo and title in the sidebar
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfkszn9Inra6fS1IzxmBX5GdD8qJVCUEBUkg&s', width=150)
st.sidebar.title("Disease Predictor")

# Add header and subheader with some custom styles
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3em;
        color: #2874f0;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5em;
        color: #2874f0;
        text-align: center;
    }
    .footer {
        font-size: 0.8em;
        color: #999999;
        text-align: center;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">Welcome to the Disease Predictor!</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">A web application that helps predict possible diseases based on your symptoms</div>', unsafe_allow_html=True)

# Input field and button
symptoms_list = st.text_area("Enter the symptoms (separated by commas):")
submit_button = st.button("Predict Disease")

if submit_button and symptoms_list:
    try:
        # Format symptoms for the prompt
        formatted_symptoms = "\n".join([f"- {symptom.strip()}" for symptom in symptoms_list.split(",")])
        
        # Prompt ready
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        {"text": f"Symptoms: {formatted_symptoms}\n{system_prompt}"},
                    ],
                },
            ]
        )
        
        # Generate AI response
        response = chat_session.send_message(f"Here are the possible diseases based on the symptoms: {formatted_symptoms}.")
        
        # Display the response in Streamlit app
        st.write(response.text)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown('<div class="footer">&copy; 2024 Disease Predictor - Helping You Stay Healthy</div>', unsafe_allow_html=True)
