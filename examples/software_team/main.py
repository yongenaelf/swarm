from agents import developer_agent, tester_agent, project_manager_agent
from swarm.repl import run_demo_loop

context_variables = {
    "project_name": "New Software Project",
    "task": "Implement feature X",
}

def main():
    task = context_variables["task"]
    
    # Developer writes code
    code = developer_agent.functions[0](task)
    print(code)
    
    # Tester tests code
    test_result = tester_agent.functions[0](code)
    print(test_result)
    
    # Project Manager manages project
    management_result = project_manager_agent.functions[0](task)
    print(management_result)

if __name__ == "__main__":
    run_demo_loop(project_manager_agent, context_variables=context_variables, debug=True)
