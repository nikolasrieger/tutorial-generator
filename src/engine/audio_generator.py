from gtts import gTTS
from os import remove, path
from subprocess import run, CalledProcessError


class AudioGenerator:
    def __init__(self, lang: str = "en", slow: bool = False):
        self.lang = lang
        self.slow = slow

    def generate_audio(self, text: str, file_name: str = "output.mp3"):
        try:
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)
            tts.save(file_name)

        except Exception as e:
            print(f"An error occurred while generating audio: {e}")

    def merge_audio(self, files: list, output_file: str = "merged_audio.mp3"):
        try:
            with open("file_list.txt", "w") as f:
                for file_name in files:
                    f.write(f"file '{file_name}'\n")

            ffmpeg_command = [
                "./lib/ffmpeg/bin/ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                "file_list.txt",
                "-c",
                "copy",
                output_file,
            ]

            run(ffmpeg_command, check=True)

            self.__delete_files(files)
            remove("file_list.txt")

        except CalledProcessError as e:
            print(f"An error occurred while merging audio files: {e}")

    def __delete_files(self, files: list):
        try:
            for file_name in files:
                if path.exists(file_name):
                    remove(file_name)

        except Exception as e:
            print(f"An error occurred while deleting files: {e}")
