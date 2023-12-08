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

./gcloudnopz.sh auth activate-service-account computeaccess@abrehman516-401023.iam.gserviceaccount.com \
        --key-file=$script_path/abrehman516-401023-286aa1ee7447.json \
        --project=$project_name

        # --key-file=$script_path/abrehman516-401023-f09a99dd00d3.json \
