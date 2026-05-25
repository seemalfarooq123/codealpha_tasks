from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import string
import webbrowser
import threading

nltk.download('punkt')

app = Flask(__name__)

questions = [
    "What is your name?",
    "How are you?",
    "What is AI?",
    "What is your purpose?",
    "Who created you?"
]

answers = [
    "I am a chatbot created for CodeAlpha internship.",
    "I am fine, thank you!",
    "AI stands for Artificial Intelligence.",
    "My purpose is to answer your questions.",
    "I was created by Seemal Farooq."
]

def preprocess(text):
    text = text.lower()
    text = "".join([c for c in text if c not in string.punctuation])
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""

    if request.method == "POST":
        user_input = preprocess(request.form["message"])

        processed_questions = [preprocess(q) for q in questions]

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(processed_questions + [user_input])

        similarity = cosine_similarity(vectors[-1], vectors[:-1])
        best_match = similarity.argmax()

        if similarity[0][best_match] > 0.3:
            response = answers[best_match]
        else:
            response = "Sorry, I don't understand."

    return render_template("index.html", response=response)

if __name__ == "__main__":
    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True)