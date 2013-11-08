# FPDetective extensions

*DISCLAIMER: these extensions are still being tested!

In this folder you can find a basic browser extension based on FPDetective framework that can be used to detect known fingerprinting scripts while you are browsing the web.
The extension is implemented for Chome (with blocking capability) and Firefox.

## Installation instructions

## Firefox

* If you have cloned the repository, you will already have the extension in the directory `~/fpbase/src/extensions/ff`. Otherwise, you can download it from [here](https://github.com/fpdetective/fpdetective/raw/master/src/extensions/ff/fpdetective.xpi).
* In order to install the extension you have to run firefox and go to Tools > Add-ons
* Choose "Extensions" from the left menu
* Go to the tools in the upper-right part of the window and "Install Add-on From File"
* Select the file `fpdetective.xpi`.
* You may need to restart Firefox
* In order to see the extension's icon you may also need to click on View > Toolbars > Add-on Bar

## Chrome

* If you have cloned the repository, you will already have the extension in the directory `~/fpbase/src/extensions/ch`. Otherwise, you have to download it from [here](https://github.com/fpdetective/fpdetective/blob/master/src/extensions/ch/ch.zip?raw=true) and unzip it.
* In order to install the extension you have to go to Chrome's Preferences toolbar button and select "Settings"
* Choose "Extensions" from the left menu
* Now, click on "Load unpacked extension..."
* Select the unziped folder if you downloaded the page from here, or select the folder `~/fpbase/src/extensions/ch`.
* You may need to restart Chrome

## Manual of Use

Once the extension is successfully installed, you can check if a website is loading a Fingerprinting script by just visiting it normally. In the positive case, a message will prop up describing the provider and the URL of the script.
 





