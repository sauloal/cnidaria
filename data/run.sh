#!/bin/bash

set -xeu

docker run --rm -it --name cnidaria_running -v $PWD/data:/home/cnidaria/cnidaria/data/data -v $PWD/out:/home/cnidaria/cnidaria/data/out sauloal/cnidaria_full data/do.sh
