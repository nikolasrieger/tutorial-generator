from model import Model 
from dotenv import load_dotenv
from os import getenv

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

        return self.model.generate(prompt)


if __name__ == "__main__":
    load_dotenv()
    API_KEY = getenv("GEMINI_API_KEY")
    model = Model(api_key=API_KEY)
    script_writer = ScriptWriter(model)
    print(
        script_writer.generate_script("The future of AI", "In the future, AI will be used to solve complex problems in healthcare, finance, and other industries.")
    )