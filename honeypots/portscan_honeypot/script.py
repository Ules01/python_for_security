from flask import Flask, request
import logging
import os
import random

app = Flask(__name__)

# Log directory setup
LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=f"{LOG_DIR}/portscan.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Redirect Flask logs to the configured logger
flask_logger = logging.getLogger('werkzeug')
flask_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{LOG_DIR}/portscan.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
flask_logger.addHandler(file_handler)

@app.route('/', methods=['GET'])
def index():
    ip = request.remote_addr
    logging.info(f"Port scan detected from {ip}")
    return "Port is open", 200

if __name__ == '__main__':
    logging.info(f"Starting honeypot on port {80}")
    app.run(host='0.0.0.0', port=80)
