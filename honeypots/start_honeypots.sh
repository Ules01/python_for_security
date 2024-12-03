#!/bin/bash

# Ensure logs directory exists
mkdir -p logs

# Start honeypots
python3 ddos_honeypot/script.py &
python3 bruteforce_honeypot/script.py &
python3 portscan_honeypot/script.py &

# Keep container running
tail -f /dev/null
