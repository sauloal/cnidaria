#!/bin/bash

set -xeu

find data/ -type d -exec chmod 777 {} \;

mkdir out     || true

chmod 777 out
