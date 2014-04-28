## LOOP OVER txtgz
 for i in *log*txt.gz ; 
 	do 
 	zcat $i | tail -n 1 | grep -- '--- END ---' &>/dev/null && { [ -f ${i%%.txt.gz}.fail ] &&  echo touch ${i%%.txt.gz}.done && rm ${i%%.txt.gz}.fail || true; [ -f ${i%%.txt.gz}.done ] || echo touch ${i%%.txt.gz}.done ; } || { echo -n $i |sed 's/^.*_//' | sed 's/\..*$//g' ; echo -n " "; [ -f  ${i%%.txt.gz}.fail ] || touch ${i%%.txt.gz}.fail ; } ; 
 	done

exit 0 
for i in *log*fail ; 
	do 
	zcat ${i%%.fail}.txt.gz | tail -n 1 | grep -- '--- END ---' &>/dev/null && { [ -f $i ] && rm ${i} && touch ${i%%.fail}.done || true; } || { echo -n $i |sed 's/^.*_//' | sed 's/\..*$//g' ; echo -n " ";} ; 
	done
