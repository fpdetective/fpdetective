Instructions for patching and building Chromium:
-------------------------------------
Apply our patch to Chromium source code to log fingerprinting related events.

1) Checkout and build Chromium by following the instructions at http://code.google.com/p/chromium/wiki/LinuxBuildInstructions (for Linux)
2) Make sure you're able to build the release binary without applying the patch (following commands worked for us)
build/gyp_chromium -Dwerror= -D remove_webcore_debug_symbols=1 
ninja -C out/Release chrome
3) Change to src/third_party/WebKit/Source directory
2) Apply the patch with the command:
patch -p0 < chromium.patch
3) Run the following commads (again) to build the patched binary
build/gyp_chromium -Dwerror= -D remove_webcore_debug_symbols=1 
ninja -C out/Release chrome
4) If you want to move Chromium to another directory, you also need to copy .pak files and locales directory from out/Release directory.


List of logged events include:
-------------------------------------
-font load attempts by intercepting calls to CSSFontFace::getFontData and CSSFontSelector::getFontData methods
-access to the following navigator properties and methods: userAgent, appCodeName, product, productSub, vendor, vendorSub, onLine, appVersion, language, plugins, mimeTypes, cookieEnabled(), javaEnabled()
-access to navigator.plugins: name, filename, description, length
-access to navigator.mimeTypes: enabledPlugin, description, suffixes, type
-window.screen properties: horizontalDPI,verticalDPI, height, width, colorDepth, pixelDepth, availLeft, availTop, availHeight, availWidth
-access to offsetWidth and offsetHeight properties and getBoundingRect method of HTML elements.
