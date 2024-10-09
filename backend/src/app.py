from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv, path, remove
from json import loads
from lib.model import Model
from engine.script_writer import ScriptWriter
from engine.extractor import Extractor
from engine.audio_generator import AudioGenerator
from engine.melody_generator import MelodyGenerator
from engine.config import THRESHOLD_BAD_PROMPTS, INITIAL_PROMPT_TEMPLATE
from base64 import b64encode, b64decode
from time import time
from models import db, Prompt, Feedback
from numpy.random import choice


app = Flask(__name__)
CORS(app)

load_dotenv()
API_KEY = getenv("GEMINI_API_KEY")
model = Model(api_key=API_KEY)
melody_generator = MelodyGenerator(model)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_feedback.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    prompt_id = request.json["prompt_id"]
    feedback_type = request.json["feedback_type"]
    comment = request.json.get("comment", None)

    prompt = Prompt.query.get(prompt_id)
    if not prompt:
        return jsonify({"message": "Internal Server Error"}), 500

    if feedback_type == "like":
        prompt.likes += 1
    elif feedback_type == "dislike":
        prompt.dislikes += 1
    else:
        return jsonify({"message": "Internal Server Error"}), 500

    if comment:
        new_feedback = Feedback(
            prompt_id=prompt_id, feedback_type=feedback_type, comment=comment
        )
        db.session.add(new_feedback)

        prompts = get_prompts()
        prompt_text = ""
        for prompt in prompts:
            if prompt.id == prompt_id:
                prompt_text = prompt.prompt_text

        new_prompt = model.generate(
            f"Generate a new, improved prompt based on the feedback: {comment}\nThis is the old prompt: {prompt_text}"
            f"Do not change the general purpose of the prompt, but improve it as you like. Return only the prompt."
        )

        add_prompt(new_prompt)

    db.session.commit()

    return jsonify({"message": "Successful"}), 201


@app.route("/process", methods=["POST"])
def process_content():
    urls = request.form.getlist("urls")
    urls = urls[0].split(",") if urls else []

    pdf_files_base64 = request.form.getlist("pdf_files")

    pdf_filenames = []
    if pdf_files_base64:
        for idx, pdf_base64 in enumerate(pdf_files_base64):
            try:
                pdf_content = b64decode(pdf_base64)

                file_name = f"temp_pdf_{idx}.pdf"
                temp_pdf = open(f"temp_pdf_{idx}.pdf", "wb")
                temp_pdf.write(pdf_content)
                temp_pdf.close()

                pdf_filenames.append(file_name)
            except Exception:
                return jsonify({"error": "Internal Server Error"}), 500

    topic = request.form.get("topic")
    target_audience = request.form.get("target_audience", "general audience")
    tone = request.form.get("tone", "informative")
    language = request.form.get("language", "en")
    length = int(request.form.get("length", 5))

    if not urls and not pdf_filenames:
        return jsonify({"message": "Internal Server Error"}), 500

    extractor = Extractor(pdf_filenames=pdf_filenames, urls=urls)
    results = extractor.extract_text()

    texts = "\n".join(results)

    script_writer = ScriptWriter(model)
    prompt = get_prompt()

    script = script_writer.generate_script(
        topic, texts, tone, target_audience, length, prompt.prompt_text, language
    )
    script = loads(script)

    audio_files = []
    audio_generator = AudioGenerator(language)

    for idx, element in enumerate(script):
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

    for pdf_file in pdf_filenames:
        if path.exists(pdf_file):
            remove(pdf_file)

    return jsonify({"audio_file": audio_base64, "prompt_id": prompt.id})


@app.teardown_appcontext
def teardown(exception=None):
    cleanup_bad_prompts()
    prompts = get_prompts()
    if len(prompts) == 0: 
        return

    prompt_list = []
    for prompt in prompts:
        prompt_text = {"text": prompt.prompt_text, "likes": prompt.likes, "dislikes": prompt.dislikes}
        prompt_list.append(prompt_text)

    new_prompt = model.generate(
        f"Generate a new, improved prompt based on the feedback: {prompt_list}"
        f"Do not change the general purpose of the prompt, but improve it as you like. Return only the prompt text."
    )
    add_prompt(new_prompt)


def get_prompts():
    return Prompt.query.all()


def get_prompt():
    prompts = get_prompts()

    prompt_data = []
    for prompt in prompts:
        likes = prompt.likes
        dislikes = max(1, prompt.dislikes)
        ratio = likes / dislikes

        score = likes + ratio
        prompt_data.append({"prompt": prompt, "score": score})

    total_score = sum([p["score"] for p in prompt_data])
    if total_score == 0:
        for data in prompt_data:
            data["probability"] = 1 / len(prompt_data)
    else:
        for data in prompt_data:
            data["probability"] = data["score"] / total_score

    if not prompt_data:
        add_prompt(INITIAL_PROMPT_TEMPLATE)
        prompt_data = [{"prompt": Prompt.query.first(), "probability": 1.0}]

    prompts = [p["prompt"] for p in prompt_data]
    probabilities = [p["probability"] for p in prompt_data]

    selected_prompt = choice(prompts, 1, p=probabilities)[0]
    return selected_prompt


def add_prompt(prompt_text: str):
    new_prompt = Prompt(prompt_text=prompt_text)
    db.session.add(new_prompt)
    db.session.commit()


def cleanup_bad_prompts():
    prompts_to_delete = Prompt.query.filter(
        Prompt.dislikes > THRESHOLD_BAD_PROMPTS
    ).all()

    if prompts_to_delete:
        for prompt in prompts_to_delete:
            db.session.delete(prompt)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
