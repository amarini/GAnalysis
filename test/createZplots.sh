#!/bin/bash
#create the plots
for i in ../Z/h*modJetLepVeto*.root ; do python test/makeZNicePlots.py -i $i -o ${i%%.root}.pdf ; done

cd ../Z
python ../GAnalysis/test/MatthiasMv.py  > map.sh
#ls ../Z/res_*.pdf  | sed 's:../Z/::' | while read file ; do [ -f ../notes/SMP-14-005/trunk/figs/$file ] && echo mv $file ../notes/SMP-14-005/trunk/figs/  || echo "# $file"; done  | bash 
cd -

for i in ../Z//hist_files_MSTW_CT10_NNPDF/h_*.root ; do  python test/makeZNicePlots.py -i $i -o ${i%%.root}.pdf ; done
