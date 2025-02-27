# Agentic-Cybersecurity-pipeline-using-LangGraph-and-LangChain





https://github.com/user-attachments/assets/e60dc764-035a-4b12-92e4-051d2fb8816f



This project is an agentic cybersecurity pipeline that automates testing and security scanning. It uses LangChain and LangGraph to break down security tasks, execute them dynamically and adapt based on results.


## Task Execution
 This converts high-level security tasks into ordered task lists,Executes tasks dynamically with error handling and retries then updates task lists based on real-time scan results
## Security Scanning Tools
 Nmap( Network scanning),Gobuster / FFUF (Directory and subdomain brute-forcing) and SQLMap (SQL injection detection)
Parses and processes scan results for further actions
## Scope Enforcement
it restricts scans to user-defined domains & IP ranges,prevents scans from running out of scope and terminates scans attempting to operate beyond allowed scope
## Task Monitoring, Failure Handling & Recovery
It detects failures such as timeouts, crashes and invalid responses.It retries tasks with alternative parameters and dynamically appends new tasks as vulnerabilities are discovered
## Reporting & Logging
It has Real-time logging of security scan activities,Final audit report highlighting vulnerabilities and Streamlit Dashboard for monitoring task progress, logs and results
