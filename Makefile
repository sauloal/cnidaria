

.PHONY: cnidaria jellyfish run test

all: cnidaria jellyfish run test

clean:
	$(MAKE) -C src clean
	$(MAKE) -C src/libs/Jellyfish clean
	$(MAKE) -C test clean
    

cnidaria:
	$(MAKE) -C src

jellyfish:
	$(MAKE) -C src/libs/Jellyfish

run:
	scripts/cnidaria.py -h

test:
	$(MAKE) -C test
