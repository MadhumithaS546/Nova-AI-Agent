
def calculate(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Sorry, I couldn't calculate that."