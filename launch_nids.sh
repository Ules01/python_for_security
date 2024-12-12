#!/bin/bash

cd nids
sudo docker build -t nids_listener .
sudo docker run --rm -it --network=host nids_listener