# Import required libraries
from diffusers import StableDiffusionPipeline
import torch
import streamlit as st
from PIL import Image

# Load Stable Diffusion model (using stabilityai's open-source model)
model_id = "stabilityai/stable-diffusion-2-1"  # Updated model ID
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# Define a function to generate an image based on text prompt
def generate_image(prompt):
    # Generate the image using the model
    image = pipe(prompt).images[0]
    return image

# Streamlit UI setup
def main():
    st.title("Text-to-Image Generation with Stable Diffusion")
    prompt = st.text_input("Enter a description:", "a beautiful landscape with mountains and rivers")

    if prompt:
        # Generate image based on the provided text prompt
        generated_image = generate_image(prompt)
        
        # Display the generated image using the new parameter
        st.image(generated_image, caption="Generated Image", use_container_width=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
