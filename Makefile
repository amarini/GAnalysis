


.PHONY:all
all: src
	cp src/libGAnalysis.so ./

.PHONY:src
src:
	$(MAKE) -C src  all 

.PHONY:clean
clean:
	$(MAKE) -C src clean
	[ -e ./libGAnalysis.so ] && rm libGAnalysis.so || true
