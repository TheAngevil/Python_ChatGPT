from module.chatGPT_helper import ChatGTPAPI
from pathlib import Path
from openai import _types


class AudioTranscriptor(ChatGTPAPI):
    """
    A class to handle the transcription of audio files using the OpenAI Whisper API.

    This class provides methods to transcribe an audio file and save the transcription to an output file.

    :param audio_file_path: The path to the audio file to be transcribed.
    :type audio_file_path: str or pathlib.Path
    :param language: The language of the audio file. Defaults to an empty string, which will use the API's language detection.
    :type language: str, optional
    """

    def __init__(self, audio_file_path: str | Path, language=''):
        """
        Initializes the AudioTranscriptor class with the audio file and language.

        :param audio_file_path: The path to the audio file to be transcribed.
        :type audio_file_path: str or pathlib.Path
        :param language: The language of the audio file. Defaults to an empty string, which will use the API's language detection.
        :type language: str, optional
        """
        super().__init__()
        self.audio_file = open(Path(audio_file_path).resolve(), "rb")
        self.language = language

    def transcription(self):
        """
        Transcribes the audio file using the OpenAI Whisper API.

        :return: The transcription result from the API.
        :rtype: Transcription object
        """
        return self.client.audio.transcriptions.create(
            model="whisper-1",
            file=self.audio_file,
            timestamp_granularities='segment',
            language=self.language or _types.NotGiven
        )

    def transcription_output(self, output_file_path: str | Path) -> bool:
        """
        Saves the transcription output to a file.

        This method transcribes the audio file and writes the resulting text to the specified output file.

        :param output_file_path: The path where the transcription output will be saved.
        :type output_file_path: str or pathlib.Path
        :return: True if the transcription is successfully written to the file, False otherwise.
        :rtype: bool
        """
        try:
            Path(output_file_path).resolve().parent.mkdir(parents=True, exist_ok=True)
            with open(output_file_path, "w") as result_file:
                result_file.write(self.transcription().text) # https://platform.openai.com/docs/api-reference/audio/createTranscription
            return True
        except FileExistsError:
            print(f"File already exists: {Path(output_file_path).resolve()}")
            return False
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    current_working_dir = Path.cwd()
    AudioTranscriptor(audio_file_path=Path.cwd().joinpath('CNC_Test.mp4'),
                      language='zh'
                      ).transcription_output(Path.cwd().joinpath('modified_result.txt'))
