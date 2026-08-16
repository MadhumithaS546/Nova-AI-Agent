from groq import Groq
from dotenv import load_dotenv
import os
import json
from tools.file_search import search_file
from tools.pdf_reader import read_pdf

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MEMORY_FILE = "memory.json"

def read_memory():
    default_memory = {
        "name": "",
        "city": "",
        "college": "",
        "favorite_language": "",
        "facts": []
    }

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            memory = json.load(file)

        for key, value in default_memory.items():
            memory.setdefault(key, value)

        return memory

    except:
        return default_memory


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)



memory = read_memory()

print("Nova is ready!")

if memory["name"]:
    print(f"Welcome back, {memory['name']}!")
else:
    print("I don't know anything about you yet.")

def update_memory(question):
    q = question.lower().strip()

    if q.startswith("my name is "):
        memory["name"] = question[11:].strip()

    elif q.startswith("i am from "):
        memory["city"] = question[10:].strip()

    elif q.startswith("i study at "):
        memory["college"] = question[11:].strip()

    elif q.startswith("my favorite language is ") or q.startswith("my favourite language is "):
        memory["favorite_language"] = question.split("is", 1)[1].strip()

    elif q.startswith("i am "):
        name = question[5:].strip()
        if len(name.split()) <= 3:      # Avoid saving sentences like "I am tired"
            memory["name"] = name

    elif q.startswith("remember "):
        memory["facts"].append(question[9:].strip())

    save_memory(memory)
    save_memory(memory)

while True:
    question = input("\nYou: ")
    update_memory(question)
    # Exit

    if question.lower() == "exit":
        print("Nova: Goodbye!")
        break

    if question.lower() == "what is my name?":
        print(f"Nova: Your name is {memory.get('name','unknown')}.")
        continue

    if question.lower() == "where am i from?":
        print(f"Nova: You're from {memory.get('city','an unknown place')}.")
        continue

    if question.lower() in ["what is my favorite language?", "what is my favourite language?"]:
        print(f"Nova: Your favorite language is {memory.get('favorite_language','unknown')}.")
        continue

    # PDF Summarizer
        # PDF Summarizer
    if question.lower().startswith("summarize "):
        filename = question[10:].strip()

        if filename.endswith(".pdf"):
            pdf_text = read_pdf(filename)

            print("Nova is thinking...")

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Nova, a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": f"Summarize this PDF clearly:\n\n{pdf_text[:3000]}"
                    }
                ]
            )

            print("\nNova:", response.choices[0].message.content)

        else:
            print("Nova: Please provide a PDF file.")

        continue
    # Everything else goes to Gemini
    memory_context = []

    if memory["name"]:
        memory_context.append(f"Name: {memory['name']}")

    if memory.get("city", ""):
        memory_context.append(f"City: {memory['city']}")

    if memory["college"]:
        memory_context.append(f"College: {memory['college']}")

    if memory["favorite_language"]:
        memory_context.append(f"Favorite Language: {memory['favorite_language']}")

    prompt = f"""
Memory:
{chr(10).join(memory_context)}

User:
{question}
"""
    print("Nova is thinking...")

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are Nova, a helpful personal AI assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        print("\nNova:", response.choices[0].message.content)

    except Exception as e:
        print(f"\nNova: Error - {e}")