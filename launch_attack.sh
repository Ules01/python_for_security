#!/bin/bash

cd script_attack
python3 bruteforce.py &
python3 ddos.py       &
python3 portscan.py   &
