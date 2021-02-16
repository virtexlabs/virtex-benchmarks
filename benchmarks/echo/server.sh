#!/bin/bash

gunicorn \
  server:app \
  -w "$1" \
  -k virtex.VirtexWorker \
  --bind localhost:8081 \
  --max-requests 10000 \
  --worker-connections 10000 \
  --logger-class virtex.VirtexLogger \
  --log-level "$2"
