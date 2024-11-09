#import necessary modules
import streamlit as st 
from pathlib import Path
import google.generativeai as genai 
from api_key import api_key
import tempfile

#configure api key
genai.configure(api_key=api_key)

system_prompt='''
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues present in the images.

Responsibilities:

1.Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.

2.Findings Report: Document all observed anomalies or signs of diseases and clearly articulate these findings in a structured format.

3.Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.

4.Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1.Scope of Response: Only respond if the image pertains to human health issues.

2.Clarity of Images: If the image quality impedes clear analysis, note that certain aspects are unable to be determined based on the provided image.
3.Disclaimer: Accompany your analysis with the disclaimer:"Consult with a Doctor before making any decisions"
4.Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structural approach outlined above.

Please provide me an output respones with these 4 headings Detailed Analysis,Findings Report,Recommendations and Next Steps,Treatment Suggestions.


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
st.set_page_config(page_title="medicare",page_icon=":robot:")

# set the logo
st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfkszn9Inra6fS1IzxmBX5GdD8qJVCUEBUkg&s', width=200)

# set the title
st.title("MEDICARE")

# set the subtitle
st.subheader("An web application that can help users to identify medical images ")
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])

submit_button = st.button("Generate the Analysis")

def upload_to_gemini(path, mime_type=None):
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        st.error(f"Error uploading file: {e}")
        return None

files = []

if submit_button and uploaded_file:
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
        
        # Upload to Gemini
        file = upload_to_gemini(temp_file_path, mime_type="image/jpeg")
        if file:
            files = [file]
        
        # Prompt ready
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        {"file_data": {"file_uri": files[0].uri, "mime_type": "image/jpeg"}},
                        {"text": system_prompt},
                    ],
                },
            ]
        )
        
        # Generative AI ready
        response = chat_session.send_message("Analyze the medical image.")
        st.write(response.text)  # Display the response in Streamlit app
    except Exception as e:
        st.error(f"An error occurred: {e}")
