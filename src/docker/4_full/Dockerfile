FROM sauloal/cnidaria_run

RUN useradd --create-home --shell /bin/bash cnidaria && \
    echo `echo "cnidaria\ncnidaria\n" | passwd cnidaria`

USER cnidaria

WORKDIR /home/cnidaria

RUN git clone https://github.com/sauloal/cnidaria.git && \
    cd cnidaria/src && \
    make clean && \
    make all && \
    cd libs/jellyfish-2.1.3 && \
    ./configure && \
    make && \
    cd ../../../scripts && \
    ./cnidaria.py -h && \
    mkdir ~cnidaria/data

VOLUME "/home/cnidaria/data"
