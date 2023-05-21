import os
import openai
#print(openai.Model.list())
messages = [
        {"role": "system", "content": "You are smart bot"}
    ]


async def add(messages, role, content) -> list:
    messages.append({"role": role, "content": content})
    return messages


async def clear_context() -> list:
    messages = [
        {"role": "system", "content": "You are smart bot"}
    ]
    return messages


async def update(message) -> str:
    await add(messages, "user", message.text)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer_gpt = response['choices'][0]['message']['content']
    await add(messages, "assistant", answer_gpt)
    print(messages)
    return answer_gpt