set -xeu

find . -name '*.jf' | xargs -n 1 ~/dev/phylogenomics2/jfreader.py QUERY -s -i > stats.log

perl -ne 'if (/"size"\:(\d+)/) { print $1, "\n"; }' stats.log > stats.log.lst

sort -u stats.log.lst > stats.log.lst.uniq
