import json
import time
import traceback
import os

# Define File paths
tasks_status = "logs/task_status.json"
ExLog_status= "logs/execution_log.txt"
audit_rfile = "logs/audit_report.json"

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Initialize empty files if they don't exist
for file in [tasks_status, ExLog_status, audit_rfile]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f) if file.endswith(".json") else f.write("")

# Function to log execution messages
def log_message(message):
    """Logs a message to execution_log.txt"""
    with open(ExLog_status, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)  

# Function to update task status
def updateTStatus(task, status):
    #Updates json file of task_status with the latest task execution status
    try:
        with open(tasks_status, "r") as f:
            task_status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        task_status = {}

    task_status[task] = status

    with open(tasks_status, "w") as f:
        json.dump(task_status, f, indent=4)

    log_message(f"Task {task} updated to {status}")

# Main function to execute security scanning tasks
def run_pipeline():
    try:
        log_message(" Pipeline started successfully")

       
        updateTStatus("Nmap Scan", "Running")
        time.sleep(3)  
        updateTStatus("Nmap Scan", "Completed")

       
        updateTStatus("Gobuster Scan", "Running")
        time.sleep(3) 
        updateTStatus("Gobuster Scan", "Completed")

       
        updateTStatus("SQLMap Scan", "Running")
        time.sleep(3) 
        updateTStatus("SQLMap Scan", "Failed")  

        # Define to Generate Final Audit Report
        finReport = {
            "summary": "Cybersecurity scan completed.",
            "tasks": {
                "Nmap Scan": "Completed",
                "Gobuster Scan": "Completed",
                "SQLMap Scan": "Failed"
            }
        }

        with open(audit_rfile, "w") as f:
            json.dump(finReport, f, indent=4)

        log_message("The Final audit report generated!")

    except Exception as e:
        log_message("Pipeline crashed!")
        with open(ExLog_status, "a") as f:
            f.write(traceback.format_exc())

# Run the pipeline
if __name__ == "__main__":
    run_pipeline()
