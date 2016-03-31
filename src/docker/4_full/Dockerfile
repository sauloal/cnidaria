FROM sauloal/cnidaria_run

RUN useradd --create-home --shell /bin/bash cnidaria && \
    echo `echo "cnidaria\ncnidaria\n" | passwd cnidaria` \
    adduser docker sudo

#RUN ln -snf /bin/bash /bin/sh

USER cnidaria

WORKDIR /home/cnidaria

RUN git clone https://github.com/sauloal/cnidaria.git

ENV PATH=/home/cnidaria/cnidaria/scripts:/home/cnidaria/cnidaria/src/libs/Jellyfish/bin/:$PATH

VOLUME "/home/cnidaria/cnidaria/data"

WORKDIR /home/cnidaria/cnidaria

CMD ["/bin/bash"]

#   cd cnidaria && \
#    ls && \
#    cat ./enable.sh >> /home/cnidaria/.bashrc && \
#    cat /home/cnidaria/.bashrc && \
#    printenv

# && \
#GEN_SHARED=true make jelly cnidaria run

#    cd cnidaria/src && \
#    make clean && \
#    make all && \
#    cd libs/jellyfish-2.1.3 && \
#    ./configure && \
#    make && \
#    cd ../../../scripts && \
#    ./cnidaria.py -h && \
#    mkdir ~cnidaria/data
