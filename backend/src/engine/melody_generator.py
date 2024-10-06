from sounddevice import default, rec, wait
from wave import open as open_wave
from os import remove
from subprocess import run, DEVNULL
from lib.model import Model


class MelodyGenerator:
    def __init__(self, model: Model, filename: str = "sonic_pi_script.rb"):
        self.fs = 44100
        self.filename = filename
        self.model = model
        default.device = (
            "PC-Lautsprecher (Realtek HD Audio output with SST), Windows WDM-KS"
        )

    def __save_melody(self, theme: str, length: int):
        sonic_pi_script = self.model.generate(
            f"Generate a sonic pi script with this theme: {theme} lasting approximately {length} seconds. Return only the script."
            f"Use ambient music, samples and synthesizers if possible. Be as creative as possible."
        )
        sonic_pi_script = "\n".join(sonic_pi_script.split("\n")[1:-1])

        with open(self.filename, "w") as file:
            file.write(sonic_pi_script.strip())

    def record_audio(self, id: int, theme: str, length: int = 3):
        self.__save_melody(theme, length)
        duration = length + 1

        audio_data = rec(
            int(duration * self.fs), samplerate=self.fs, channels=2, dtype="int16"
        )

        run(["cmd.exe", "/c", f"type {self.filename} | sonic_pi4"], check=True)

        wait()

        with open_wave("output.wav", "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(audio_data.tobytes())

        output_file = f"output_{id}.mp3"
        ffmpeg_command = [
            "./lib/ffmpeg/bin/ffmpeg",
            "-i",
            "output.wav",
            "-af",
            "silenceremove=start_periods=1:start_duration=0:start_threshold=0.02",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "192k",
            output_file,
        ]

        run(ffmpeg_command, stdout=DEVNULL, stderr=DEVNULL, check=True)

        remove(self.filename)
        remove("output.wav")
