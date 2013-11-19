# FPDetective extensions

You can use following browser extensions to detect fingerprinting scripts, most of which were 
discovered during our FPDetective study.

The extensions will display a notification when you visit a page that has a fingerprinting script or obje.

Please keep in mind that the extensions are not tested extensively and in alpha stage.

 
## Installation instructions

## Firefox

* Download the [extension](https://github.com/fpdetective/fpdetective/blob/master/extensions/fpdetective.xpi?raw=true).
* Click Install.
* You may need to click on *View > Toolbars > Add-on Bar* to show the add-on's icon.

## Chrome
* Download the [extension](https://github.com/fpdetective/fpdetective/blob/master/extensions/fpdetective.crx?raw=true).
* Click the Chrome menu icon at the right top.
* Select *Tools > Extensions*.
* Locate the extension file on your computer and drag the file onto the Extensions page.
* Click Install.

## How they work?
Extensions search for the [URLs of the previously discovered fingerprinting scripts]
(https://github.com/fpdetective/fpdetective/blob/master/src/crawler/fp_regex.py) within the resources 
loaded by the pages you visit.

The extensions cannot determine if the detected script (or Flash file) is executed or not. 
So it's technically possible that the scripts detected by the extension were not executed but only served.

## Do extensions report findings to any parties?
No. Extensions don't keep any data about your browsing habits and they don't report any information to any
parties including us.


