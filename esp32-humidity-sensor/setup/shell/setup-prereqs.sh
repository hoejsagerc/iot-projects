#! /bin/bash

# Updating packages on the Raspberry Pi
echo "UPDATING THE PACKAGES"
sudo apt update && sudo apt upgrade -y

# Installing prerequisites
echo "INSTALLING PREREQS"
sudo apt install git dnsmasq hostapd bc build-essential dkms raspberrypi-kernel-headers -y

echo "Do you want to reboot now? (y/n) - you will need to run the script: setup-wifi.sh once reboot is complete."
read ACTION

if [[ $ACTION == "y" ]]
then
    sudo reboot now
else
    exit
fi