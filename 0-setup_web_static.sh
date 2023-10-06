#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

apt-get update

if ! command -v nginx &> /dev/null; then
    apt-get install -y nginx
fi

ufw allow 'Nginx HTTP'

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

nginx_config="/etc/nginx/sites-available/default"
sed -i '/^server {/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' "$nginx_config"

service nginx restart
