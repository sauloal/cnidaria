#!/bin/bash

set -xeu

rm data/*/*.{jf,timming} || true
find data/ -type d -exec chmod 777 {} \;

rm -rf out    || true
mkdir out     || true
chmod 777 out
