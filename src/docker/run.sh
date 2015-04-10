cd 1_base && ./runDocker.sh && cd ..
cd 2_make && ./runDocker.sh && cd ..
cd 3_run  && ./runDocker.sh && cd ..

docker run -it --rm -v `readlink -f $PWD/../../`:/cnidaria cnidaria_run bash
