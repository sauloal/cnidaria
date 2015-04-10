#rm */*.stats  */*/*.stats
#rm */*.jstats */*/*.jstats

#cout nucleotide composition
find . -name '*.fasta'   | xargs -P 30 -n 1 ~/dev/phylogenomics4/scripts/countChars.sh
find . -name '*.fas'     | xargs -P 30 -n 1 ~/dev/phylogenomics4/scripts/countChars.sh
find . -name '*.fa'      | xargs -P 30 -n 1 ~/dev/phylogenomics4/scripts/countChars.sh
find . -name '*.seq'     | xargs -P 30 -n 1 ~/dev/phylogenomics4/scripts/countChars.sh

find . -name '*.bam'     | xargs -P 10 -n 1 ~/dev/phylogenomics4/scripts/countChars.sh
find . -name '*.cram'    | xargs -P 10 -n 1 ~/dev/phylogenomics4/scripts/countChars.sh

#count number of sequences in fasta
find . -name '*.fasta'   | xargs -P 30 -n 1 -I{} bash -c 'if [[ ! -f "{}.count" ]]; then echo -n "{} " | tee {}.count.tmp ; grep ">" {} | wc -l | tee -a {}.count.tmp; mv {}.count.tmp {}.count; else echo {} already done; fi'
find . -name '*.fa'      | xargs -P 30 -n 1 -I{} bash -c 'if [[ ! -f "{}.count" ]]; then echo -n "{} " | tee {}.count.tmp ; grep ">" {} | wc -l | tee -a {}.count.tmp; mv {}.count.tmp {}.count; else echo {} already done; fi'
find . -name '*.fas'     | xargs -P 30 -n 1 -I{} bash -c 'if [[ ! -f "{}.count" ]]; then echo -n "{} " | tee {}.count.tmp ; grep ">" {} | wc -l | tee -a {}.count.tmp; mv {}.count.tmp {}.count; else echo {} already done; fi'
find . -name '*.seq'     | xargs -P 30 -n 1 -I{} bash -c 'if [[ ! -f "{}.count" ]]; then echo -n "{} " | tee {}.count.tmp ; grep ">" {} | wc -l | tee -a {}.count.tmp; mv {}.count.tmp {}.count; else echo {} already done; fi'

#count jellyfish statistics
find . -name '*.jf'      | xargs -P 5  -n 1 -I{} bash -c 'if [[ ! -f "{}.jstats" ]]; then echo "{}"; source jopts; $JELLYFISH stats {} | tee {}.jstats.tmp; mv {}.jstats.tmp {}.jstats; else echo {} already done; fi'

#count bam statsistics
find . -name '*.bam'     | xargs -P 10 -n 1 -I{} bash -c 'if [[ ! -f "{}.bstats" ]]; then echo "{}"; source jopts; $SAMTOOLS  stats {} | tee {}.bstats.tmp; mv {}.bstats.tmp {}.bstats; else echo {} already done; fi'
find . -name '*.cram'    | xargs -P 10 -n 1 -I{} bash -c 'if [[ ! -f "{}.bstats" ]]; then echo "{}"; source jopts; $SAMTOOLS  stats {} | tee {}.bstats.tmp; mv {}.bstats.tmp {}.bstats; else echo {} already done; fi'

#time samtools flagstat sa.fa.bam.filtered.bam
#time ../samtools/samtools-1.1/samtools stats 711.cram | tee 711.cram.bstats

rm nucStats.csv || true
#~/dev/phylogenomics4/parseCountCharsStats.py nucStats.csv */*.stats */*/*.stats */*.jstats */*/*.jstats */*.bstats */*/*.bstats */*.count */*/*.count
~/dev/phylogenomics4/scripts/parseCountCharsStats.py nucStats.csv */*.stats */*/*.stats */*.jstats */*/*.jstats */*.bstats */*.count */*/*.count
