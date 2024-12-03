#!/bin/bash

cd honeypots
sudo docker build -t honeypots .
sudo docker run -d -p 8080:8080 -p 22:22 -p 80:80 \
    -v $(pwd)/logs:/honeypots/logs honeypots

echo "################################################"
echo Honey pots lauched with Success
echo "################################################"

