#!/bin/bash

gunicorn \
  server:app \
  -w "$NUM_VIRTEX_WORKERS" \
  -k virtex.VirtexWorker \
  --bind localhost:"$VIRTEX_SERVICE_PORT" \
  --worker-connections "$MAX_CONCURRENT_CONNECTIONS" \
  --logger-class virtex.VirtexLogger \
  --log-level "$LOG_LEVEL"
