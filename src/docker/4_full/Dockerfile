FROM cnidaria_run

RUN git clone https://github.com/sauloal/cnidaria.git

RUN cd cnidaria/src && \
    make clean && \
    make all && \
    cd libs/jellyfish-2.1.3 && \
    ./configure && \
    make

RUN cd cnidaria/scripts && \
    ./cnidaria.py -h

VOLUME "/data"
