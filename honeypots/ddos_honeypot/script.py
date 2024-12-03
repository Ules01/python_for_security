from flask import Flask, request
import logging
import os

app = Flask(__name__)

# Log directory setup
LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=f"{LOG_DIR}/ddos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Redirect Flask logs to the configured logger
flask_logger = logging.getLogger('werkzeug')
flask_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{LOG_DIR}/ddos.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
flask_logger.addHandler(file_handler)

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    method = request.method
    logging.info(f"Received {method} request from {ip}")
    return "Simulated vulnerable server", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
