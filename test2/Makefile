KMER_SIZE=21
NUM_PIECES=1
HASH_SIZE=1G
LOWER_COUNT=2

ifdef SAMPLEDATA
HASH_SIZE=256M
endif

ifdef NOIMAGE
DOIMAGE="--no-gen-image"
else
DOIMAGE=
endif


CURR_DIR_N=$(abspath $(lastword $(MAKEFILE_LIST)))
CURR_DIR=$(patsubst %/,%,$(dir $(CURR_DIR_N)))

DATAFOLDER=$(CURR_DIR)/data

FILE_LIST=$(CURR_DIR)/filelist.csv
DEF_FILE=$(CURR_DIR)/test_def.csv

OUT_DIR=$(CURR_DIR)/out

JELLYFISH=$(CURR_DIR)/../src/libs/Jellyfish/bin/jellyfish

COUNTER_LEN=7
OUT_COUNTER_LEN=1
#JCMD="${JELLYFISH} count -m ${MER_SIZE} -s ${HASH_SIZE} -t 5 -F 300 --disk --counter-len=${COUNTER_LEN} --out-counter-len=${OUT_COUNTER_LEN} --canonical"
#ulimit -Sn 4096


OUT_MAKE=$(OUT_DIR)/Makefile
OUT_FILE=$(OUT_DIR)/test/test.json

INFOLDERS=$(wildcard $(DATAFOLDER)/*)

INJF=$(patsubst %,%/$(KMER_SIZE).jf,$(INFOLDERS))


SHELL:=/bin/bash

 
all: $(OUT_FILE)


clean:
	rm $(DATAFOLDER)/*/*.jf
	rm -rf $(OUT_DIR)/*


print:
	@echo CURR_DIR   $(CURR_DIR)
	@echo DATAFOLDER $(DATAFOLDER)
	@echo FILE_LIST  $(FILE_LIST)
	@echo DEF_FILE   $(DEF_FILE)
	@echo OUT_DIR    $(OUT_DIR)
	@echo KMER_SIZE  $(KMER_SIZE)
	@echo NUM_PIECES $(NUM_PIECES)
	@echo OUT_MAKE   $(OUT_MAKE)
	@echo OUT_FILE   $(OUT_FILE)
	@echo INFOLDERS  $(INFOLDERS)
	@echo
	@echo INJF       $(INJF)


.PHONY: json makefile fastas maker jfs

json: $(OUT_FILE)

maker: $(OUT_MAKE)

jfs: $(INJF)

fastas: $(INFA)


#$(DATAFOLDER)/%.fasta: $(DATAFOLDER)/%.sh
#	test -f $@ || ( cd $(DATAFOLDER) && bash $? && test -e $@ )



ifdef SAMPLEDATA
$(DATAFOLDER)/%/$(KMER_SIZE).jf: $(DATAFOLDER)/%/*.fq.gz
	gunzip -k $? | head -40000 | gzip -1 > $(DATAFOLDER)/$*/head.fq.gz
	test -f $@ || ( cd $(DATAFOLDER)/$* && ulimit -Sn 4096 && ${JELLYFISH} count -m $(KMER_SIZE) -s $(HASH_SIZE) --lower-count=$(LOWER_COUNT) -t 5 -F 300 --disk --counter-len=$(COUNTER_LEN) --out-counter-len=$(OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming head.fq.gz && mv $@.tmp $@ )
else
$(DATAFOLDER)/%/$(KMER_SIZE).jf: $(DATAFOLDER)/%/*.fq.gz
	test -f $@ || ( cd $(DATAFOLDER)/$* && ulimit -Sn 4096 && ${JELLYFISH} count -m $(KMER_SIZE) -s $(HASH_SIZE) --lower-count=$(LOWER_COUNT) -t 5 -F 300 --disk --counter-len=$(COUNTER_LEN) --out-counter-len=$(OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming <(pigz -kcd $?) && mv $@.tmp $@ )
endif



$(FILE_LIST): $(INJF)
	echo $(INJF) | tr " " "\n" | xargs -n1 -L1 -I{} bash -c 'dn=`dirname {}`; bn=`basename $$dn`; echo -e "{}\t$$bn"' > $@.tmp && mv $@.tmp $@

$(DEF_FILE): $(INJF)
	echo $(INJF) | tr " " "\n" | xargs -n1 -L1 -I{} bash -c 'echo -e "test\t{}"' > $@.tmp && mv $@.tmp $@

$(OUT_MAKE): $(FILE_LIST) $(DEF_FILE)
	../scripts/gen_mkfile.py $(FILE_LIST) $(DEF_FILE) $(OUT_DIR) $(KMER_SIZE) $(NUM_PIECES) $(DOIMAGE)

$(OUT_FILE): $(OUT_MAKE) $(INJF)
	$(MAKE) -C $(OUT_DIR)/test

