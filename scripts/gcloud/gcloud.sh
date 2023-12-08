#!/bin/bash

get_real_path() {
    script_path=$(dirname $1)
    script_path=$(realpath $script_path)
}
if [[ $0 != $BASH_SOURCE ]]; then
    get_real_path $BASH_SOURCE
else
    get_real_path $0
fi

source $script_path/config.sh

$script_path/../google-cloud-sdk/bin/gcloud \
              "$@" \
              --project=$project_name \
              --zone=$zone 
