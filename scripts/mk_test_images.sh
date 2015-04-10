cd test

ls *.nj *.upgma | xargs -n1 -I{} -P10 ../newick_to_png.py {}

for test in test1 test2; do echo $test; for scale in no_scale fibonnacci_scale power2_scale; do echo $test $scale; ../pngfolder_to_html.py ${test}.cnm.${scale}*.png; done; done;
