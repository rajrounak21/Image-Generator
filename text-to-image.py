import streamlit as st
import requests
import os
import time
from io import BytesIO
from PIL import Image

# Set your Hugging Face API key here or in the key.py file
from key import HUGGINGFACE_API_KEY

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_KEY


# Function to generate image using Hugging Face Inference API with retries
def generate_image(prompt, retries=5, wait_time=30):
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}"}

    # Create the payload with the prompt
    payload = {"inputs": prompt}

    # Retry mechanism
    for _ in range(retries):
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            # Read the image bytes
            image_bytes = response.content
            image = Image.open(BytesIO(image_bytes))
            return image
        elif response.status_code == 503:
            st.warning(f"Image is still loading. Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)  # Wait before retrying
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None

    st.error("Failed to generate image after multiple attempts.")
    return None


# Streamlit app layout
st.title("AI Image Generator")

# User input for the prompt
prompt = st.text_input("Enter a prompt for the image:", value="A beautiful sunset over a mountain range")

# Button to generate the image
if st.button("Generate Image"):
    if prompt:
        with st.spinner('Generating...'):
            generated_image = generate_image(prompt)
            if generated_image:
                st.image(generated_image, caption=f"Generated image for prompt: {prompt}")
    else:
        st.warning("Please enter a prompt before generating.")

# Instructions to run
st.write(
    "DESCRIPTION :- "
    "This app uses the Stable Diffusion model via Hugging Face's Inference API to generate images based on your text prompt.")
