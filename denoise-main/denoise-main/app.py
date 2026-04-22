# app.py

import cv2
import numpy as np
import tensorflow as tf
import gradio as gr

# Load the trained model without restoring old optimizer/loss, then re-compile
model = tf.keras.models.load_model("best_model.h5", compile=False)
model.compile(optimizer="adam", loss="mse")

def process_and_denoise(image):
    """
    Takes any input image (color or grayscale), converts it to 64×64 grayscale,
    adds Gaussian noise, runs the autoencoder, and returns all three stages
    upsampled to 128×128 for clearer display:
      1) Original resized
      2) Noisy version
      3) Denoised reconstruction
    """
    # Convert to single-channel grayscale
    if image.ndim == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image[..., 0] if image.ndim == 3 else image

    # Resize down to 64×64 for the model
    small = cv2.resize(gray, (64, 64))
    norm   = small.astype(np.float32) / 255.0

    # Add Gaussian noise
    sigma = 0.1
    noisy = norm + sigma * np.random.randn(*norm.shape)
    noisy = np.clip(noisy, 0.0, 1.0)

    # Denoise with the autoencoder
    inp  = noisy[np.newaxis, ..., np.newaxis]   # (1,64,64,1)
    pred = model.predict(inp)[0, ..., 0]         # (64,64)

    # Convert back to uint8
    orig_disp = (norm  * 255).astype(np.uint8)
    noisy_disp = (noisy * 255).astype(np.uint8)
    recon_disp = (pred  * 255).astype(np.uint8)

    # Upsample each to 128×128 for display
    def upsample(img):
        return cv2.resize(img, (128, 128), interpolation=cv2.INTER_LINEAR)

    return upsample(orig_disp), upsample(noisy_disp), upsample(recon_disp)

demo = gr.Interface(
    fn=process_and_denoise,
    inputs=gr.Image(type="numpy", label="Input Image"),
    outputs=[
        gr.Image(type="numpy", label="Original ▶ 128×128"),
        gr.Image(type="numpy", label="Noisy (σ=0.1) ▶ 128×128"),
        gr.Image(type="numpy", label="Denoised ▶ 128×128")
    ],
    title="Denoising Autoencoder Demo",
    description=(
        "Upload any image (grayscale or color).\n"
        "- Internally resized to 64×64 for denoising.\n"
        "- Adds Gaussian noise (σ=0.1).\n"
        "- Displays all stages upsampled to 128×128 for clearer viewing."
    )
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=True)
