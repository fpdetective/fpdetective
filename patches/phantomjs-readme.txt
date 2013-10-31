Instructions for patching PhantomJS:
-------------------------------------
Apply our patch to PhantomJS source code to log fingerprinting related events.

1) Checkout and build PhantomJS code by following the instructions at http://phantomjs.org/build
2) Make sure you're able to build the binary when you run ./build.sh
2) Apply the patch with the command:
patch -p0 < phantomjs.patch
3) Run ./build.sh again to build the patched binary