


.PHONY:all
all: src
	cp src/libGAnalysis.so ./

.PHONY:src
src:
	cd src ; make all

.PHONY:clean
clean:
	cd src; make clean
	[ -e ./libGAnalysis.so ] && rm libGAnalysis.so || true
