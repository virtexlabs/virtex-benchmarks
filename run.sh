#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

case "$TASK" in
   "bert-server")
      cd "$DIR"/benchmarks/bert_base_cased_embedding
      ./server.sh
      ;;
   "bert-client")
      cd "$DIR"/benchmarks/bert_base_cased_embedding
      python3 client.py
      ;;
   "resnet-server")
      cd "$DIR"/benchmarks/resnet_50_v2
      ./server.sh
      ;;
   "resnet-client")
      cd "$DIR"/benchmarks/resnet_50_v2
      python3 client.py
      ;;
   "echo-server")
      cd "$DIR"/benchmarks/echo
      ./server.sh
      ;;
   "echo-client")
      cd "$DIR"/benchmarks/echo
      python3 client.py
      ;;
   *)
     echo "$TASK is not a valid task."
     exit 1
     ;;
esac