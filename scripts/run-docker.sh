#!/bin/sh
ip=`hostname -I | awk '1 { print $1 }'`
exec python manage.py runserver ${ip}:8000
