from model import Model 

OUTPUT_FORMAT = """
The podcast name is "Teachify".
Return a JSON object List[Element] with the following structure:
Element {
    "tag": str,
    "text": str}
There a two tags available: "music" and "speech". If you choose "music", the text field should be a description of the music.
If you choose "speech", the text field should be the text of the speech.
"""

class ScriptWriter:
    def __init__(self, model: Model):
        self.model = model
    
    def generate_script(self, topic: str, context: str = "", tone: str = "informative", audience: str = "general audience"):
        prompt = (f"Draft a structured script for a tutorial on the topic: '{topic}'.\n"
                  f"The podcast should be designed for {audience} and should have a {tone} tone.\n"
                  f"Include the following context: {context}\n\n"
                  f"Structure the script with sections such as:\n"
                  f"- Introduction (greet the listeners, introduce the topic)\n"
                  f"- Body (break down the topic into parts, explain in detail)\n"
                  f"- Conclusion (summarize, provide next steps, thank the listeners)\n"
                  f"Add speaker cues and timestamps if appropriate.")
        
        script = self.model.generate(prompt)

        converted_script = self.model.generate(script + "\n" + OUTPUT_FORMAT)

        return converted_script