#! /bin/bash

echo "INSTALLING DOCKER"
sudo apt-get update && sudo apt-get upgrade
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo usermod -aG docker pi

echo "INSTALLING DOCKER-COMPOSE"
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip
sudo pip3 install docker-compose

echo "ENABLING DOCKER SYSTEMD"
sudo systemctl enable docker