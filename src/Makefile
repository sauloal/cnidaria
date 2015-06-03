KMER_SIZE=21
#GEN_DEBUG=false
#GEN_SHARED=false



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

#CPP_INCL=-I/usr/lib/x86_64-linux-gnu 
CPP_INCL= \
		-I$(LIB_EXT)/Jellyfish \
		-I$(LIB_EXT)/Jellyfish/include \
		-I$(LIB_EXT)/Jellyfish/include/jellyfish \
		-I$(LIB_EXT)/rapidjson/include \
		-I$(LIB_EXT)/threadpool \
		-I$(LIB_SRC) \
		-I$(SRC_CPP) \
		-I/home/aflit001/lib/include \
		-I/usr/include/python2.7



ifdef GEN_SHARED
CPP_LIBS=-L/usr/lib/x86_64-linux-gnu -fopenmp -lboost_system -lboost_filesystem -lboost_thread -lpthread
else
CPP_LIBS=-fopenmp -Wl,-rpath,'$$ORIGIN/static' static/*.so -static-libgcc -static-libstdc++ -Wl,-Bstatic -lc -Wl,-Bdynamic
#-Wl,--dynamic-linker=static/ld-2.19.so 
endif



CPP_VARS=-DKMER_SIZE=$(KMER_SIZE)
CPP_VARS=

ifdef GEN_DEBUG
CPP_VARS+= -DDEBUG
endif

LDD_OPTS=



CFLAGS=''
LDFLAGS=''
ifdef GEN_SHARED
LD_LIBRARY_PATH=''
LD_LIBRARY_PATH=$(PWD)/static/
LIBRARY_PATH=''
LIBRARY_PATH=$(PWD)/static/
endif



JELLY_LIB=$(LIB_EXT)/Jellyfish/lib

J_SRC=  $(JELLY_LIB)/allocators_mmap.cc           \
        $(JELLY_LIB)/jsoncpp.cc                   \
        $(JELLY_LIB)/mer_dna.cc                   \
        $(JELLY_LIB)/rectangular_binary_matrix.cc

J_OBJ=$(J_SRC:.cc=.o  )


HEADERS=$(LIB_SRC)/*.hpp $(LIB_SRC)/*.h $(LIB_SRC)/*.cpp






.PHONY: all clean

ifdef GEN_DEBUG
all: cnidaria build jelly
else
all: build jelly
endif

clean: clean_swig
	rm -v cnidaria core $(SRC_CPP)/* $(SRC_OBJ)/* $(JELLY_LIB)/*.o || true
	rm -v $(BUILD_DIR)/cnidariapy.py  $(BUILD_DIR)/_cnidariapy.so  || true




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


UNIFIED=unified.a
COMPLETE=all.a

$(UNIFIED): $(OPPS) $(J_OBJ)
	ar crf $@ $^


.PHONY: cpps
cpps: $(CPPS) $(HPPS)

$(SRC_CPP)/%.cpp $(SRC_CPP)/%.hpp: $(SRC_LZZ)/%.lzz
	mkdir -p $(SRC_CPP) || true
	lzz/lzz -e $(CPP_VARS) -hx 'hpp' -I $(CPP_INCL) -c -o $(SRC_CPP) $<

$(SRC_OBJ)/%.o: $(SRC_CPP)/%.cpp $(SRC_CPP)/%.hpp $(HEADERS)
	mkdir -p $(SRC_OBJ) || true
	$(CPP) -c $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $< -o $@ 2>&1

$(JELLY_LIB)/%.o: $(JELLY_LIB)/%.cc
	$(CPP) -c $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $< -o $@ 2>&1

$(JELLY_LIB)/%.o: $(JELLY_LIB)/%.cpp
	$(CPP) -c $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $< -o $@ 2>&1

cnidaria: $(UNIFIED)
	$(CPP) $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) $(LDD_OPTS) -o $@ $(UNIFIED) $(CPP_LIBS) 2>&1





$(COMPLETE): $(OPPS) $(J_OBJ) $(SRC_OBJ)/cnidariapy_wrap.o
	ar crf $@ $^




.PHONY: swig
swig: cnidariapy.py

clean_swig:
	rm $(SRC_CPP)/cnidariapy.py $(SRC_CPP)/cnidariapy_wrap.cxx _cnidariapy.so cnidariapy.py || true

$(SRC_CPP)/cnidariapy_wrap.cxx: $(LIB_SRC)/cnidariapy.i $(SRC_CPP)/cnidaria.cpp
	swig -c++ -python -outdir $(SRC_CPP)/ -I$(SRC_CPP)/ -o $(SRC_CPP)/cnidariapy_wrap.cxx $(LIB_SRC)/cnidariapy.i

$(SRC_OBJ)/cnidariapy_wrap.o: $(SRC_CPP)/cnidariapy_wrap.cxx
	$(CPP) -c $< $(CPP_OPTS) $(CPP_INCL) $(CPP_VARS) -o $@ 1>&1

#_cnidariapy.so: $(OPPS) $(J_OBJ) $(SRC_OBJ)/cnidariapy_wrap.o
_cnidariapy.so: $(COMPLETE)
	@#-fvisibility=hidden
	@#$(CPP) -shared -Xlinker $(CPP_INCL) $(CPP_VARS) $^ -o $@ $(CPP_LIBS)
	@#$(CPP) -shared -Wl,-Bsymbolic -Wl,-E -Wl,-soname,$@ $(CPP_INCL) $(CPP_VARS) $^ -o $@ $(CPP_LIBS)
	$(CPP) -shared -Wl,-Bsymbolic -Wl,-E -Wl,-soname,$@ $(CPP_INCL) $(CPP_VARS) -Wl,--whole-archive $^ -Wl,--no-whole-archive -o $@ $(CPP_LIBS) $(CPP_INCL)

cnidariapy.py: _cnidariapy.so
	cp $(SRC_CPP)/cnidariapy.py cnidariapy.py



.PHONY: jelly
jelly:
	$(MAKE) -C $(LIB_EXT)/Jellyfish -f Makefile_static config CFLAGS='' LDFLAGS='' LD_LIBRARY_PATH='' LIBRARY_PATH=''
	$(MAKE) -C $(LIB_EXT)/Jellyfish
	$(MAKE) -C $(LIB_EXT)/Jellyfish -f Makefile_static




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

