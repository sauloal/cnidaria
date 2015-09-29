set -xeu

cd data

find . -name *.fasta | xargs -I{} bash -c 'f={}; bn=`basename $f`; ap=`echo $f | sed "s/\.fasta//"`; echo $f $bn $ap; mkdir $ap; mv $f ap'

