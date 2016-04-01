set -xeu

( cd 1_base   && ./runDocker.sh )
( cd 2_python && ./runDocker.sh )
( cd 3_full   && ./runDocker.sh )
