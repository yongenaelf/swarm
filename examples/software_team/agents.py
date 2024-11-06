from swarm import Agent


def write_code(task):
    """Function for the Developer agent to write code based on the given task."""
    return f"Code for {task} has been written."


def test_code(code):
    """Function for the Tester agent to test the given code."""
    return f"Code '{code}' has been tested and passed all tests."


def manage_project(task):
    """Function for the Project Manager agent to manage the project and coordinate between Developer and Tester."""
    return f"Project task '{task}' has been managed and coordinated."


developer_agent = Agent(
    name="Developer Agent",
    instructions="You are responsible for writing code based on the given task.",
    functions=[write_code],
)

tester_agent = Agent(
    name="Tester Agent",
    instructions="You are responsible for testing the given code.",
    functions=[test_code],
)

project_manager_agent = Agent(
    name="Project Manager Agent",
    instructions="You are responsible for managing the project and coordinating between the Developer and Tester agents.",
    functions=[manage_project],
)
