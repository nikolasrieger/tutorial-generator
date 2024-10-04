from google.generativeai import configure, GenerativeModel


class Model:
    def __init__(self, api_key: str):
        configure(api_key=api_key)
        self.__model = GenerativeModel("gemini-1.5-flash")

    def generate(self, prompt: str):
        res = self.__model.generate_content(prompt)
        return res.text
