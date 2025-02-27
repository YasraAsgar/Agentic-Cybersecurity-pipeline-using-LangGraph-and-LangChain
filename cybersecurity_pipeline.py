import os
import subprocess
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph
from typing import Dict, List, Any

# Define tool execution functions
def run_nmap(target: str) -> str:
    try:
        result = subprocess.run(["nmap", "-sV", target], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def run_gobuster(target: str) -> str:
    try:
        result = subprocess.run(["gobuster", "dir", "-u", target, "-w", "/usr/share/wordlists/dirb/common.txt"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def run_ffuf(target: str) -> str:
    try:
        result = subprocess.run(["ffuf", "-u", f"{target}/FUZZ", "-w", "/usr/share/wordlists/dirb/common.txt"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

# Define tools
nmap_tool = Tool(
    name="Nmap Scanner",
    func=run_nmap,
    description="Scans a target for open ports and services using Nmap"
)
gobuster_tool = Tool(
    name="Gobuster Scanner",
    func=run_gobuster,
    description="Discovers directories on a web server using Gobuster"
)
ffuf_tool = Tool(
    name="FFUF Scanner",
    func=run_ffuf,
    description="Performs web fuzzing using FFUF"
)

# Define LangGraph state class
class SecurityState:
    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []
        self.results: List[Dict[str, str]] = []
        self.failed_tasks: List[Dict[str, Any]] = []

    def add_task(self, task: Dict[str, Any]):
        self.tasks.append(task)

    def add_result(self, task: Dict[str, Any], result: str):
        self.results.append({"task": task, "result": result})

    def retry_task(self, task: Dict[str, Any]):
        self.failed_tasks.append(task)

# Define LangGraph workflow
def execute_task(state: SecurityState):
    if not state.tasks:
        return state
    
    task = state.tasks.pop(0)
    tool_func = task["tool"]
    target = task["target"]
    
    result = tool_func(target)
    if "error" in result.lower():
        state.retry_task(task)
    else:
        state.add_result(task, result)
    
    return state

# Define LangGraph execution graph
graph = StateGraph(SecurityState)
graph.add_node("execute_task", execute_task)
graph.set_entry_point("execute_task")
executable_graph = graph.compile()

# Example usage
if __name__ == "__main__":
    state = SecurityState()
    state.add_task({"tool": run_nmap, "target": "scanme.nmap.org"})
    state.add_task({"tool": run_gobuster, "target": "http://testphp.vulnweb.com"})
    state.add_task({"tool": run_ffuf, "target": "http://testphp.vulnweb.com"})
    
    executable_graph.invoke(state)
    print("Results:", state.results)
