#!/bin/sh
docker rmi -f $(docker images --filter "dangling=true" -q --no-trunc)
docker-compose down
docker-compose up -d $1
docker logs -f crypto-alert-service 2>&1 | ccze -m ansi
