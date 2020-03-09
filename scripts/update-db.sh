#!/bin/sh
exec >> debug.log 2>&1
while true
do
	python manage.py runscript NBAclient
	sleep 60
	python manage.py runscript baseballclient
	sleep 60
	python manage.py runscript hockeyclient
	sleep 60
	python manage.py runscript ncaabclient
	sleep 86220
done
