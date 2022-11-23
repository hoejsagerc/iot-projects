#! /bin/bash

# Installing drivers
echo "CLONING WIFI DRIVER PACKAGE TO DEVICE"
git clone https://github.com/cilynx/rtl88x2bu /home/pi/drivers

echo "INSTALLING WIFI DRIVERS"
pushd /home/pi/drivers/
pwd
# Configure for RasP
sed -i 's/I386_PC = y/I386_PC = n/' Makefile
sed -i 's/ARM_RPI = n/ARM_RPI = y/' Makefile

# DKMS as above
VER=$(sed -n 's/\PACKAGE_VERSION="\(.*\)"/\1/p' dkms.conf)
sudo rsync -rvhP ./ /usr/src/rtl88x2bu-${VER}
sudo dkms add -m rtl88x2bu -v ${VER}
sudo dkms build -m rtl88x2bu -v ${VER}
sudo dkms install -m rtl88x2bu -v ${VER}
popd
pwd

echo "Please connect your wifi adapter to the pi before continuing."
read ACTION


# Configuring the new WLAN
echo "SETTING STATIC IP ON WLAN1"
sudo tee -a /etc/dhcpcd.conf <<EOF
interface wlan1
    static ip_address=192.168.99.1/24
    nohook wpa_supplicant
EOF

sudo tee /etc/systcl.d/routed-ap.conf <<EOF
net.ipv4.ip_forward=1
EOF

sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo netfilter-persistent save


echo "CLOBBERING THE DEFAULT DNSMASQ CONFIG"
sudo tee /etc/dnsmasq.conf <<EOF
interface=wlan1
  dhcp-range=192.168.99.100,192.168.99.199,255.255.255.0,24h
  domain=wlan
  address=/rt.wlan/192.168.99.1
EOF


echo "CONFIGURING HOSTAPD"
sudo tee /etc/hostapd/hostapd.conf <<EOF
interface=wlan1
driver=nl80211
ssid=pinet
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=P!ssw0rd1234
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

sudo sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

sudo systemctl unmask hostapd
sudo systemctl enable hostapd

echo "Do you want to reboot now? (y/n) - you will need to run the script: setup-docker.sh once reboot is complete."
read ACTION

if [[ $ACTION == "y" ]]
then
    sudo reboot now
else
    exit
fi