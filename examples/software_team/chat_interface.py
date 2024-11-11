import json
import panel as pn
from agents import project_manager_agent
from swarm import Swarm

client = Swarm()

messages = []
agent = project_manager_agent

pn.extension()

def get_response(contents, user, instance):
    global agent, messages, stream

    if user == "user":
        messages.append({"role": "user", "content": contents})

    response = client.run(
            agent=agent,
            messages=messages,
            stream=True,
            debug=True
        )
    
    content = ""
    last_sender = ""
    current_sender = ""

    for chunk in response:
        if "sender" in chunk:
            last_sender = chunk["sender"]
            current_sender = chunk["sender"]

        if "content" in chunk and chunk["content"] is not None:
            if not content and last_sender:
                print(f"\033[94m{last_sender}:\033[0m", end=" ", flush=True)
                last_sender = ""
            print(chunk["content"], end="", flush=True)
            content += chunk["content"]
            yield pn.chat.ChatMessage(
                content,
                user=current_sender,
            )

        if "tool_calls" in chunk and chunk["tool_calls"] is not None:
            for tool_call in chunk["tool_calls"]:
                f = tool_call["function"]
                name = f["name"]
                if not name:
                    continue
                print(f"\033[94m{last_sender}: \033[95m{name}\033[0m()")

        if "delim" in chunk and chunk["delim"] == "end" and content:
            print()  # End of response message
            content = ""

        if "response" in chunk:
            response = chunk["response"]
    
    messages.extend(response.messages)
    agent = response.agent
    

chat_bot = pn.chat.ChatInterface(callback=get_response, user="user", max_height=800)
chat_bot.send("Ask me anything!", user="Project Manager", respond=False)

pn.extension(template="fast")
logout = pn.widgets.Button(name="Log out")
logout.js_on_click(code="""window.location.href = './logout'""")
pn.Column(chat_bot, logout).servable()