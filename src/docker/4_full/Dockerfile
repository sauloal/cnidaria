FROM sauloal/cnidaria_run

RUN useradd --create-home --shell /bin/bash cnidaria && \
    echo `echo "cnidaria\ncnidaria\n" | passwd cnidaria` \
    adduser docker sudo

USER cnidaria

WORKDIR /home/cnidaria

RUN git clone https://github.com/sauloal/cnidaria.git && \
    cd cnidaria && \
    make cnidaria jellyfish run

#    cd cnidaria/src && \
#    make clean && \
#    make all && \
#    cd libs/jellyfish-2.1.3 && \
#    ./configure && \
#    make && \
#    cd ../../../scripts && \
#    ./cnidaria.py -h && \
#    mkdir ~cnidaria/data

VOLUME "/home/cnidaria/cnidaria/data"

WORKDIR /home/cnidaria/cnidaria

CMD ["/usr/bin/bash"]
