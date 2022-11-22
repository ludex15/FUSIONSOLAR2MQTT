#!/usr/bin/env bash
set -e

docker-compose down

docker-compose --env-file ../app/.env up -d --build