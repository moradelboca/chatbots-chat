import google.generativeai as genai
from dotenv import load_dotenv
import os
import time


def chat_init(context):
    global chat_session
    load_dotenv()
    API_KEY = os.environ['GEMINI_API_KEY']
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=context,
        generation_config={
            "temperature": 1,
            "top_p": 1.0,
            "top_k": 64,
            "max_output_tokens": 1000,
            "response_mime_type": "text/plain"
        }
    )
    chat_session = model.start_chat(history=[])


def send_message(message):
    global chat_session
    response = chat_session.send_message(message)
    # 30 seconds delay to avoid rate limiting in free google api
    time.sleep(30)
    return response.text
