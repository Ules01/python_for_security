from flask import Flask, request
import logging
import os

app = Flask(__name__)

# Create logs directory relative to script location
LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=f'{LOG_DIR}/ddos.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s')

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    method = request.method
    logging.info(f"Received {method} request from {ip}")
    return "Simulated vulnerable server", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
