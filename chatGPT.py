from openai import OpenAI
import json
from pathlib import Path


class ChatGTPAPI:

    def __init__(self, system_content: str, user_content: str, key_file_path= Path("secrets.json").resolve()):
        secret = json.load(open(Path(key_file_path).resolve()))
        self._client = OpenAI(api_key=secret["open_ai_api_key"])
        self._model = "gpt-4o"
        self._messages = [{"role": "system",
                           "content": f"{system_content}, Provide just the result without any additional comment or expression, while provide Chinese, use traditional chiness style"},
                          # 預設前置條件 可以設
                          {"role": "user", "content": f"請翻譯以下文字: {user_content}"}
                          ]

    @property
    def client(self):
        return self._client

    @property
    def answer(self):
        return self.client.chat.completions.create(
            model=self._model,
            messages=self._messages  # 預設前置條件 可以設
        ).choices[0].message.content


alive = True

while alive:
    try:
        chat_initial = input("What do you want me to be? ")
        if chat_initial == "stop":
            raise TypeError
        while alive:
            try:
                question = input("What you like to do? ")
                if question == "stop" or question == "exit":
                    raise TypeError
                print(ChatGTPAPI(chat_initial, question).answer)
            except BaseException:
                alive = False
                break
    except BaseException:
        alive = False
        break
    break
