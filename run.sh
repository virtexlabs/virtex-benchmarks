#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

case "$TASK" in
   "bert-server")
      cd "$DIR"/benchmarks/bert_base_cased_embedding
      ./server.sh "$WORKERS" "$LOGLEVEL"
      ;;
   "bert-client")
      cd "$DIR"/benchmarks/bert_base_cased_embedding
      python client.py "$NUM_DATA" "$BATCHSIZE" "$RPS"
      ;;
   "resnet-server")
      cd "$DIR"/benchmarks/resnet_50_v2
      ./server.sh "$WORKERS" "$LOGLEVEL"
      ;;
   "resnet-client")
      cd "$DIR"/benchmarks/resnet_50_v2
      python client.py "$NUM_DATA" "$BATCHSIZE" "$RPS"
      ;;
   "echo-server")
      cd "$DIR"/benchmarks/echo
      ./server.sh "$WORKERS" "$LOGLEVEL"
      ;;
   "echo-client")
      cd "$DIR"/benchmarks/echo
      python client.py "$NUM_DATA" "$BATCHSIZE" "$RPS"
      ;;
   *)
     echo "$TASK is not a valid task."
     exit 1
     ;;
esac