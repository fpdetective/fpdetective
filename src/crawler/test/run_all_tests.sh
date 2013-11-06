#!/usr/bin/env bash

# Run all the tests
echo "Running runenv_test.py"
python runenv_test.py
echo "Running agents_test.py"
python agents_test.py
echo "Running casper_test.py"
python casper_test.py
echo "Running chrome_test.py"
python chrome_test.py
echo "Running dbutils_test.py"
python dbutils_test.py
echo "Running fileutils_test.py"
python fileutils_test.py
echo "Running logparser_test.py"
python logparser_test.py
echo "Running mitm_test.py"
python mitm_test.py
echo "Running mod_chromium_test.py"
python mod_chromium_test.py
echo "Running phantomDNT_test.py"
python phantomDNT_test.py
echo "Running swfutils_test.py"
python swfutils_test.py
echo "Running utils_test.py"
python utils_test.py
echo "Running webutils_test.py"
python webutils_test.py
