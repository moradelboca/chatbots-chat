from openai import OpenAI


def chat_init(context):
    # Env variable name must be OPENAI_API_KEY
    global client
    global messages
    client = OpenAI()
    messages = [{"role": "system", "content": context}]


def send_message(message):
    global messages
    global client
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=1000,
        top_p=1.0
    )
    response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    return response
