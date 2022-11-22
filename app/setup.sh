#!/usr/bin/env bash

docker-compose down

docker-compose --env-file .env up -d --build