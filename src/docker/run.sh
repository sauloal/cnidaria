set -xeu

( cd 1_base && ./runDocker.sh )
( cd 2_make && ./runDocker.sh )
( cd 3_run  && ./runDocker.sh )

docker run -it --rm -v `readlink -f $PWD/../../`:/test sauloal/cnidaria_run bash
