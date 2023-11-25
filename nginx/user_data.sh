#!/bin/bash
cd panda
sudodocker-compose up --build -d
chmod 777 /var/www/html/index.nginx-debian.html
echo "Hello World" > /var/www/html/index.nginx-debian.html