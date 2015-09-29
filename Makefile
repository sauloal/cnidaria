.PHONY: jelly cnidaria run test

all: jelly cnidaria run test

clean:
	$(MAKE) -C src  clean
	$(MAKE) -C test clean
    
jelly:
	$(MAKE) -C src jelly

cnidaria:
	$(MAKE) -C src build

run: cnidaria jelly
	scripts/cnidaria.py -h

test:
	$(MAKE) -C test
