#import necessary modules
import streamlit as st 
from pathlib import Path
import google.generativeai as genai 
from api_key import api_key


#configure api key
genai.configure(api_key=api_key)

system_prompt='''
As a highly knowledgeable pharmacist, you are tasked with providing detailed information about various medicines. Your response should include the following sections:

1. Usage: Describe the primary uses of the medicine.
3. Side Effects: Mention any common side effects associated with the medicine.

Please provide a structured response with these headings.

'''

#create the model
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

# set the page configuration
st.set_page_config(page_title="Ausadhisthal", page_icon=":robot:", layout="wide")

# set the logo and title in the sidebar
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfkszn9Inra6fS1IzxmBX5GdD8qJVCUEBUkg&s', width=150)
st.sidebar.title("MEDICINE LOVE ❤")

# Add header and subheader with some custom styles
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3em;
        color: #ffffff;
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

st.markdown('<div class="main-header">Welcome to Ausadhisthal!</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">A web application that helps users gain knowledge about medicines</div>', unsafe_allow_html=True)

# Input field and button
medicine_name = st.text_input("Enter the medicine name:")
submit_button = st.button("Generate the Detail")

if submit_button and medicine_name:
    try:
        # Prompt ready
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        {"text": f"Medicine Name: {medicine_name}\n{system_prompt}"},
                    ],
                },
            ]
        )
        
        # Generative AI ready
        response = chat_session.send_message(f"Provide details for the medicine {medicine_name}.")
        st.write(response.text)  # Display the response in Streamlit app
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.markdown('<div class="footer">&copy; 2024 Ausadhisthal - Empowering Health with Knowledge</div>', unsafe_allow_html=True)
