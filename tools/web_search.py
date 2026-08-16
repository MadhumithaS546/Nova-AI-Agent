from duckduckgo_search import DDGS

def web_search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    output = ""

    for i, result in enumerate(results, 1):
        output += (
            f"{i}. {result['title']}\n"
            f"{result['href']}\n"
            f"{result['body']}\n\n"
        )

    return output