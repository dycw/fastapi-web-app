#!/usr/bin/env bash

# Consider running these two commands separately
# Do a reboot before continuing.
sudo apt update
sudo apt upgrade -y

# shell utilities
sudo apt install fzf nvim zsh
sudo snap install starship

# Install some OS dependencies:
sudo apt install -y build-essential git nload tree unzip zip
sudo apt install -y python3-pip python3-dev python3-venv
sudo apt install -y direnv

# Stop the hackers
sudo apt install fail2ban -y

ufw allow 22
ufw allow 80
ufw allow 443
ufw enable


apt install acl -y
useradd -M apiuser
usermod -L apiuser
setfacl -m u:apiuser:rwx /apps/logs/weather_api


# Web app file structure
mkdir /apps
chmod 777 /apps
mkdir /apps/logs
mkdir /apps/logs/weather_api
mkdir /apps/logs/weather_api/app_log
# chmod 777 /apps/logs/weather_api
cd /apps

# Create a virtual env for the app.
cd /apps
python3 -m venv venv
source /apps/venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install --upgrade httpie glances
pip install --upgrade gunicorn uvloop httptools

# clone the repo:
cd /apps
git clone https://github.com/talkpython/modern-apis-with-fastapi app_repo

# Setup the web app:
cd /apps/app_repo/ch08-deployment
pip install -r requirements.txt

# Copy and enable the daemon
cp /apps/app_repo/ch08-deployment/server/units/weather.service /etc/systemd/system/

systemctl start weather
systemctl status weather
systemctl enable weather

# Setup the public facing server (NGINX)
apt install nginx

# CAREFUL HERE. If you are using default, maybe skip this
rm /etc/nginx/sites-enabled/default

cp /apps/app_repo/ch08-deployment/server/nginx/weather.nginx /etc/nginx/sites-enabled/
update-rc.d nginx enable
service nginx restart


# Optionally add SSL support via Let's Encrypt:
# https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04

add-apt-repository ppa:certbot/certbot
apt install python3-certbot-nginx
certbot --nginx -d weatherapi.talkpython.com
