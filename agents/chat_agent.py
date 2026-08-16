from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_reply(messages, system_prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            *messages
        ]
    )

    return response.choices[0].message.content
def generate_title(first_message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Create a very short chat title (3-5 words). "
                    "Return only the title."
                )
            },
            {
                "role": "user",
                "content": first_message
            }
        ]
    )

    return response.choices[0].message.content.strip()