### Instructions for patching browsers
You can use patches in this directory to build modified browsers used in FPDetective. 
The patched browsers will logs [events](https://github.com/fpdetective/fpdetective/blob/master/patches/README.md##the-patched-browsers-will-log-the-following-events) that might be related to web-based device fingerprinting.

* [Chromium](https://github.com/fpdetective/fpdetective/blob/master/patches/README.md#chromium)
* [PhantomJS](https://github.com/fpdetective/fpdetective/blob/master/patches/README.md#phantomjs)

### Chromium
1. Checkout and build Chromium by following the instructions at [http://code.google.com/p/chromium/wiki/LinuxBuildInstructions](http://code.google.com/p/chromium/wiki/LinuxBuildInstructions) (for Linux)
2. Make sure you're able to build and run the release version before applying the patch (the following commands worked for us)
```
build/gyp_chromium -Dwerror= -D remove_webcore_debug_symbols=1
ninja -C out/Release chrome
```
3. Change to `src/third_party/WebKit/Source` directory
4. Download the [patch file](https://raw.github.com/fpdetective/fpdetective/master/patches/chromium.patch)
5. Test the patch, be sure that you get no complaints for this command:
```
    git apply --check chromium.patch
```
6. If the check in step 6 fails, revert to exact snapshot used to generate the patch (32.0.1673.0):
```
    gclient config https://src.chromium.org/chrome/releases/32.0.1673.0
```
7. Apply the patch (if the check in step 5 is ok, you can possibly ignore whitespace warnings)
```
    git apply chromium.patch
```

8. Build the patched binary
```
    build/gyp_chromium -Dwerror= -D remove_webcore_debug_symbols=1 
    ninja -C out/Release chrome
```

Please note that if you want to move Chromium to another directory, 
you also need to copy all the `.pak` files, `locales` directory and `.so` files from `out/Release` folder.

### PhantomJS
1. Checkout and build PhantomJS code by following the instructions at [http://phantomjs.org/build](http://phantomjs.org/build)
2. Make sure you're able to build and run the binary
3. Download the [patch file](https://raw.github.com/fpdetective/fpdetective/master/patches/phantomjs.patch)
4. Apply the patch with the command:
`patch -p0 < phantomjs.patch`
5. Run `./build.sh` again to build the patched binary


### The patched browsers will log the following events:
* Font load attempts by intercepting calls to `CSSFontFace::getFontData` and `CSSFontSelector::getFontData` methods
* access to the following properties and methods: 
* **navigator**: `userAgent`, `appCodeName`, `product`, `productSub`, `vendor`, `vendorSub`, `onLine`, `appVersion`, `language`, `plugins`, `mimeTypes`, `cookieEnabled()`, `javaEnabled()`
* **navigator.plugins**: `name`, `filename`, `description`, `length`
* **navigator.mimeTypes**: `enabledPlugin`, `description`, `suffixes`, `type`
* **screen**: `horizontalDPI`, `verticalDPI`, `height`, `width`, `colorDepth`, `pixelDepth`, `availLeft`, `availTop`, `availHeight`, `availWidth`
* **HTML elements**: `offsetWidth`, `offsetHeight` properties and `getBoundingRect` method.
