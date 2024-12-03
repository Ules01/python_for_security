from flask import Flask, request
import logging
import os
import random

app = Flask(__name__)

# Create logs directory relative to script location
LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=f'{LOG_DIR}/portscan.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s')

@app.route('/', methods=['GET'])
def index():
    ip = request.remote_addr
    logging.info(f"Port scan detected from {ip}")
    return "Port is open", 200

if __name__ == '__main__':
    random_port = random.choice([21, 22, 80, 443, 3306])
    logging.info(f"Starting honeypot on port {random_port}")
    app.run(host='0.0.0.0', port=random_port)
