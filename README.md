fpdetective
===========
STILL UNDER CONSTRUCTION!

A framework for conducting large scale web privacy studies.

## Installation

```
git clone https://github.com/fpdetective/fpdetective.git
cd fpdetective
```
After that point, you've two options: 

1. Run `./setup.sh` to use FPDetective on your computer
2. Follow [instructions for setting up VM](https://github.com/fpdetective/fpdetective/blob/master/vm/README.md)
to run FPDetective in a virtual machine

Please note that setup.sh will download browsers and other binaries used by FPDetective. 
This may take while depending on your connection.

## Get Started
* Check [documentation](https://github.com/fpdetective/fpdetective/wiki)
* Visit [FPDetective website](https://www.cosic.esat.kuleuven.be/fpdetective/).
* Instructions for [using FPDetective with a VM](https://github.com/fpdetective/fpdetective/wiki/Instructions-for-setting-up-VM)
* Check out recent binary [releases](https://github.com/fpdetective/phantomjs/releases).
* Consult [PhantomJS wiki](https://github.com/ariya/phantomjs/wiki) to learn more about PhantomJS

### Basic manual for `agents.py`
* --index_url: path to the file containing the list of URLs to crawl
* --top: index of the url_file where the crawl will stop
* --start: index of the url_file where the crawl will start
* --type: the agent can be:
   * lazy: uses phantomjs and only visits homepages
   * clicker: uses phantomjs and clicks a number of login-like links
   * chrome_lazy: uses chrome and only visits homepages
   * chrome_clicker: uses chromium and clicks a number of login-like links
   * dnt: visits a page setting the DNT header to True
   * screenshot: visits pages and prints a screenshot to file
* --max_proc: maximum number of processes that will run in parallel
* --fc_debug: boolean to set the system environment variable that logs the OS font requests


### How to make a basic crawl
As an example, if you want to crawl the Alexa top 100 in lazy mode and using 10 process in parallel, you can follow the following instructions:

* Change to the FPDetective base directory: `cd ~/fpbase` 
* Run agents.py: `python src/crawler/agents.py --url_file run/top-1m.csv --stop 100 --type lazy --max_proc 10`

Once the crawl is finished, you can check the log in `run/logs/latest` or connect to the DB using Phpmyadmin (the password for the root user is: `fpdetective`).

### FPDetective on VM
You can follow these instructions to set up a VM and use FPDetective independently of the configuration of your operating system:

* [Instructions for setting up VM](https://github.com/fpdetective/fpdetective/wiki/Instructions-for-setting-up-VM)

### Patches for Chromium & PhantomJS browser
You can use following patches to build modified Chromium and PhantomJS browsers from source. Please consult the [instructions](https://github.com/fpdetective/fpdetective/blob/master/patches/README.md) for further explanation.
 
* Chromium: [patch](https://github.com/fpdetective/fpdetective/blob/master/patches/chromium.patch)
* PhantomJS: [patch](https://github.com/fpdetective/fpdetective/blob/master/patches/phantomjs.patch)
