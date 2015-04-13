

.PHONY: cnidaria jellyfish run test

all: cnidaria jellyfish run test

clean:
	$(MAKE) -C src clean
	$(MAKE) -C src/libs/Jellyfish clean
	$(MAKE) -C test clean
    

cnidaria:
	$(MAKE) -C src

jellyfish:
	cd src/libs/Jellyfish && ./configure && $(MAKE)

run:
	scripts/cnidaria.py -h

test:
	$(MAKE) -C test
