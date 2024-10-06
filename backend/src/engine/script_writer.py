from lib.model import Model

OUTPUT_FORMAT = """
The podcast name is "Teachify".
Return a JSON object List[Element] with the following structure:
Element {
    "tag": str,
    "text": str,
    "duration": int
}
There a two tags available: "music" and "speech". If you choose "music", the text field should be a description of the music and duration the length of the music.
If you choose "speech", the text field should be the text of the speech.
"""

template = """
Draft a structured script for a tutorial on above topic and keep all the specific instructions in mind.\n
Add the above context to the script, put in the informations, do not leave gaps and make sure to maintain the tone and target audience.\n
Structure the script with sections such as:\n
- Introduction (greet the listeners, introduce the topic)\n
- Body (break down the topic into parts, explain in detail)\n
- Conclusion (summarize, provide next steps, thank the listeners)\n
Add speaker cues and timestamps if appropriate.
"""


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
        prompt_template: str = template
    ):
        prompt = (
            f"The topic: {topic}\n"
            f"Context: {context}\n"
            f"Tone: {tone}, Audience: {audience}, Length: {length}\n\n" +
            prompt_template
        )

        script = self.model.generate(prompt)

        converted_script = self.model.generate(script + "\n" + OUTPUT_FORMAT, True)

        return converted_script
