.PHONY: cnidaria jellyfish run test

all: cnidaria jellyfish run test

clean:
	$(MAKE) -C src clean
	$(MAKE) -C test clean
    
cnidaria:
	$(MAKE) -C src build

jellyfish:
	$(MAKE) -C src jelly

run: cnidaria jellyfish
	scripts/cnidaria.py -h

test:
	$(MAKE) -C test
