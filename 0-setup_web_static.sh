#!/usr/bin/env bash
# A script that installs and configs nginx

# install nginx
sudo apt-get update
sudo apt-get install nginx -y

# creating the repositories
sudo mkdir -p /data/web_static/releases/test/ 
sudo mkdir -p /data/web_static/shared/
echo " Holberton School" | sudo tee /data/web_static/releases/test/index.html

# creating the symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu and group
sudo chown -R ubuntu:ubuntu /data/

# setting up the page to be served
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo service nginx start
