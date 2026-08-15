def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"Error: {e}"