set -xeu

cat ../trees/*.upgma.filtered.nwk > all.upgma.nwk
cat ../trees/*.nj.filtered.nwk    > all.nj.nwk

cat "../trees/S10_homozygous SNPs in 10 domestication genes_names_fixed.nwk.filtered.nwk" >> all.upgma.nwk
cat "../trees/S10_homozygous SNPs in 10 domestication genes_names_fixed.nwk.filtered.nwk" >> all.nj.nwk

cat "../trees/F5_whole genome snp 20140611_names_fixed.nwk.filtered.nwk" >> all.upgma.nwk
cat "../trees/F5_whole genome snp 20140611_names_fixed.nwk.filtered.nwk" >> all.nj.nwk

java -jar bin/TreeCmp.jar -m -d ms rf pd qt mc rc ns  tt mp -i all.upgma.nwk -o all.upgma.normalized.csv -N -I
java -jar bin/TreeCmp.jar -m -d ms rf pd qt mc rc ns  tt mp -i all.nj.nwk    -o all.nj.normalized.csv    -N -I
