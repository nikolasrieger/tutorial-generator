import fitz
import requests
from bs4 import BeautifulSoup
from typing import List, Union


class Extractor:
    def __init__(self, pdf_filenames: List[str] = None, urls: List[str] = None):
        self.pdf_filenames = pdf_filenames if pdf_filenames else []
        self.urls = urls if urls else []

    def extract_text_from_pdf(self, pdf_filename: str):
        text = ""
        try:
            with fitz.open(pdf_filename) as pdf_document:
                for page in pdf_document:
                    text += page.get_text()
        except Exception as e:
            print(f"Error reading {pdf_filename}: {e}")
        return text

    def extract_text_from_url(self, url: str):
        text = ""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all(["p", "h1", "h2", "h3", "li"])
            text = "\n".join(paragraph.get_text() for paragraph in paragraphs)
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
        return text

    def extract_text(self) -> List[Union[str, List[str]]]:
        extracted_texts = []

        for pdf_filename in self.pdf_filenames:
            text = self.extract_text_from_pdf(pdf_filename)
            extracted_texts.append(text)

        for url in self.urls:
            text = self.extract_text_from_url(url)
            extracted_texts.append(text)

        return extracted_texts
