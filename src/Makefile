


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
all: Analyzer.so fit.so
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

fit.o: fit.C fit.d
	$(CXX) -c -o fit.o fit.C $(LDFLAGS) $(CXXFLAGS) 

fit.d: fit.C
	$(CXX) -o fit.$(DepSuf) -M fit.C -I$(ROOFIT_BASE)/include $(CXXFLAGS) $(LDFLAGS) 

fitDict.cc: fit.C fitLinkDef.h
	@rootcint -v4 -f fitDict.cc -c -I$(ROOFIT_BASE)/include -I$(CMSSW_BASE)/src  -I$(CMSSW_RELEASE_BASE)/src fit.C fitLinkDef.h

fitDict.o: fitDict.cc
	$(CXX) -c -o fitDict.o fitDict.cc $(LDFLAGS) $(CXXFLAGS)

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
