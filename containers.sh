#!/bin/bash
set -e

case $1 in
    "stop")
        docker stop postgres-server
    ;;
    "start")
        docker container start postgres-server
    ;;
    "init")
        docker run -d -p 5432:5432 --name postgres-server -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD postgres:11
    ;;
    *)
        echo "Unknown option $1.  Should be one of [start stop]"
        exit 1
    ;;
esac
