# Agentic-Cybersecurity-pipeline-using-LangGraph-and-LangChain





https://github.com/user-attachments/assets/e60dc764-035a-4b12-92e4-051d2fb8816f



This project is an agentic cybersecurity pipeline that automates testing and security scanning. It uses LangChain and LangGraph to break down security tasks, execute them dynamically and adapt based on results.


# Setting up the project

## Prereqisites
Python 3.11+,Poetry and Dependencies 
`brew install nmap ffuf gobuster sqlmap`

## Clone Repository
`git clone https://github.com/your-username/cybersecurity-pipeline.git
cd cybersecurity-pipeline
`
## Install Dependencies

`pip install -r requirements.txt`

## Check Folder Structure
Run the command 
`tree`

You might get structure like this
`├── cybersecurity_pipeline.py
├── logs
├── pngtree-cyber-security-hologram-icon-png-image_13881165.png
├── requirements.txt
├── run_pipeline.py
├── streaml.py
└── test_pipeline.py`

## Initialize security scanning process
Run the command in terminal for testing tasks penetration on the defined scope
`python run_pipeline.py`

## Run Tests to Ensure Pipelines
`python -m unittest test_pipeline.py`

## Visualize the progress in real-time
Launch Streamlit Dashboard using command
`streamlit run streamlit_dashboard.py`

The final report generates when scan gets completed.

