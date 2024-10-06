from lib.model import Model

OUTPUT_FORMAT = """
Return a JSON array List[Element] with the following structure:
Element {
    "tag": str,   
    "text": str, 
    "duration": int
}
Tags:
"music": The text field should contain a description of the music, and the duration should reflect the length of the music in seconds.
"speech": The text field should contain the text of the speech segment.
Make sure the speech content aligns with the podcast name, "Teachify.", do not leave anything of the following content out: 
"""

PROMPT_TEMPLATE = """
Draft a structured, detailed script for a tutorial on the specified topic, adhering to all the provided instructions and including the provided context.
The script should include well-researched information without any content gaps, following the tone and target audience as specified. Ensure the tutorial covers the topic in depth and does not just explain how to structure it.
The script should be clearly organized with the following sections:
- Introduction: Greet the audience and introduce the topic.
- Body: Break down the topic into smaller parts, explaining each in detail.
- Conclusion: Summarize the key points, suggest next steps, and thank the listeners.
Additionally, incorporate speaker cues, timestamps (if applicable), and maintain a clear, professional, and engaging flow.
Add some engaging music to the script to enhance the listener's experience.
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
