#!/bin/bash
if [ $1 = "server" ]
then
    python manage.py runserver --settings=fud.settings.dev
elif [ $1 = "migrate" ]
then
    python manage.py migrate --settings=fud.settings.dev
elif [ $1 = "test" ]
then
    python manage.py test --settings=fud.settings.dev
elif [ $1 = "makemigrations" ]
then
    python manage.py makemigrations --settings=fud.settings.dev
elif [ $1 = "shell" ]
then
    python manage.py shell --settings=fud.settings.dev
elif [ $1 = "dbshell" ]
then
    python manage.py dbshell --settings=fud.settings.dev
else
    echo "server || migrate || test || makemigrations || shell || dshell"
fi
