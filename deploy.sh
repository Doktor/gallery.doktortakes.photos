#!/bin/bash

error=0

echo "running pre-deployment checks"

if ! command -v docker &> /dev/null
then
  echo "error: Docker is missing"
  error=1
fi

if ! command -v docker-compose &> /dev/null
then
  echo "error: Docker Compose is missing"
  error=1
fi

if [[ ! -f ./config/config.production.toml ]]
then
  echo "error: configuration file \"config.production.toml\" is missing"
  error=1
fi

if [[ ! -f ./config/secrets.production.toml ]]
then
  echo "error: secrets configuration file \"secrets.production.toml\" is missing"
  error=1
fi

if [[ ! error -eq 0 ]]
then
  echo "encountered errors during pre-deployment check, exiting"
  exit 1
else
  echo "pre-deployment checks ran successfully"
fi

echo "starting deployment"

echo "building Docker images" && \
  sudo docker-compose -f docker-compose.production.yml build && \
  echo "starting Docker container" && \
  sudo docker-compose -f docker-compose.production.yml up -d

echo "copying Nginx config file" && \
  sudo cp ./build/nginx/nginx.production.conf /etc/nginx/sites-enabled/doktortakes.photos.conf

echo "reloading Nginx" && \
  service nginx reload

exit 0
