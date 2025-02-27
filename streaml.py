import os
import json
import time
import subprocess
import streamlit as st
import pandas as pd
from pathlib import Path

# Define file paths
LogDir = "logs"
TaskStatus= os.path.join(LogDir, "task_status.json")
LogFile = os.path.join(LogDir, "execution_log.txt")
FinReport = os.path.join(LogDir, "audit_report.json")
ScopeConf = os.path.join(LogDir, "scope_cong.json")

# Check log directory exists
os.makedirs(LogDir, exist_ok=True)


# Define function to load task status
def LoadTstatus():
    if Path(TaskStatus).exists():
        with open(TaskStatus, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Define function to load logs
def SearchLogs():
    if Path(LogFile).exists():
        with open(LogFile, "r") as f:
            return f.readlines()[-10:]  
    return ["Waiting for logs..."]

# Define function to load final report
def SearchFinReport():
    if Path(FinReport).exists():
        with open(FinReport, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"error": "Report not generated yet."}
    return {"error": "Report not available."}

def start_pipeline():
    #Initialize cybersecurity pipeline process
    scope_cong = {"domain": target_domain, "ip_range": ip_range}
    with open(ScopeConf, "w") as f:
        json.dump(scope_cong, f)

    st.session_state["running"] = True
    subprocess.Popen(["python3", "run_pipeline.py"])
    st.success(":green[Pipeline started successfully!]")

def stop_pipeline():
    #Terminate running pipeline process.
    st.session_state["running"] = False
    subprocess.call(["pkill", "-f", "run_pipeline.py"])
    st.warning(" :red[Pipeline stopped.]")

# Initialize Layout
st.set_page_config(page_title="LangGraph-Based Agentic Cybersecurity Workflow", layout="centered",page_icon="/Users/yasrakhan/Desktop/PROJECT\/pngtree-cyber-security-hologram-icon-png-image_13881165.png",menu_items={
        "About": "This is a Streamlit app created by Yasra Sharif Khan"
    })
st.markdown(
    """
    <style>
    
    .custom-header {
        color: #3b74a3; 
        font-family: 'Courier New', monospace; 
        font-size: 36px;  
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h2 class="custom-header">Agentic Cybersecurity pipeline using LangGraph and LangChain</h2>', unsafe_allow_html=True)
st.write(":blue[Monitor penetration testing tasks in real time.]")


# Define Scope input
st.sidebar.header("Scope Scan Settings")
st.sidebar.divider()
target_domain = st.sidebar.text_input("Target Domain", "example.com")
ip_range = st.sidebar.text_input("IP Range ", "192.168.1.0/24")

# Start/Stop Scan Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Scan", key="start",type="primary"):
        start_pipeline()
with col2:
    if st.button("Stop Scan", key="stop",type="secondary"):
        stop_pipeline()

st.divider()


# Display Task Status 
st.subheader(":blue[Task Progress]")
task_status = LoadTstatus()

if task_status:
    try:
        task_status = {task: str(status) for task, status in task_status.items()}
        df = pd.DataFrame(list(task_status.items()), columns=["Task", "Status"])

        
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error displaying task status: {e}")
else:
    st.info("No tasks executed yet.")

# Display Live Log
st.subheader(":blue[Live Logs]")
st.text_area("Logs", "\n".join(SearchLogs()), height=200)

# Task Metrics
if task_status:
    completed_tasks = sum(1 for status in task_status.values() if status == "Completed")
    running_tasks = sum(1 for status in task_status.values() if status == "Running")
    failed_tasks = sum(1 for status in task_status.values() if status == "Failed")

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Completed Tasks", completed_tasks)
    col2.metric("⚡ Running Tasks", running_tasks)
    col3.metric("❌ Failed Tasks", failed_tasks)

# Display Final Audit Report
st.subheader(":blue[Final Audit Report]")
final_report = SearchFinReport()

if "error" in final_report:
    st.warning(final_report["error"])
else:
    st.json(final_report)

# Auto-refresh every 5 seconds
time.sleep(5)
st.experimental_rerun()
