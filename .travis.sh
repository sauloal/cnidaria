if      [[ $TEST_TARGET == 'DOWNLOAD' ]]; then
    make -c test out/Makefile
else if [[ $TEST_TARGET == 'ANALYSIS' ]]; then
    make -c test out/test/test.json
else if [[ $TEST_TARGET == 'ALL'      ]]; then
    make -c test
else
    exit 1
fi
