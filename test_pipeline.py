import pytest
from cybersecurity_pipeline import SecurityState, execute_task, run_nmap, run_gobuster, run_ffuf  # type: ignore # Import your functions

# Mock target for testing
target_test = "scanme.nmap.org"

@pytest.fixture
#Refresh SecurityState before each test
def state():
    return SecurityState()

#Check tasks are added correctly
def task_addition(state):
    task = {"tool": run_nmap, "target": target_test}
    state.add_task(task)
    assert len(state.tasks) == 1
    assert state.tasks[0]["target"] == target_test

#Check correct Nmap format execution
def nmap_T_execution():
    result = run_nmap(target_test)
    assert isinstance(result, str)
    assert "open" in result.lower() or "filtered" in result.lower()  

#Check correct Gobuster execution
def gobuster_T_execution():
    
    result = run_gobuster(target_test)
    assert isinstance(result, str)

#Check FFUF execution
def ffuf_T_execution():
    result = run_ffuf(target_test)
    assert isinstance(result, str)

#Check State execution
def state_T_execution(state):
    state.add_task({"tool": run_nmap, "target": target_test})
    initial_task_count = len(state.tasks)
    state = execute_task(state)
    assert len(state.tasks) == initial_task_count - 1
    assert len(state.results) == 1

#Check to test the failed tasks
def retry_mech(state):
    failed_task = {"tool": lambda x: "error", "target": target_test}  # Mock failing tool
    state.add_task(failed_task)
    state = execute_task(state)
    assert len(state.failed_tasks) == 1  # Task should be retried
