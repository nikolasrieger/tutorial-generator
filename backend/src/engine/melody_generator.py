from sounddevice import default, rec, wait
from wave import open
from os import remove
from subprocess import run, DEVNULL


class MelodyGenerator:
    def __init__(self, filename: str = "sonic_pi_script.rb"):
        self.fs = 44100
        self.duration = 3 + 1
        self.filename = filename
        default.device = (
            "PC-Lautsprecher (Realtek HD Audio output with SST), Windows WDM-KS"
        )

    def __save_melody(self):
        sonic_pi_script = """
        use_bpm 120
        start_time = Time.now

        live_loop :simple_melody do
        while (Time.now - start_time) < 2
            play :C4
            sleep 0.5
            play :E4
            sleep 0.5
            play :G4
            sleep 0.5
            play :B4
            sleep 0.5
            play :C5
            sleep 0.5
        end
        end
        """

        with open(self.filename, "w") as file:
            file.write(sonic_pi_script.strip())

    def record_audio(self, id: int):
        self.__save_melody()

        audio_data = rec(
            int(self.duration * self.fs), samplerate=self.fs, channels=2, dtype="int16"
        )

        run(["cmd.exe", "/c", f"type {self.filename} | sonic_pi4"], check=True)

        wait()

        with open("output.wav", "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(audio_data.tobytes())

        output_file = f"output_{id}.mp3"
        ffmpeg_command = [
            "./lib/ffmpeg/bin/ffmpeg",
            "-i",
            "output.wav",
            "-ss",
            "1",
            "-acodec",
            "mp3",
            output_file,
        ]

        run(ffmpeg_command, stdout=DEVNULL, stderr=DEVNULL, check=True)

        remove(self.filename)
        remove("output.wav")
