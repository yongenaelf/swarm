import panel as pn
from agents import developer_agent, tester_agent, project_manager_agent

# Function to handle user input and display agent responses
def handle_input(event):
    user_input = event.new
    if user_input:
        response = project_manager_agent.functions[0](user_input)
        chat.append((user_input, response))
        chat_box.value = "\n".join([f"User: {msg[0]}\nAgent: {msg[1]}" for msg in chat])
        input_box.value = ""

# Set up the chat interface
chat = []
chat_box = pn.widgets.TextAreaInput(value="", height=300, width=500, disabled=True)
input_box = pn.widgets.TextInput(placeholder="Enter your message here...")
input_box.param.watch(handle_input, 'value')

chat_interface = pn.Column(chat_box, input_box)
chat_interface.servable()
