#!/bin/bash

cd honeypots
sudo docker build -t honeypots .
sudo docker run -d -p 8080:8080 -p 3000:3000 -p 80:80 \
    -v $(pwd)/logs:/app/logs honeypots

if [ $? -eq 0 ]; then
    echo "################################################"
    echo Honey pots lauched with Success
    echo '  - DDOS: 8080'
    echo '  - Brute Force: 3000'
    echo '  - Port Scan: 80'
    echo "################################################"
    exit 0
fi
exit 1

