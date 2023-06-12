import os
import openai

def askLLM(messages, retries = 3):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if messages is str:
        messages = [{ 
            "role": "user",
            "content": messages
        }]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    response = completion.choices[0].message.content

    return response
