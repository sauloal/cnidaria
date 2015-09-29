####
# ENVIRONMENT VARIABLES
####
DATA_BASE             ?= data
OUT_BASE              ?= out
OUT_FOLDER            ?= test
NUM_SAMPLE_ROWS       ?= 40000

CNIDARIA_NUM_PIECES   ?= 1
CNIDARIA_EXTRA_FILES  ?=

JELLY_KMER_SIZE       ?= 21
JELLY_HASH_SIZE       ?= 1G
JELLY_LOWER_COUNT_FA  ?= 1
JELLY_LOWER_COUNT_FQ  ?= 2
JELLY_THREADS         ?= 5
JELLY_COUNTER_LEN     ?= 7
JELLY_OUT_COUNTER_LEN ?= 1
JELLY_NUM_FILES       ?= 300


# CREATE FULL DATABASE (SLOW)
ifdef CNIDARIA_GENDB
DODB=--export-complete
else
DODB=
endif

# SAMPLE THE DATA
ifdef SAMPLEDATA
JELLY_HASH_SIZE=256M
endif

# DO NOT EXPORT IMAGES
ifdef CNIDARIA_NOIMAGE
DOIMAGE="--no-gen-image"
else
DOIMAGE=
endif




####
# PROGRAMS
####
PIGZ:=$(shell which pigz &>/dev/null)
ifdef PIGZ
    $(info USING PIGZ $(PIGZ))
    COMPRESS=pigz --keep -1
    DECOMPRESS=pigz --keep --stdout --decompress
else
    $(info USING GZIP $(PIGZ))
    COMPRESS=gzip --stdout -1
    DECOMPRESS=gunzip --stdout
endif




####
# WORK VARIABLES
####
CURR_DIR_N=$(abspath $(lastword $(MAKEFILE_LIST)))
CURR_DIR=$(patsubst %/,%,$(dir $(CURR_DIR_N)))

DATA_FOLDER=$(CURR_DIR)/$(DATA_BASE)

FILE_LIST=$(CURR_DIR)/$(OUT_FOLDER)_filelist.csv
DEF_FILE=$(CURR_DIR)/$(OUT_FOLDER)_def.csv

OUT_DIR=$(CURR_DIR)/$(OUT_BASE)/$(OUT_FOLDER)

JELLYFISH=$(CURR_DIR)/../src/libs/Jellyfish/bin/jellyfish

OUT_MAKE=$(OUT_DIR)/Makefile
OUT_FILE=$(OUT_DIR)/$(OUT_FOLDER)/$(OUT_FOLDER).json

#INFOLDERS=$(wildcard $(DATA_FOLDER)/*)
INFOLDERS=${shell find $(DATA_FOLDER) -mindepth 1 -type d -print}

