#!/bin/bash

gunicorn \
  server:app \
  -w "$NUM_VIRTEX_WORKERS" \
  -k virtex.VirtexWorker \
  --bind 0.0.0.0:"$VIRTEX_TARGET_PORT" \
  --worker-connections "$MAX_CONCURRENT_CONNECTIONS" \
  --logger-class virtex.VirtexLogger \
  --log-level "$LOG_LEVEL"
