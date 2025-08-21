from flask import Flask, render_template, request
import os
import whisper

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the Whisper model once at startup
model = whisper.load_model("turbo")  # or "tiny", "small", "medium", "large", "turbo"

@app.route("/", methods=["GET", "POST"])
def home():
    translation = None
    audio_file = None
    print("Received GET request")
    if request.method == "POST":
        print("Received POST request")
        print(request.files)
        if "audio" not in request.files:
            return render_template("home.html", translation="No file part")
        file = request.files["audio"]
        if file.filename == "":
            return render_template("home.html", translation="No selected file")
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            audio_file = file.filename
            try:
                result = model.transcribe(filepath)
                translation = result["text"]
            except Exception as e:
                translation = f"Error: {str(e)}"
            # os.remove(filepath)
    return render_template("home.html", translation=translation, audio_filename=audio_file)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)