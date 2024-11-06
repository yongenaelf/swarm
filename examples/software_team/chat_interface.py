import json
import panel as pn
from agents import project_manager_agent
from swarm import Swarm

client = Swarm()

messages = []
agent = project_manager_agent

# Function to handle user input and display agent responses
def handle_input(event):
    user_input = event.new
    if user_input:
        global agent, chat, messages, chat_box
        messages.append({"role": "user", "content": user_input})
        response = client.run(
            agent=agent,
            messages=messages,
            stream=False,
        )
        chat.append(("User", user_input))
        pretty_print_messages(response.messages)
        chat_box.value = "\n".join([f"{msg[0]}: {msg[1]}" for msg in chat])
        input_box.value = ""
        messages.extend(response.messages)
        agent = response.agent

# Set up the chat interface
chat = []
chat_box = pn.widgets.TextAreaInput(value="", height=300, width=500, disabled=True)
input_box = pn.widgets.TextInput(placeholder="Enter your message here...")
input_box.param.watch(handle_input, 'value')

chat_interface = pn.Column(chat_box, input_box)
chat_interface.servable()

def pretty_print_messages(messages) -> None:
    for message in messages:
        if message["role"] != "assistant":
            continue

        # print agent name in blue
        print(f"\033[94m{message['sender']}\033[0m:", end=" ")

        # print response, if any
        if message["content"]:
            print(message["content"])
            chat.append((message["sender"], message["content"]))

        # print tool calls in purple, if any
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            print()
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            print(f"\033[95m{name}\033[0m({arg_str[1:-1]})")