from swarm import Agent


def write_code(task):
    """
    Provide the code written for the given task.
    """
    return f"Code for {task} has been written."


def test_code(code):
    """
    Provide the test results.
    When there is a problem with the test results, you can feedback to the User and Developer.
    """
    return f"Code '{code}' has been tested and passed all tests."


def manage_project(task):
    """
    When managing the project, you can provide updates to the user.
    Provide the code from the Developer or the test results from the Tester.
    """
    return f"Project task '{task}' is in progress."

def get_status(task):
    """
    When the user asks for the status of the project, you can provide the output of the code from Developer or the result of the tests from Tester.
    """
    return f"Project task '{task}' is in progress. The output is as follows:"

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
    instructions="""
    You are responsible for managing the project and coordinating between Developer and Tester.
    You can transfer the conversation to the Developer or Tester agent if needed.
    As the work progresses, you can provide updates to the user.
    When the user asks for the status of the project, you can provide the output of the code from Developer or the result of the tests from Tester.
    """,
    functions=[manage_project, get_status],
)

def transfer_to_developer():
    """Function to transfer the conversation to the Developer agent."""
    return developer_agent

def transfer_to_tester():
    """Function to transfer the conversation to the Tester agent."""
    return tester_agent

def transfer_to_project_manager():
    """Function to transfer the conversation to the Project Manager agent."""
    return project_manager_agent

developer_agent.functions.append(transfer_to_project_manager)
tester_agent.functions.append(transfer_to_project_manager)
project_manager_agent.functions.append(transfer_to_developer)
project_manager_agent.functions.append(transfer_to_tester)