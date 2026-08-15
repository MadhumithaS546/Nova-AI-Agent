import os

def search_file(keyword):
    matches = []

    for root, dirs, files in os.walk("."):
        for file in files:
            if keyword.lower() in file.lower():
                matches.append(os.path.join(root, file))

    if matches:
        return "\n".join(matches)

    return "No matching file found."