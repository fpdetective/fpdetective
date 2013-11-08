# FPDetective extensions

In this folder you can find a basic browser extension based on FPDetective framework that can be used to detect known fingerprinting scripts while you are browsing the web.
The extension is implemented for Chome (with blocking capability) and Firefox.

## Installation instructions

## Firefox

* If you have cloned the repository, you will already have the extension in the directory `~/fpbase/src/extensions/ff`. Otherwise, you can download it from [here](https://github.com/fpdetective/fpdetective/raw/master/src/extensions/ff/fpdetective.xpi).
* In order to inatall the extension you have to run firefox and go to Tools > Add-ons
* Choose "extensions" from the left menu
* Go to the tools in the upper-right part of the window and "Install Add-on From File"
* Select the file `fpdetective.xpi` and accept.
* You may need to restart Firefox

## Chrome

* You can download the Chrome extension from [here](https://github.com/fpdetective/fpdetective/blob/master/src/extensions/ch/ch.crx?raw=true).
* 

## Manual of Use

Once the extension is successfully installed, you can check if a website is loading a Fingerprinting script by just visiting it normally. In the positive case, a message will prop up describing the provider and the URL of the script.
 





