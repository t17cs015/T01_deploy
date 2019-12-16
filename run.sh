#!/bin/sh

if [[ $# == 0 ]]; then
    python3.5 manage.py runserver
elif [[ $1 == "mig" ]]; then
    python3.5 manage.py makemigrations management_system && python3.5 manage.py migrate
elif [[ $1 == "clean" ]]; then
    rm -r db.sqlite3 
    management_system/migrations/*
elif [[ $1 == "all" ]]; then
    $0 clean
    $0 mig
else
    python3.5 manage.py $@
fi

