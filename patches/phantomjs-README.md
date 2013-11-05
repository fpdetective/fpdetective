1. Checkout and build PhantomJS code by following the instructions at [http://phantomjs.org/build](http://phantomjs.org/build)
2. Make sure you're able to build the binary when you run `./build.sh`
3. Apply the patch with the command:
`patch -p0 < phantomjs.patch`
4. Run `./build.sh` again to build the patched binary