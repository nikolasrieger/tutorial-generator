from dotenv import load_dotenv
from os import getenv
from model import Model
from scriptwriter import ScriptWriter
from extractor import Extractor

# TODO: Prompt improvement
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
    for _, result in enumerate(results):
        texts += result + "\n"

    script_writer = ScriptWriter(model)
    print(script_writer.generate_script("KAN", texts))
