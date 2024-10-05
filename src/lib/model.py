from google.generativeai import configure, GenerativeModel, GenerationConfig


class Model:
    def __init__(self, api_key: str):
        configure(api_key=api_key)
        self.__model = GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt: str, json_output: bool = False):
        if json_output:
            config = GenerationConfig(response_mime_type="application/json")
        else:
            config = GenerationConfig()
        res = self.__model.generate_content(prompt, generation_config=config)
        return res.text
