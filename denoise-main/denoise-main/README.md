# Denoising Autoencoder Project

## Overview
This project demonstrates the training and deployment of a denoising autoencoder on 100 grayscale images (64×64). It includes:
- A **Jupyter notebook** for model development, evaluation, and analysis.  
- A **Gradio web application** for interactive denoising.

## Links
- **Colab Notebook:** [Open in Google Colab](https://colab.research.google.com/drive/1RQAEGP4WZEIUxHyyw-8mgFmq6UF-DWXe?usp=sharing)  
- **Gradio App (Hugging Face Space):** [Try it here](https://huggingface.co/spaces/isana25/denoise)

## What It Does

### 1. Jupyter Notebook
- **Data Preparation:**  
  - Fetches the Olivetti Faces dataset (400 × 64×64 grayscale images).  
  - Randomly samples 100 images, splits into 80% train / 20% test.  
  - Adds Gaussian noise (σ=0.1) to both sets.  
- **Model Definition:**  
  - Builds a Residual U-Net autoencoder with skip-connections and residual blocks.  
- **Training:**  
  - Trains with MSE loss, using EarlyStopping and ModelCheckpoint to save `best_model.h5`.  
- **Evaluation:**  
  - Computes Mean Squared Error (MSE) on train and test sets.  
  - Plots training vs. validation loss curves.  
  - Visualizes side-by-side comparisons of noisy, reconstructed, and original images.  
- **Analysis:**  
  - Discusses reconstruction errors, loss curves, and visual results to assess generalization.

### 2. Gradio Web App
- **Interactive Interface:**  
  - Upload any image (grayscale or color).  
  - Displays three outputs:  
    1. **Original** (resized to 128×128 for display)  
    2. **Noisy** (Gaussian-corrupted, σ=0.1)  
    3. **Reconstructed** (denoised by the autoencoder)  
- **Deployment:**  
  - Simple `app.py` script and `requirements.txt` file enable one-step launch and public sharing.

## Model & Tech Stack
- **Model:**  
  - Denoising autoencoder based on a Residual U-Net backbone.  
- **Libraries & Frameworks:**  
  - **TensorFlow / Keras** for model building and training  
  - **scikit-learn** for dataset loading  
  - **OpenCV** for image processing  
  - **NumPy** & **Pandas** for data handling and metrics  
  - **Matplotlib** for plotting loss curves and examples  
  - **Gradio** for the interactive web interface  

## Analysis & Observations
- **Noise Removal:** The model cleans up most of the noise while keeping faces recognizable and clear.  
- **Consistent Performance:** Training and test errors are both low and nearly the same, which tells us the model learned useful patterns and works well on new images.  
- **Smooth Learning Curve:** The loss steadily went down during training without large jumps or gaps, so it didn’t overfit or underfit.  
- **Visual Quality:** Reconstructed images look sharp in general, although very fine details can appear slightly blurred. Trying different loss functions (like SSIM) might help bring back those tiny details.

**Conclusion:**  
The Residual U-Net autoencoder exhibits strong denoising performance and generalization. Future enhancements could include multi-noise conditioning, alternative loss functions, or extension to color images and higher resolutions.
