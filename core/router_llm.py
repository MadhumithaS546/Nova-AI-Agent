from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_route(prompt, has_pdf=False):
    routing_prompt = f"""
You are Nova's routing brain.

Choose ONLY ONE of these words:

memory
pdf
web
tool
chat

Rules:
- memory → questions about stored user information.
- pdf → questions about an uploaded document.
- web → current or latest information.
- tool → calculations or file operations.
- chat → everything else.

User:
{prompt}

PDF available: {has_pdf}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Reply with exactly one routing word."},
            {"role": "user", "content": routing_prompt}
        ]
    )

    return response.choices[0].message.content.strip().lower()