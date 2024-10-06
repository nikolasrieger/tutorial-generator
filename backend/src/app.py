from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from json import loads
from lib.model import Model
from engine.script_writer import ScriptWriter
from engine.extractor import Extractor
from engine.audio_generator import AudioGenerator
from engine.melody_generator import MelodyGenerator
from base64 import b64encode
from time import time

# TODO: Automatic Prompt improvement
# TODO: Generate video
# TODO: Different people, different voices, customize, length, difficulty ...
# TODO: Use Images from pages
# TODO: upload pdfs


app = Flask(__name__)
CORS(app)

load_dotenv()
API_KEY = getenv("GEMINI_API_KEY")
model = Model(api_key=API_KEY)
melody_generator = MelodyGenerator(model)


@app.route("/process", methods=["POST"])
def process_content():
    urls = request.form.getlist("urls")
    urls = urls[0].split(",")
    pdf_files = request.form.getlist("pdf_files")
    topic = request.form.get("topic")
    target_audience = request.form.get("targetAudience", "general audience")
    tone = request.form.get("tone", "informative")
    length = int(request.form.get("length", 5))

    if not urls and not pdf_files:
        return jsonify({"error": "No URLs or PDF files provided"}), 400

    extractor = Extractor(pdf_filenames=pdf_files, urls=urls)
    results = extractor.extract_text()

    print(results, urls)

    texts = ""
    for result in results:
        texts += result + "\n"

    script_writer = ScriptWriter(model)
    script = script_writer.generate_script(topic, texts, tone, target_audience, length)
    script = loads(script)

    audio_files = []
    audio_generator = AudioGenerator()

    for idx, element in enumerate(script):
        print(idx, len(script))
        if element["tag"] == "speech":
            file_name = f"output_{idx}.mp3"
            audio_generator.generate_audio(element["text"], file_name)
            audio_files.append(file_name)
        elif element["tag"] == "music":
            melody_generator.record_audio(idx, element["text"], element["duration"])
            audio_files.append(f"output_{idx}.mp3")

    output_filename = f"output_{int(time())}.mp3"
    audio_generator.merge_audio(audio_files, output_filename)

    with open(output_filename, "rb") as audio_file:
        audio_base64 = b64encode(audio_file.read()).decode("utf-8")

    return jsonify({"audio_file": audio_base64})


if __name__ == "__main__":
    app.run(debug=True)
