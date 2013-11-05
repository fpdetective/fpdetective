#!/usr/bin/env bash

# Update repositories
sudo apt-get update
sudo apt-get upgrade

# Install git
sudo apt-get -y install --yes --force-yes git-core
sudo -u vagrant git clone git://github.com/fpdetective/fpdetective.git
cd fpdetective
sudo -u vagrant ./setup.sh

echo "The bootstrap script has finished."
