#!/usr/bin/env bash

# Update repositories
sudo apt-get update
sudo apt-get upgrade

# Install git
sudo apt-get -y install --yes --force-yes git-core
git clone https://github.com/fpdetective/fpdetective/fpdetective
cd fpdetective
sh setup.sh

echo "The  bootstrap script has finished."
