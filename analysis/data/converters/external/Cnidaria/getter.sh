set -xeu

echo NAME $NAME
echo URLS $URLS

if [[ -z "$NAME" ]]; then
    echo "no name given"
    exit 1
fi

if [[ ! -f "$NAME.fasta" ]]; then
mkdir $NAME
cd $NAME
wget -O - $URLS | gunzip -kc > ../$NAME.fasta
#wget $URLS
#gunzip -kc *.gz > ../$NAME.fasta
cd ..
rm -rf $NAME
fi
