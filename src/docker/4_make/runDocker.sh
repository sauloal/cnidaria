set -xeu

if [[ -f "ok" ]]; then
exit 0
fi

USER_UID=`id -u $USER`

#docker build --rm --build-arg USER_UID=`id -u $USER` -t sauloal/cnidaria_make .

docker run --rm -it --name cnidaria_making -v $PWD/../../../:/home/cnidaria/cnidaria sauloal/cnidaria_full bash -c '\
echo $PWD && \
cd ../src && \
ls -la && \
GEN_SHARED=true make all && \
chown -R '$USER_UID':'$USER_UID' .'

docker run --rm -it --name cnidaria_running -v $PWD/../../../:/home/cnidaria/cnidaria sauloal/cnidaria_full bash -c '\
jellyfish --help && \
cnidaria.py --help \
\
'

# && make clean && make all -j 1
#CMD /bin/bash -c if [[ -z "$USER_UID" ]]; then echo USER ID $USER_UID; fi

touch ok
