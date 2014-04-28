
SLC=$(shell lsb_release -r | tr '\t' ' '| tr -s ' ' | cut -d ' ' -f2)
SLC6=$(shell echo "$(SLC) > 5.9" | bc -lq )

ifeq ($(strip $(SLC6)),"1")
	LD_LIBRARY_PATH=/lib64:/usr/lib64/perl5/CORE:$(LD_LIBRARY_PATH)
	$(shell source /afs/cern.ch/sw/lcg/contrib/gcc/4.7.2p1/x86_64-slc6/setup.sh )
endif


.PHONY:all
all: src
	#source  /afs/cern.ch/sw/lcg/contrib/gcc/4.7.2p1/x86_64-slc6/setup.sh
	#[ ${SLC6} -eq 1 ] && LD_LIBRARY_PATH=/lib64:/usr/lib64/perl5/CORE:$LD_LIBRARY_PATH
	cp src/libGAnalysis.so ./

.PHONY:src
src:
	$(MAKE) -C src  all 

.PHONY:tar
tar: all GAnalysis.tar.gz

GAnalysis.tar.gz: libGAnalysis.so data/* python/* aux/* test/* 
	tar -czf GAnalysis.tar.gz libGAnalysis.so data python aux test

.PHONY:clean
clean:
	$(MAKE) -C src clean
	-rm libGAnalysis.so 
	-rm GAnalysis.tar.gz 
