#!/bin/sh


python ./banking_system/manage.py makemigrations --merge
python ./banking_system/manage.py migrate --noinput
python ./banking_system/manage.py populate
python ./banking_system/manage.py rqworker &
echo "Start Rq worker"
python ./banking_system/manage.py runserver 0.0.0.0:8000 


