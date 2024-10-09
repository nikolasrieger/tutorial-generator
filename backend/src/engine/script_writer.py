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
        improved_context = self.improve_context(context)
        prompt = (
            f"Topic: {topic}\n"
            f"Context: {improved_context}\n"
            f"Tone: {tone}, Audience: {audience}, Length: {length}, Language: {language}\n\n"
            + prompt_template
        )

        script = self.model.generate(prompt)

        converted_script = self.model.generate(
            script + "\nLanguage:" + language + "\n" + OUTPUT_FORMAT, True
        )

        return converted_script

    def improve_context(self, context: str):
        improved_context = self.model.generate(
            f"Here is the given context: {context}\n"
            f"Please enhance this context by expanding on key points, adding more details, and organizing it in a structured manner. "
            f"Include possible subtopics, key points, and questions that a tutorial on this topic should address, think about possible learning goals. "
            f"Provide clear answers to the questions and ensure the entire explanation follows a logical, well-structured flow. "
            f"Do not leave any details out, rather add additional information to make the context more informative and engaging. "
            f"Return only the improved context."
        )

        return improved_context
