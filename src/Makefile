


SrcSuf        = cc
HeadSuf       = h
ObjSuf        = o
DepSuf        = d
DllSuf	      = so

.SUFFIXES: .$(SrcSuf) .$(ObjSuf) .$(DllSuf)

##
## Flags and external dependecies
## 
LDFLAGS       = -O
SOFLAGS       = -fPIC -shared
LD	      = g++
CXX	      = g++
ROOFIT_BASE=$(ROOFITSYS)
LDFLAGS+=-L$(ROOFIT_BASE)/lib $(ROOTLIBS) -lRooFitCore -lRooFit 
LDFLAGS+= -lTMVA
CXXFLAGS+=-I$(ROOFIT_BASE)/include 
CXXFLAGS+= `root-config --cflags`
CXXFLAGS+=-I$(shell pwd) -g
CXXFLAGS+= -O -fPIC
ROOTLIBS=`root-config --libs`

.PHONY: all
all: Analyzer.so fit.so stat.so
#all: Analyzer.so

Analyzer.d: Analyzer.cc Analyzer.h
	$(CXX) -o Analyzer.$(DepSuf) -M Analyzer.$(SrcSuf) $(CXXFLAGS) $(LDFLAGS)

Analyzer.o: Analyzer.cc Analyzer.h Analyzer.d
	$(CXX) -c -o Analyzer.$(ObjSuf) Analyzer.$(SrcSuf) $(LDFLAGS) $(CXXFLAGS)

Analyzer.so: Analyzer.o AnalyzerDict.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  Analyzer.o AnalyzerDict.o -o Analyzer.so

AnalyzerDict.o: AnalyzerDict.cc
	$(CXX) -c -o AnalyzerDict.o AnalyzerDict.cc $(LDFLAGS) $(CXXFLAGS)

AnalyzerDict.cc: Analyzer.cc AnalyzerLinkDef.h
	@rootcint -v4 -f AnalyzerDict.cc -c -I$(ROOFIT_BASE)/include -I$(CMSSW_BASE)/src  -I$(CMSSW_RELEASE_BASE)/src Analyzer.h AnalyzerLinkDef.h

fit.so: fit.o fitDict.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  fit.o fitDict.o -o fit.so

fit.o: fit.cc fit.d fit.h
	$(CXX) -c -o fit.o fit.cc $(LDFLAGS) $(CXXFLAGS) 

fit.d: fit.cc fit.h
	$(CXX) -o fit.$(DepSuf) -M fit.cc -I$(ROOFIT_BASE)/include $(CXXFLAGS) $(LDFLAGS) 

fitDict.cc: fit.h fitLinkDef.h
	@rootcint -v4 -f fitDict.cc -c -I$(ROOFIT_BASE)/include -I$(CMSSW_BASE)/src  -I$(CMSSW_RELEASE_BASE)/src fit.h fitLinkDef.h

fitDict.o: fitDict.cc
	$(CXX) -c -o fitDict.o fitDict.cc $(LDFLAGS) $(CXXFLAGS)
####################---STAT----
stat.so: stat.o statDict.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  stat.o statDict.o -o stat.so

stat.o: stat.cc stat.d stat.h
	$(CXX) -c -o stat.o stat.cc $(LDFLAGS) $(CXXFLAGS) 

stat.d: stat.cc stat.h
	$(CXX) -o stat.$(DepSuf) -M stat.cc  $(CXXFLAGS) $(LDFLAGS) 

statDict.cc: stat.h statLinkDef.h
	@rootcint -v4 -f statDict.cc -c  stat.h statLinkDef.h

statDict.o: statDict.cc
	$(CXX) -c -o statDict.o statDict.cc $(LDFLAGS) $(CXXFLAGS)
##Analyzer_cc.so: Analyzer.cc Analyzer.h
##	root -q -l -b <<EOF \
##.L Analyzer.cc++ \
##EOF
##
##fit_C.so: fit.C
##	root -q -l -b <<EOF \
##.L fit.C++ \
##EOF

.PHONY: clean	
clean:
	[ -f Analyzer.d      ] && rm Analyzer.d || true
	[ -f Analyzer.o      ] && rm Analyzer.o || true
	[ -f Analyzer.so     ] && rm Analyzer.so || true
	[ -f AnalyzerDict.cc ] && rm AnalyzerDict.cc || true
	[ -f AnalyzerDict.o  ] && rm AnalyzerDict.o || true
	[ -f fit.so          ] && rm fit.so || true
	[ -f fit.o           ] && rm fit.o || true
	[ -f fit.d           ] && rm fit.d || true
	[ -f fitDict.cc      ] && rm fitDict.cc || true
	[ -f fitDict.o       ] && rm fitDict.o || true
	[ -f stat.so          ] && rm stat.so || true
	[ -f stat.o           ] && rm stat.o || true
	[ -f stat.d           ] && rm stat.d || true
	[ -f statDict.cc      ] && rm statDict.cc || true
	[ -f statDict.o       ] && rm statDict.o || true
