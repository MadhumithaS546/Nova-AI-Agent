import re
from tools.calculator import calculate
from tools.file_reader import read_file
from tools.file_search import search_file
from tools.pdf_reader import read_pdf
from tools.web_search import web_search
from tools.folder_browser import list_files

def use_tool(question):
    text = question.lower().strip()

    # ---------- Calculator ----------
    math_words = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "multiplied by": "*",
        "multiply by": "*",
        "divide by": "/",
        "divided by": "/"
    }

    expression = text

    for word, symbol in math_words.items():
        expression = expression.replace(word, symbol)

    # Keep only numbers, operators, dots, parentheses and spaces
    expression = re.sub(r"[^0-9+\-*/(). ]", "", expression).strip()

    if expression and any(op in expression for op in "+-*/"):
        return calculate(expression)

    # ---------- Read File ----------
    if text.startswith("read "):
        filename = question[5:].strip()
        return read_file(filename)

    # ---------- Find File ----------
    if text.startswith("find "):
        keyword = question[5:].strip()
        return search_file(keyword)

    if text.endswith(".pdf") or "pdf" in text:
        filename = question.split()[-1]
        return read_pdf(filename)

    if text.startswith("search ") or "look up" in text:
        query = question.replace("search", "").replace("look up", "").strip()
        return web_search(query)

    if "list files" in text:
        return list_files()
    
    return None