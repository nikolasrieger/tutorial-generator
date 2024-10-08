from lib.model import Model
from engine.config import OUTPUT_FORMAT


class ScriptWriter:
    def __init__(self, model: Model):
        self.model = model

    def generate_script(
        self,
        topic: str,
        context: str,
        tone: str,
        audience: str,
        length: int,
        prompt_template: str,
        language: str,
    ):
        prompt = (
            f"Topic: {topic}\n"
            f"Context: {context}\n"
            f"Tone: {tone}, Audience: {audience}, Length: {length}, Language: {language}\n\n"
            + prompt_template
        )

        script = self.model.generate(prompt)

        converted_script = self.model.generate(
            script + "\nLanguage:" + language + "\n" + OUTPUT_FORMAT, True
        )

        return converted_script
