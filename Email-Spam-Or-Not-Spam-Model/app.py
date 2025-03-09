import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import streamlit as st

# Load and preprocess dataset
@st.cache_resource
def load_and_preprocess_data(file_path):
    # Load dataset
    df = pd.read_csv(file_path, sep='\t', header=None, names=['label', 'email'])
    # Encode labels
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    # Extract features and labels
    X = df['email']
    y = df['label']
    # Convert text to TF-IDF features
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X = vectorizer.fit_transform(X)
    return X, y, vectorizer

# Train the model
@st.cache_resource
def train_model(_X, y):  # Rename 'X' to '_X' to bypass Streamlit caching hash issues
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(_X, y, test_size=0.2, random_state=42)
    # Train a MultinomialNB model
    model = MultinomialNB()
    model.fit(X_train, y_train)
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, accuracy

# Streamlit app interface
st.title("Email Spam Classifier: Spam vs. Not Spam")
st.write("This app allows you to classify emails as spam or not spam.")

# Load and preprocess data
X, y, vectorizer = load_and_preprocess_data('/content/SMSSpamCollection')
model, accuracy = train_model(X, y)

st.write(f"Model Training Accuracy: {accuracy:.2f}")

# Input email text for classification
email_text = st.text_area("Enter the email text below:")

if st.button("Classify Email"):
    if email_text.strip():
        # Transform input email to TF-IDF vector
        input_vector = vectorizer.transform([email_text])
        # Predict using trained model
        prediction = model.predict(input_vector)
        result = "Spam" if prediction[0] == 1 else "Not Spam"
        st.write(f"**Prediction:** {result}")
    else:
        st.write("Please enter some text for classification.")
