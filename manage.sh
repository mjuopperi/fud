#!/bin/bash

DEFAULT_ENV="dev"

if [[ $(hostname) =~ "eu-west-1.compute.internal" ]]
then
    DEFAULT_ENV="prod"
fi

function usage {
    echo "Usage: ./manage.sh <command> <[dev|prod] default: $DEFAULT_ENV>"
    exit 1
}

if [ $# -lt 1 ]
then
    usage
elif [ $# -eq 1 ]
then
    python manage.py $1 --settings=fud.settings.$DEFAULT_ENV
    exit 0
elif [ $# -eq 2 ]
then
    if [ $2 == "dev" ] || [ $2 == "prod" ]
    then
        python manage.py $1 --settings=fud.settings.$2
        exit 0
    else
        usage
    fi
else
    usage
fi
