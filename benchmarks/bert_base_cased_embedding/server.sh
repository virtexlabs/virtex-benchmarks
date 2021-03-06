#!/bin/bash

gunicorn \
  server:app \
  --workers "$NUM_VIRTEX_WORKERS" \
  --worker-class virtex.VirtexWorker \
  --bind 0.0.0.0:"$VIRTEX_TARGET_PORT" \
  --worker-connections "$MAX_CONCURRENT_CONNECTIONS" \
  --timeout 120 \
  --log-level "$LOG_LEVEL"