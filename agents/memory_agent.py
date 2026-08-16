def memory_reply(prompt, memory):
    text = prompt.lower()

    if "what is my name" in text:
        return f"Your name is {memory.get('name', 'unknown')}."

    if "where am i from" in text:
        return f"You're from {memory.get('city', 'an unknown place')}."

    if "what is my favorite language" in text or "what is my favourite language" in text:
        return f"Your favorite language is {memory.get('favorite_language', 'unknown')}."

    return Nones