fpdetective
===========

A framework for conducting large scale web privacy studies.

## Installation

```
git clone https://github.com/fpdetective/fpdetective.git
cd fpdetective
```

Then follow [instructions for setting up VM](https://github.com/fpdetective/fpdetective/blob/master/vm/README.md)
to run FPDetective in a virtual machine

## Get Started
* Check [documentation](https://github.com/fpdetective/fpdetective/wiki)
* Read the paper: [FPDetective: Dusting the Web for Fingerprinters (CCS 2013)](https://www.cosic.esat.kuleuven.be/publications/article-2334.pdf)
* Visit [FPDetective website](https://www.cosic.esat.kuleuven.be/fpdetective/).
* Instructions for [using FPDetective with a VM](https://github.com/fpdetective/fpdetective/blob/master/vm/README.md)
* Check out recent binary [releases](https://github.com/fpdetective/phantomjs/releases).
* Check out the FPDetective browser [extensions](https://github.com/fpdetective/fpdetective/blob/master/extensions/).

### Command line parameters
Below we give a description of the parameters that are passed to the `agents.py` module.
* --index_url: path to the file containing the list of URLs to crawl
* --stop: index of the url_file where the crawl will stop
* --start (optional): index of the url_file where the crawl will start
* --type: the agent can be:
   * lazy: uses phantomjs and visits homepages
   * clicker: uses phantomjs and clicks a number of links
   * chrome_lazy: uses chrome and visits homepages
   * chrome_clicker: uses chromium and clicks a number of links
   * dnt: visits homepages with a DNT header set to 1
   * screenshot: visits homepages and takes a screenshot
* --max_proc: maximum number of processes that will run in parallel
* --fc_debug: boolean to set the system environment variable that logs the OS font requests


### How to launch a simple crawl 
You can use following command to crawl the homepages of Alexa top 100 sites with 
10 browsers running in parallel:

* Change to the FPDetective source directory: (`~/fpbase/src/crawler`) and run the command:
```
python agents.py --url_file ~/fpbase/run/top-1m.csv --stop 100 --type lazy --max_proc 10
```

Once the crawl is finished, you can check the log in `run/logs/latest` or connect to the DB using Phpmyadmin (the password for the root user is: `fpdetective`).

### Patches for Chromium & PhantomJS browser
You can use following patches to build modified Chromium and PhantomJS browsers from source. Please consult the [instructions](https://github.com/fpdetective/fpdetective/blob/master/patches/README.md) for further explanation.
 
* Chromium: [patch](https://github.com/fpdetective/fpdetective/blob/master/patches/chromium.patch)
* PhantomJS: [patch](https://github.com/fpdetective/fpdetective/blob/master/patches/phantomjs.patch)
