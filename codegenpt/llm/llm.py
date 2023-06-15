from json import JSONDecodeError
import os
import openai
from demjson3 import decode

def askLLM(messages, json=False, retries=3):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if messages is str:
        messages = [{ 
            "role": "user",
            "content": messages
        }]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
    )

    response = completion.choices[0].message.content

    if json:
        try:
            response = decode(response)
        except JSONDecodeError:
            if retries == 0:
                raise JSONDecodeError
            return askLLM(messages, json, retries - 1)

    return response
