#!/bin/bash

set -x


if [ "$#" == "0" ]; then 
  arg=""
else
  arg="--command=$@"
fi

source ./config.sh

for i in {1..10}; do
  if ./gcloud.sh compute ssh abrehman@$instance $arg;then 
    break
  fi
  echo "Retrying gcloudscp $i th time"
  sleep 1
done

