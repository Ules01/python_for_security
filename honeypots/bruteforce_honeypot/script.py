from flask import Flask, request
import logging
import os

app = Flask(__name__)

# Create logs directory relative to script location
LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=f'{LOG_DIR}/bruteforce.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', 'unknown')
    password = request.form.get('password', 'unknown')
    ip = request.remote_addr
    logging.info(f"Brute force attempt from {ip}: {username} / {password}")
    return "Access Denied", 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=22)
