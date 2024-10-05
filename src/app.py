from dotenv import load_dotenv
from os import getenv
from json import loads
from lib.model import Model
from engine.script_writer import ScriptWriter
from engine.extractor import Extractor
from engine.audio_generator import AudioGenerator

# TODO: Automatic Prompt improvement
# TODO: Add frontend
# TODO: Generate video
# TODO: Use Images from page
# TODO: Get music


if __name__ == "__main__":
    load_dotenv()
    API_KEY = getenv("GEMINI_API_KEY")
    model = Model(api_key=API_KEY)

    pdf_files = []
    urls = ["https://kindxiaoming.github.io/pykan/intro.html"]

    extractor = Extractor(pdf_filenames=pdf_files, urls=urls)
    results = extractor.extract_text()

    texts = ""
    for result in results:
        texts += result + "\n"

    script_writer = ScriptWriter(model)
    script = script_writer.generate_script("KAN", texts)
    print(script)
    script = loads(script)

    audio_files = []
    audio = AudioGenerator()
    for idx, element in enumerate(script):
        if element["tag"] == "speech":
            file_name = f"output_{idx}.mp3"
            audio.generate_audio(element["text"], file_name)

            audio_files.append(file_name)

    audio.merge_audio(audio_files, "output.mp3")
