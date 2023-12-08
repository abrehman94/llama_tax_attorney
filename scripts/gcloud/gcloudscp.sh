#!/bin/bash

for i in {1..10}; do
  if ./gcloud.sh compute scp "$@";then 
    break
  fi
  echo "Retrying gcloudscp $i th time"
  sleep 1
done
