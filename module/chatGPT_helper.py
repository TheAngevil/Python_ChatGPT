from openai import OpenAI
import json
from pathlib import Path


class ChatGTPAPI:
    """
    This class is designed to interact with the OpenAI API using a pre-configured client and model.
    It initializes the client with an API key stored in a specified JSON file and sets up the initial messages
    for the system and user roles.

    Attributes:
        _client (OpenAI): An instance of the OpenAI client initialized with the provided API key.
        _model (str): The model name to be used for the OpenAI API requests, default is 'gpt-4o'.
        _messages (list): A list of dictionaries containing the initial system and user messages.

    Parameters:
        system_content (str): Content for the system message role. Defaults to an empty string.
        user_content (str): Content for the user message role. Defaults to an empty string.
        key_file_path (Path): The path to the JSON file containing the API key. Defaults to "secrets.json"
                              in the current directory.

    Usage:
        This class is intended to be used as a base for sending prompts to the OpenAI API and receiving
        responses. The system and user messages can be customized at initialization, and the client
        will automatically load the necessary API key from the specified file.
    """

    def __init__(self, system_content: str = "", user_content: str = "", key_file_path=Path("secrets.json").resolve()):
        """


        Initialize the ChatGTPAPI instance.

        This constructor initializes the OpenAI API client with a specified API key and sets up the
        initial system and user messages. The API key is loaded from a JSON file, and the initial
        conversation context is configured based on the provided system and user content.

        :param system_content:
            The content for the system role in the conversation. This parameter defines the behavior
            and guidelines for the AI's responses. Default empty string. Learn more: https://platform.openai.com/docs/guides/prompt-engineering
        :type system_content: str, optional

        :param user_content:
            The content for the user role in the conversation. This is the main prompt or input from
            the user that the AI will respond to. Defaults to an empty string. Learn more: https://platform.openai.com/docs/guides/prompt-engineering
        :type user_content: str, optional

        :param key_file_path:
            The file path to the JSON file containing the OpenAI API key. The default path is
            "secrets.json" in the current directory. This path is resolved to an absolute path.
        :type key_file_path: pathlib.Path, optional

        :raises FileNotFoundError:
            If the JSON file containing the API key is not found at the specified path.

        :raises json.JSONDecodeError:
            If the JSON file is not formatted correctly or the API key cannot be retrieved.

        :raises KeyError:
            If the API key is not found in the JSON file.

        :return:
            Initializes the ChatGTPAPI object with the specified system and user content,
            and sets up the OpenAI client for future interactions.
        :rtype: None
        """
        secret = json.load(open(Path(key_file_path).resolve()))
        self._client = OpenAI(api_key=secret["open_ai_api_key"])
        self._model = "gpt-4o"
        self._messages = [{
            "role": "system",
            "content": f"{system_content}"
        },
            {
                "role": "user",
                "content": f"{user_content}"
            }]

    @property
    def client(self):
        return self._client

    @property
    def answer(self):
        return self.client.chat.completions.create(
            model=self._model,
            messages=self._messages
        ).choices[0].message.content

    @property
    def audio(self):
        return self.client.audio

    @classmethod
    def initial_conversation(cls):
        alive = True
        while alive:
            try:
                print("What do you want me to be?")
                chat_initial = input()
                if chat_initial in ["stop", 'exit']:
                    break
                while alive:
                    print("How can I help?")
                    ask = input()
                    if ask in ["stop", 'exit']:
                        break
                    print(cls(chat_initial, ask).answer)
            except BaseException:
                break
            break


if __name__ == "__main__":
    ChatGTPAPI().initial_conversation()
