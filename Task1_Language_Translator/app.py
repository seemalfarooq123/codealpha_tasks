from flask import Flask, render_template, request
from googletrans import Translator
import webbrowser
import threading
from gtts import gTTS

app = Flask(__name__)
translator = Translator()

@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = ""

    if request.method == "POST":
        text = request.form["text"]
        source = request.form["source"]
        target = request.form["target"]

        translated = translator.translate(text, src=source, dest=target)
        translated_text = translated.text

        tts = gTTS(translated_text, lang=target)
        tts.save("static/output.mp3")

    return render_template("index.html", translated_text=translated_text)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)