#!/usr/bin/env bash

pip3 install -r requirements.txt -r requirements_dev.txt -r requirements_tools.txt

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
 sleep 0.1
done

echo "postgres started"

# Start ssh server
/usr/sbin/sshd -D

python3 manage.py db upgrade
python3 manage.py run -h 0.0.0.0 -p 5000
