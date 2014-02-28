


.PHONY:all
all: src tar
	cp src/libGAnalysis.so ./

.PHONY:src
src:
	$(MAKE) -C src  all 

.PHONY:tar
tar: GAnalysis.tar.gz

GAnalysis.tar.gz: libGAnalysis.so data/* python/* aux/* test/* 
	tar -czf GAnalysis.tar.gz libGAnalysis.so data python aux test

.PHONY:clean
clean:
	$(MAKE) -C src clean
	-rm libGAnalysis.so 
	-rm GAnalysis.tar.gz 
