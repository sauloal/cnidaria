set -xeu

export GZIP="-1"

tar ahcvf validation_classes.tar.gz classes_all/* classes_2percent/*

tar ahcvf validation_data.tar.gz    data/* desired_rows.csv desired_rows_extended.csv filelist.csv

tar ahcvf validation_trees.tar.gz   trees/*

tar ahcvf validation_treecmp.tar.gz TreeCmp/*.csv TreeCmp/*.nwk TreeCmp/run.sh

tar ahcvf validation_source.tar.gz  src/*
