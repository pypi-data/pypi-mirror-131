#!/bin/bash

set -e
env
echo "Current directory: $(pwd)"

apt-get update
apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
bash -c "curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -"
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian buster stable"
apt-get update
apt-get -y install docker-ce docker-ce-cli containerd.io
docker -v
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-319.0.0-linux-x86_64.tar.gz
tar -vzxf google-cloud-sdk-319.0.0-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh --quiet
./google-cloud-sdk/bin/gcloud components install kubectl --quiet
export PATH="$PATH:$(pwd)/google-cloud-sdk/bin"
ln -s "$(pwd)/google-cloud-sdk/bin/gcloud" /usr/local/bin/gcloud
ln -s "$(pwd)/google-cloud-sdk/bin/kubectl" /usr/local/bin/kubectl
ln -s "$(pwd)/google-cloud-sdk/bin/docker-credential-gcloud" /usr/local/bin/docker-credential-gcloud
