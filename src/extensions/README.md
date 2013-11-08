# FPDetective extensions

In this folder you can find browser extensions that can be used to detect known fingerprinting scripts. 
They're in alpha versions and not tested extensively.  

The extensions will display a notification when you visit a site that contain a fingerprinting script, 
describing the provider and the URL of the script. Chrome version also able to block fingerprinting scripts.

 
## Installation instructions

## Firefox

* Download the [extension](https://github.com/fpdetective/fpdetective/raw/master/src/extensions/ff/fpdetective.xpi).
* Click Install.
* You may need to click on *View > Toolbars > Add-on Bar* to show the add-on's icon.

## Chrome
* Download the [extension](https://github.com/fpdetective/fpdetective/blob/master/src/extensions/ch/ch.crx?raw=true).
* Click the Chrome menu icon at the right top.
* Select *Tools > Extensions*.
* Locate the extension file on your computer and drag the file onto the Extensions page.
* Click Install.

## How they work?
Extensions search for the URLs of the previously discovered fingerprinting scripts within the resources 
loaded by the pages you visit. 

## Do extensions report findings to a central server?
No. Extensions don't keep any data about your browsing habits and they don't report any information to any
parties including us.


