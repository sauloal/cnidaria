DATAFOLDER=$(PWD)/data/fungi
FILE_LIST=filelist.csv
DEF_FILE=test_def.csv
OUT_DIR=out
KMER_SIZE=21
NUM_PIECES=1

JELLYFISH=$(PWD)/../src/libs/Jellyfish/bin/jellyfish
HASH_SIZE=1G
COUNTER_LEN=7
OUT_COUNTER_LEN=1
#JCMD="${JELLYFISH} count -m ${MER_SIZE} -s ${HASH_SIZE} -t 5 -F 300 --disk --counter-len=${COUNTER_LEN} --out-counter-len=${OUT_COUNTER_LEN} --canonical"
#ulimit -Sn 4096


OUT_MAKE=$(OUT_DIR)/Makefile
OUT_FILE=$(OUT_DIR)/test/test.json

INSH=$(wildcard $(DATAFOLDER)/*.sh)

INFA=$(patsubst %.sh,%.fasta,$(INSH))

INJF=$(patsubst %.sh,%.fasta.$(KMER_SIZE).jf,$(INSH))




all: $(OUT_FILE)


clean:
	rm $(DATAFOLDER)/*.jf
	rm -rf $(OUT_DIR)/*


print:
	@echo DATAFOLDER $(DATAFOLDER)
	@echo FILE_LIST  $(FILE_LIST)
	@echo DEF_FILE   $(DEF_FILE)
	@echo OUT_DIR    $(OUT_DIR)
	@echo KMER_SIZE  $(KMER_SIZE)
	@echo NUM_PIECES $(NUM_PIECES)
	@echo OUT_MAKE   $(OUT_MAKE)
	@echo OUT_FILE   $(OUT_FILE)
	@echo INSH       $(INSH)
	@echo
	@echo INFA       $(INFA)
	@echo
	@echo INJF       $(INJF)


$(DATAFOLDER)/%.fasta: $(DATAFOLDER)/%.sh
	cd $(DATAFOLDER) && bash $? && test -e $@


$(DATAFOLDER)/%.fasta.$(KMER_SIZE).jf: $(DATAFOLDER)/%.fasta
	cd $(DATAFOLDER) && ulimit -Sn 4096 && ${JELLYFISH} count -m $(KMER_SIZE) -s $(HASH_SIZE) -t 5 -F 300 --disk --counter-len=$(COUNTER_LEN) --out-counter-len=$(OUT_COUNTER_LEN) --canonical -o $@.tmp --timing=$@.timming $? && mv $@.tmp $@ 


$(OUT_MAKE): $(FILE_LIST) $(DEF_FILE)
	../scripts/gen_mkfile.py $(FILE_LIST) $(DEF_FILE) $(OUT_DIR) $(KMER_SIZE) $(NUM_PIECES)


$(OUT_FILE): $(OUT_MAKE) $(INJF)
	$(MAKE) -C $(OUT_DIR) all

