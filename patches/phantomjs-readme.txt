Instructions for patching PhantomJS:
-------------------------------------
Apply our patch to PhantomJS source code to log fingerprinting related events.

1) Checkout and build PhantomJS code by following the instructions at http://phantomjs.org/build
2) Make sure you're able to build the binary when you run ./build.sh
2) Apply the patch with the command:
patch -p0 < phantomjs.patch
3) Run ./build.sh again to build the patched binary

List of logged events include:
-------------------------------------
-font load attempts by intercepting calls to CSSFontFace::getFontData and CSSFontSelector::getFontData methods
-access to the following navigator properties and methods: userAgent, appCodeName, product, productSub, vendor, vendorSub, onLine, appVersion, language, plugins, mimeTypes, cookieEnabled(), javaEnabled()
-access to navigator.plugins: name, filename, description, length
-access to navigator.mimeTypes: enabledPlugin, description, suffixes, type
-window.screen properties: horizontalDPI,verticalDPI, height, width, colorDepth, pixelDepth, availLeft, availTop, availHeight, availWidth
-access to offsetWidth and offsetHeight properties and getBoundingRect method of HTML elements.