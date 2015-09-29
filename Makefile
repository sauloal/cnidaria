.PHONY: cnidaria run test

all: cnidaria run test

clean:
	$(MAKE) -C src  clean
	$(MAKE) -C test clean
    
cnidaria:
	$(MAKE) -C src build

run: cnidaria jellyfish
	scripts/cnidaria.py -h

test:
	$(MAKE) -C test
