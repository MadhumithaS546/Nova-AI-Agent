from google import genai
from dotenv import load_dotenv
import os

from tools.calculator import calculate
from tools.file_reader import read_file
from tools.file_search import search_file
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MEMORY_FILE = "memory.txt"


# Read memory
def read_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return file.read()
    return ""


# Save memory
def save_memory(text):
    with open(MEMORY_FILE, "w") as file:
        file.write(text)


memory = read_memory()

print("Nova is ready!")

if memory.strip():
    print(f"Welcome back! I remember: {memory}")
else:
    print("I don't know anything about you yet.")

while True:
    question = input("\nYou: ")

    # Exit
    if question.lower() == "exit":
        print("Nova: Goodbye!")
        break

    # Save name
    if question.lower().startswith("my name is"):
        name = question[10:].strip()
        save_memory(f"Your name is {name}.")
        memory = read_memory()
        print(f"Nova: Nice to meet you, {name}! I'll remember that.")
        continue

    # Calculator
    if question.lower().startswith("calculate "):
        expression = question[10:]
        print("\nNova:", calculate(expression))
        continue

    # Read file
    if question.lower().startswith("read "):
        filename = question[5:]
        print("\nNova:")
        print(read_file(filename))
        continue

    # Find file
    if question.lower().startswith("find "):
        keyword = question[5:]
        print("\nNova:")
        print(search_file(keyword))
        continue

    # Gemini handles everything else
    prompt = f"""
Memory:
{memory}

User:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    print("\nNova:", response.text)