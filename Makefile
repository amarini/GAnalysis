


.PHONY:all
all: src
	cp src/Analyzer.so ./
	cp src/fit.so ./

.PHONY:src
src:
	cd src ; make all

fit.so:
	cd src ; make fit.so

Analyzer.so:
	cd src	; make Analyzer.so


.PHONY:clean
clean:
	cd src; make clean
	[ -e ./Analyzer.so ] && rm Analyzer.so || true
	[ -e ./fit.so ] && rm fit.so || true
