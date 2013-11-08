# FPDetective extensions

You can use following browser extensions to detect fingerprinting scripts, most of which were 
discovered during our FPDetective study.

The extensions will display a notification when you visit a site that contain a fingerprinting script, 
describing the provider and the URL of the script. Chrome extension is also able to block fingerprinting scripts.

Please keep in mind that the extensions are not tested extensively and alpha stage.

 
## Installation instructions

## Firefox

* Download the [extension](https://github.com/fpdetective/fpdetective/raw/master/src/extensions/firefox/fpdetective.xpi).
* Click Install.
* You may need to click on *View > Toolbars > Add-on Bar* to show the add-on's icon.

## Chrome
* Download the [extension](https://github.com/fpdetective/fpdetective/blob/master/src/extensions/chrome/ch.crx?raw=true).
* Click the Chrome menu icon at the right top.
* Select *Tools > Extensions*.
* Locate the extension file on your computer and drag the file onto the Extensions page.
* Click Install.

## How they work?
Extensions search for the [URLs of the previously discovered fingerprinting scripts]
(https://github.com/fpdetective/fpdetective/blob/master/src/crawler/log_parser.py) within the resources 
loaded by the pages you visit.

The extensions cannot determine if the detected script (or Flash file) is executed or not. 
So it's technically possible that the scripts detected by the extension were not executed but only served.

## Do extensions report findings to a central server?
No. Extensions don't keep any data about your browsing habits and they don't report any information to any
parties including us.


