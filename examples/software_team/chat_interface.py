import json
import panel as pn
from agents import project_manager_agent
from swarm import Swarm

client = Swarm()

messages = []
agent = project_manager_agent

pn.extension()

def get_response(contents, user, instance):
    global agent, messages

    if user == "user":
        messages.append({"role": "user", "content": contents})

    response = client.run(
            agent=agent,
            messages=messages,
            stream=False,
        )
    
    messages.extend(response.messages)
    agent = response.agent
    return pretty_print_messages(response.messages)
    

chat_bot = pn.chat.ChatInterface(callback=get_response, user="user", max_height=800)
chat_bot.send("Ask me anything!", user="Assistant", respond=False)

chat_bot.servable()

def pretty_print_messages(messages):
    for message in messages:
        if message["role"] != "assistant":
            continue

        # print agent name in blue
        print(f"\033[94m{message['sender']}\033[0m:", end=" ")

        # print response, if any
        if message["content"]:
            print(message["content"])
            yield message["content"]

        # print tool calls in purple, if any
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            print()
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            print(f"\033[95m{name}\033[0m({arg_str[1:-1]})")