INJF=$(patsubst %,%/$(JELLY_KMER_SIZE).jf,$(INFOLDERS))
INCNE=$(wildcard $(DATA_FOLDER)/*.cne)

SHELL:=/bin/bash



 
####
# RULES
####
all: $(OUT_FILE)


clean:
	rm $(DATA_FOLDER)/*/*.jf
	rm -rf $(OUT_DIR)/*


print:
	@echo "JELLY_KMER_SIZE       $(JELLY_KMER_SIZE)"
	@echo "JELLY_HASH_SIZE       $(JELLY_HASH_SIZE)"
	@echo "JELLY_LOWER_COUNT_FA  $(JELLY_LOWER_COUNT_FA)"
	@echo "JELLY_LOWER_COUNT_FQ  $(JELLY_LOWER_COUNT_FQ)"
	@echo "JELLY_THREADS         $(JELLY_THREADS)"
	@echo "JELLY_COUNTER_LEN     $(JELLY_COUNTER_LEN)"
	@echo "JELLY_OUT_COUNTER_LEN $(JELLY_OUT_COUNTER_LEN)"
	@echo "JELLY_NUM_FILES       $(JELLY_NUM_FILES)"
	@echo
	@echo "CNIDARIA_NUM_PIECES   $(CNIDARIA_NUM_PIECES)"
	@echo "CNIDARIA_EXTRA_FILES  $(CNIDARIA_EXTRA_FILES)"

ifdef CNIDARIA_NOIMAGE
	@echo "CNIDARIA_NOIMAGE      true"
else
	@echo "CNIDARIA_NOIMAGE      false"
endif


ifdef CNIDARIA_GENDB
	@echo "CNIDARIA_NOIMAGE      true"
else
	@echo "CNIDARIA_NOIMAGE      false"
endif


ifdef SAMPLEDATA
	@echo
	@echo "NUM_SAMPLE_ROWS       $(NUM_SAMPLE_ROWS)"
endif

	@echo
	@echo "CURR_DIR              $(CURR_DIR)"
	@echo "DATA_BASE             $(DATA_BASE)"
	@echo "DATA_FOLDER           $(DATA_FOLDER)"
	@echo "FILE_LIST             $(FILE_LIST)"
	@echo "DEF_FILE              $(DEF_FILE)"
	@echo "OUT_MAKE              $(OUT_MAKE)"
	@echo "OUT_BASE              $(OUT_BASE)"
	@echo "OUT_FILE              $(OUT_FILE)"
	@echo "OUT_DIR               $(OUT_DIR)"
	@echo "OUT_FOLDER            $(OUT_FOLDER)"
	@echo
	@echo "INFOLDERS             $(INFOLDERS)"
	@echo
	@echo "INJF                  $(INJF)"
	@echo "INCNE                 $(INCNE)"


help:
	@echo all, clean, print, help, json, maker, jfs
	@echo 
	@echo 
	@echo "DATA_BASE             ?= data  - base path for input"
	@echo "OUT_BASE              ?= out   - base path for output"
	@echo "OUT_FOLDER            ?= test  - project name"
	@echo "NUM_SAMPLE_ROWS       ?= 40000 - number of rows to sample if sampling, must be multiple of 4"
	@echo "SAMPLEDATA                     - sample the data"
	@echo 
	@echo "CNIDARIA_NUM_PIECES   ?= 1     - number of pieces for cnidaria to multithread"
	@echo "CNIDARIA_NOIMAGE               - do not export images"
	@echo "CNIDARIA_GENDB                 - create full database [slow]"
	@echo "CNIDARIA_EXTRA_FILES           - add extra files to cnidaria"
	@echo 
	@echo "JELLY_KMER_SIZE       ?= 21    - kmer size"
	@echo "JELLY_HASH_SIZE       ?= 1G    - hash size"
	@echo "JELLY_LOWER_COUNT_FA  ?= 1     - lower count for fastA files"
	@echo "JELLY_LOWER_COUNT_FQ  ?= 2     - lower count for fastQ files"
	@echo "JELLY_THREADS         ?= 5     - number of threads"
	@echo "JELLY_COUNTER_LEN     ?= 7     - counter len"
	@echo "JELLY_OUT_COUNTER_LEN ?= 1     - out counter len"
	@echo "JELLY_NUM_FILES       ?= 300   - number of disk files"


.PHONY: json maker jfs

json: $(OUT_FILE)

maker: $(OUT_MAKE)

jfs: $(INJF)


#$(DATA_FOLDER)/%.fasta: $(DATA_FOLDER)/%.sh
#	test -f $@ || ( cd $(DATA_FOLDER) && bash $? && test -e $@ )



ifdef SAMPLEDATA
$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fq.gz
	$(DECOMPRESS) $? | head -$(NUM_SAMPLE_ROWS) | $(COMPRESS) > $(DATA_FOLDER)/$*/head.fqh.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FQ) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) head.fqh.gz) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fastq.gz
	$(DECOMPRESS) $? | head -$(NUM_SAMPLE_ROWS) | $(COMPRESS) > $(DATA_FOLDER)/$*/head.fqh.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FQ) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) head.fqh.gz) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fasta.gz
	$(DECOMPRESS) $? | head -$(NUM_SAMPLE_ROWS) | $(COMPRESS) > $(DATA_FOLDER)/$*/head.fah.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FA) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) head.fah.gz) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fa.gz
	$(DECOMPRESS) $? | head -$(NUM_SAMPLE_ROWS) | $(COMPRESS) > $(DATA_FOLDER)/$*/head.fah.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FQ) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <(pigz -kcd head.fah.gz) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fasta
	head -$(NUM_SAMPLE_ROWS) $? | $(COMPRESS) > $(DATA_FOLDER)/$*/head.fah.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FA) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) head.fah.gz) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fa
	head -$(NUM_SAMPLE_ROWS) $? | $(COMPRESS) > $(DATA_FOLDER)/$*/head.fah.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FQ) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) head.fah.gz) && mv $@.tmp $@ )


else
$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fq.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FQ) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) $?) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fastq.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FQ) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) $?) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fasta.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FA) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) $?) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fa.gz
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FA) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <($(DECOMPRESS) $?) && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fasta
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FA) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming $? && mv $@.tmp $@ )

$(DATA_FOLDER)/%/$(JELLY_KMER_SIZE).jf: $(DATA_FOLDER)/%/*.fa
	test -f $@ || ( cd $(DATA_FOLDER)/$* && ulimit -Sn 4096 && $(JELLYFISH) count -m $(JELLY_KMER_SIZE) -s $(JELLY_HASH_SIZE) --lower-count=$(JELLY_LOWER_COUNT_FA) -t $(JELLY_THREADS) -F $(JELLY_NUM_FILES) --disk --counter-len=$(JELLY_COUNTER_LEN) --out-counter-len=$(JELLY_OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming $? && mv $@.tmp $@ )


endif





$(OUT_MAKE): $(INJF) $(INCNE)
	echo $(INJF)                                  | tr " " "\n" |                   xargs -n1 -L1 -I{} bash -c 'dn=`dirname {}`; bn=`basename $$dn`; echo -e "{}\t$$bn"'  > $(FILE_LIST).tmp && mv $(FILE_LIST).tmp $(FILE_LIST)
	echo $(CNIDARIA_EXTRA_FILES) $(INCNE)         | tr " " "\n" |                   xargs -n1 -L1 -I{} bash -c '                 bn=`basename {}`;   echo -e "{}\t$$bn"' >> $(FILE_LIST)
	echo $(INJF) $(CNIDARIA_EXTRA_FILES) $(INCNE) | tr " " "\n" | sed 's/\.cne//' | xargs -n1 -L1 -I{} bash -c 'echo -e "$(OUT_FOLDER)\t{}"' > $(DEF_FILE).tmp && mv $(DEF_FILE).tmp $(DEF_FILE)
	$(CURR_DIR)/../scripts/gen_mkfile.py $(FILE_LIST) $(DEF_FILE) $(OUT_DIR) $(JELLY_KMER_SIZE) $(CNIDARIA_NUM_PIECES) $(DOIMAGE) $(DODB)


$(OUT_FILE): $(OUT_MAKE) $(INJF)
	$(MAKE) -C $(OUT_DIR)/$(OUT_FOLDER)

