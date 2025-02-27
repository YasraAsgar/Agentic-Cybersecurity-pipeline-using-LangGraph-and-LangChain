import logging

logging.basicConfig(filename="cybersecurity_pipeline.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_event(event):
    logging.info(event)
