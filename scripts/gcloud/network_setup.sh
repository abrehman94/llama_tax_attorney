#!/bin/bash

source ./config.sh

gcloud(){
  ./gcloudnopz.sh $@
}

# gcloud auth login
# gcloud projects list
# gcloud config set project $project_name 

nname=project516
gcloud compute networks create $nname --subnet-mode=auto
gcloud compute firewall-rules create psnetwork-allow-internal --network $nname --allow tcp,udp,icmp --source-ranges 10.128.0.0/9
gcloud compute firewall-rules create psnetwork-allow-external --network $nname --allow tcp:22,tcp:3389,icmp

