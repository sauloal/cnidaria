set -xeu

( cd 1_base   && ./runDocker.sh )
( cd 2_python && ./runDocker.sh )
( cd 3_full   && ./runDocker.sh )
( cd 4_make   && ./runDocker.sh )

#docker run -it --rm -v `readlink -f $PWD/../../`:/test sauloal/cnidaria_full bash
