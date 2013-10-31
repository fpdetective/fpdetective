Instructions for patching and building Chromium:
-------------------------------------
Apply our patch to Chromium source code to log fingerprinting related events.

1) Checkout and build Chromium by following the instructions at http://code.google.com/p/chromium/wiki/LinuxBuildInstructions (for Linux)
2) Make sure you're able to build the release binary without applying the patch (following commands worked for us)
build/gyp_chromium -Dwerror= -D remove_webcore_debug_symbols=1 
ninja -C out/Release chrome
3) Change to src/third_party/WebKit directory
2) Apply the patch with the command:
patch -p0 < chromium.patch
3) Run the following commads (again) to build the patched binary
build/gyp_chromium -Dwerror= -D remove_webcore_debug_symbols=1 
ninja -C out/Release chrome
4) If you want to move Chromium to another directory, you also need to copy .pak files and locales directory from out/Release directory.
