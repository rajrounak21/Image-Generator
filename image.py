import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
from key import HUGGINGFACE_API_KEY  # Import your API token

# Set up the Hugging Face API URL for FLUX.1-dev
api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


# Function to generate image from text prompt using the API
def generate_image_from_api(prompt):
    payload = {"inputs": prompt}
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        # Load the image from the API response
        image = Image.open(BytesIO(response.content))
        return image
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None


# Streamlit UI
st.title("AI Image Generator")

# Text input for prompt
prompt = st.text_input("Enter your prompt:", value="A beautiful sunset over a mountain range")

# Button to trigger the image generation
if st.button("Generate Image"):
    if prompt:
        with st.spinner("Generating...."):
            image = generate_image_from_api(prompt)

        if image:
            # Display the generated image
            st.image(image, caption="Generated Image", use_column_width=True)
    else:
        st.warning("Please enter a prompt before generating.")

st.write("Generated Image According to Your Prompt")
