KMER_SIZE=21
#GEN_DEBUG=false

SRC_LZZ=src_lzz
SRC_CPP=src_cpp
SRC_OBJ=src_obj
LIB_SRC=headers
LIB_EXT=libs
BUILD_DIR=build



SRCS=\
header_r.lzz \
jelly.lzz \
header_w.lzz \
cnidaria_methods.lzz \
cnidaria.lzz

ifdef GEN_DEBUG
SRCS+= cnidaria_debug.lzz
endif



LZZS=$(SRCS:%=$(SRC_LZZ)/%)
CPPST=$(SRCS:%=$(SRC_CPP)/%)
OPPST=$(SRCS:%=$(SRC_OBJ)/%)

CPPS=$(CPPST:.lzz=.cpp)
HPPS=$(CPPST:.lzz=.hpp)
OPPS=$(OPPST:.lzz=.o  )


CPP=g++

DEBUG=-g -pg
DEBUG=-g
#DEBUG=

JELLY_LIB=$(LIB_EXT)/Jellyfish/lib
JELLY_LIB=$(LIB_EXT)/jelly


CPP_OPTS=$(DEBUG) -std=c++11 -m64 -fPIC -mtune=native

#CPP_OPTS+=	-faggressive-loop-optimizations -fexpensive-optimizations \
#			-fearly-inlining                -ffast-math \
#			-floop-parallelize-all          -funsafe-loop-optimizations \
#			-funsafe-math-optimizations     -ftree-vectorize \
#			-fno-strict-aliasing  			-fwrapv \
#			-msse4.2                        -Wall

#CPP_OPTS+=-O3
CPP_OPTS+=-Ofast
#CPP_OPTS+=-O0    

CPP_INCL=-I/usr/lib/x86_64-linux-gnu \
		-I$(LIB_EXT)/rapidjson/include \
		-I$(LIB_EXT)/threadpool \
        -I$(JELLY_LIB) \
		-I$(LIB_SRC) \
		-I$(SRC_CPP) \
		-I$HOME/include \
		-I/usr/include/python2.7

#		-I$(LIB_EXT)/Jellyfish \
#		-I$(LIB_EXT)/Jellyfish/include \
#		-I$(LIB_EXT)/Jellyfish/include/jellyfish \


CPP_LIBS=-L/usr/lib/x86_64-linux-gnu -fopenmp -lboost_system -lboost_filesystem -lboost_thread -lpthread


ifdef GEN_DEBUG
CPP_VARS=-DKMER_SIZE=$(KMER_SIZE)
CPP_VARS+= -DDEBUG
endif

LDD_OPTS=








J_SRC=  $(JELLY_LIB)/allocators_mmap.cc           \
        $(JELLY_LIB)/jsoncpp.cc                   \
        $(JELLY_LIB)/mer_dna.cc                   \
        $(JELLY_LIB)/rectangular_binary_matrix.cc

J_OBJ=$(J_SRC:.cc=.o  )

HEADERS=$(LIB_SRC)/*.hpp $(LIB_SRC)/*.h $(LIB_SRC)/*.cpp







.PHONY: all clean

ifdef GEN_DEBUG
all: cnidaria build
else
all: build
endif

clean: clean_swig
	rm cnidaria core $(SRC_CPP)/* $(SRC_OBJ)/* $(JELLY_LIB)/*.o || true
	rm -rf $(BUILD_DIR) || true

.PHONY: vars

vars:
	echo SRC_CPP $(SRC_CPP)
	echo SRC_LZZ $(SRC_LZZ)
	echo SRC_OBJ $(SRC_OBJ)
	echo LIB_SRC $(LIB_SRC)
	echo LIB_EXT $(LIB_EXT)
	echo SRCS    $(SRCS)
	echo LZZS    $(LZZS)
	echo CPPS    $(CPPS)
	echo HPPS    $(HPPS)
	echo OPPS    $(OPPS)
	echo HEADERS $(HEADERS)






.PHONY: cpps
cpps: $(CPPS) $(HPPS)


$(SRC_CPP)/%.cpp $(SRC_CPP)/%.hpp: $(SRC_LZZ)/%.lzz
	mkdir -p $(SRC_CPP) || true
	lzz/lzz -e $(CPP_VARS) -hx 'hpp' -I $(CPP_INCL) -c -o $(SRC_CPP) $<

$(SRC_OBJ)/%.o: $(SRC_CPP)/%.cpp $(SRC_CPP)/%.hpp $(HEADERS)
	mkdir -p $(SRC_OBJ) || true
	$(CPP) -c $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $< -o $@ $(CPP_LIBS) 2>&1

$(JELLY_LIB)/%.o: $(JELLY_LIB)/%.cc
	$(CPP) -c $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $< -o $@ $(CPP_LIBS) 2>&1

$(JELLY_LIB)/%.o: $(JELLY_LIB)/%.cpp
	$(CPP) -c $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $< -o $@ $(CPP_LIBS) 2>&1

cnidaria: $(OPPS) $(J_OBJ)
	$(CPP)    $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $(LDD_OPTS)    -o $@      -static                           $(OPPS) $(J_OBJ) $(CPP_LIBS) 2>&1





.PHONY: swig
swig: cnidariapy.py

clean_swig:
	rm $(SRC_CPP)/cnidariapy.py $(SRC_CPP)/cnidariapy_wrap.cxx _cnidariapy.so cnidariapy.py || true

$(SRC_CPP)/cnidariapy_wrap.cxx: $(LIB_SRC)/cnidariapy.i $(SRC_CPP)/cnidaria.cpp
	swig -c++ -python -outdir $(SRC_CPP)/ -I$(SRC_CPP)/ -o $(SRC_CPP)/cnidariapy_wrap.cxx $(LIB_SRC)/cnidariapy.i

$(SRC_OBJ)/cnidariapy_wrap.o: $(SRC_CPP)/cnidariapy_wrap.cxx $(OPPS) $(J_OBJ)
	$(CPP) -c $< $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $(CPP_LIBS) -o $@ 2>&1

_cnidariapy.so: $(SRC_OBJ)/cnidariapy_wrap.o
	@#-fvisibility=hidden
	$(CPP) -shared -Xlinker $(CPP_INCL) $(CPP_VARS) $(OPPS) $(J_OBJ) $< -o $@ $(CPP_LIBS)

cnidariapy.py: _cnidariapy.so
	cp $(SRC_CPP)/cnidariapy.py cnidariapy.py




.PHONY: build
build: cnidariapy.py _cnidariapy.so
	mkdir -p $(BUILD_DIR)
	cp cnidariapy.py  $(BUILD_DIR)/cnidariapy.py 
	cp _cnidariapy.so $(BUILD_DIR)/_cnidariapy.so




.PHONY: run
run: cnidaria
	./cnidaria | tee cnidaria.log

.PHONY: python
python:
	rm -rf build/ || true
	python setup.py build


#.PHONY: jelly
#jelly: $(LIB_EXT)/Jellyfish/bin/jellyfish
#
#$(LIB_EXT)/Jellyfish/bin/jellyfish:
#	cd $(LIB_EXT)/Jellyfish
#	./configure
#	cd ..
#	$(MAKE) -C Jellyfish

#$(J_OBJ):
#	cd $(LIB_EXT)/Jellyfish
#	./configure
#	cd ..
#	$(MAKE) -C Jellyfish
#
#%.o: %.cc
#	$(CPP) -c $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $(CPP_LIBS) $< -o $@

