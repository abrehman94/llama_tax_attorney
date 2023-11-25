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


if [ ! -d $script_path/../google-cloud-sdk ]; then  
  package=google-cloud-cli-449.0.0-linux-x86_64.tar.gz
  curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/$package
  tar -xvzf $package 
  rm $package
  mv $script_path/google-cloud-sdk $script_path/../
else
  echo "sdk is already downloaded"
fi

