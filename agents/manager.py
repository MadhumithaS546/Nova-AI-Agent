from agents.memory_agent import memory_reply
from agents.web_agent import web_reply
from tools.router import use_tool, route_query

def handle_local_request(prompt, memory, pdf_text):
    route = route_query(prompt, has_pdf=bool(pdf_text))

    # Memory Agent
    if route == "memory":
        reply = memory_reply(prompt, memory)
        return route, reply

    # Web Agent
    if route == "web":
        return route, web_reply(prompt)

    # Tool Agent
    if route == "tool":
        return route, use_tool(prompt)

    # PDF and Chat go to the Chat Agent
    return route, None