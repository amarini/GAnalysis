


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
LDFLAGS+=-L$(ROOFIT_BASE)/lib $(ROOTLIBS) -lRooFitCore -lRooFit -lz
LDFLAGS+= -lTMVA
CXXFLAGS+=-I$(ROOFIT_BASE)/include 
CXXFLAGS+= `root-config --cflags`
CXXFLAGS+=-I$(shell pwd) -g
CXXFLAGS+= -O -fPIC
ROOTLIBS=`root-config --libs`

.PHONY: all
all: Analyzer.so fit.so stat.so Selection.so libGAnalysis.so DumpAscii.so
#all: Analyzer.so

libGAnalysis.so: Analyzer.o fit.o Selection.o AnalyzerDict.o fitDict.o SelectionDict.o stat.o statDict.o DumpAscii.o DumpAsciiDict.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  Analyzer.o AnalyzerDict.o Selection.o SelectionDict.o fit.o fitDict.o stat.o statDict.o DumpAscii.o DumpAsciiDict.o -o libGAnalysis.so

Analyzer.d: Analyzer.cc Analyzer.h
	$(CXX) -o Analyzer.$(DepSuf) -M Analyzer.$(SrcSuf) $(CXXFLAGS) $(LDFLAGS)

Analyzer.o: Analyzer.cc Analyzer.h Analyzer.d
	$(CXX) -c -o Analyzer.$(ObjSuf) Analyzer.$(SrcSuf) $(LDFLAGS) $(CXXFLAGS)

Analyzer.so: Analyzer.o AnalyzerDict.o Selection.o SelectionDict.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  Analyzer.o AnalyzerDict.o Selection.o SelectionDict.o -o Analyzer.so

AnalyzerDict.o: AnalyzerDict.cc
	$(CXX) -c -o AnalyzerDict.o AnalyzerDict.cc $(LDFLAGS) $(CXXFLAGS)

AnalyzerDict.cc: Analyzer.cc AnalyzerLinkDef.h
	@rootcint -v4 -f AnalyzerDict.cc -c -I$(ROOFIT_BASE)/include -I$(CMSSW_BASE)/src  -I$(CMSSW_RELEASE_BASE)/src Analyzer.h AnalyzerLinkDef.h

fit.so: fit.o fitDict.o stat.o statDict.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  fit.o fitDict.o stat.o statDict.o -o fit.so

fit.o: fit.cc fit.d fit.h
	$(CXX) -c -o fit.o fit.cc $(LDFLAGS) $(CXXFLAGS) 

fit.d: fit.cc fit.h
	$(CXX) -o fit.$(DepSuf) -M fit.cc -I$(ROOFIT_BASE)/include $(CXXFLAGS) $(LDFLAGS) 

fitDict.cc: fit.h fitLinkDef.h
	@rootcint -v4 -f fitDict.cc -c -I$(ROOFIT_BASE)/include -I$(CMSSW_BASE)/src  -I$(CMSSW_RELEASE_BASE)/src fit.h fitLinkDef.h

fitDict.o: fitDict.cc
	$(CXX) -c -o fitDict.o fitDict.cc $(LDFLAGS) $(CXXFLAGS)
#####################---DUMPASCII
DumpAscii.so: DumpAscii.o DumpAsciiDict.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  DumpAscii.o DumpAsciiDict.o -o DumpAscii.so

DumpAscii.o: DumpAscii.cc DumpAscii.d DumpAscii.h
	$(CXX) -c -o DumpAscii.o DumpAscii.cc $(LDFLAGS) $(CXXFLAGS) 

DumpAscii.d: DumpAscii.cc DumpAscii.h
	$(CXX) -o DumpAscii.$(DepSuf) -M DumpAscii.cc -I$(ROOFIT_BASE)/include $(CXXFLAGS) $(LDFLAGS) 

DumpAsciiDict.cc: DumpAscii.h DumpAsciiLinkDef.h
	@rootcint -v4 -f DumpAsciiDict.cc -c -I$(ROOFIT_BASE)/include -I$(CMSSW_BASE)/src  -I$(CMSSW_RELEASE_BASE)/src DumpAscii.h DumpAsciiLinkDef.h

DumpAsciiDict.o: DumpAsciiDict.cc
	$(CXX) -c -o DumpAsciiDict.o DumpAsciiDict.cc $(LDFLAGS) $(CXXFLAGS)
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


###############SELECTION
Selection.d: Selection.cc Selection.h
	$(CXX) -o Selection.$(DepSuf) -M Selection.$(SrcSuf) $(CXXFLAGS) $(LDFLAGS)

Selection.o: Selection.cc Selection.h Selection.d
	$(CXX) -c -o Selection.$(ObjSuf) Selection.$(SrcSuf) $(LDFLAGS) $(CXXFLAGS)

Selection.so: Selection.o SelectionDict.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  Selection.o SelectionDict.o -o Selection.so

SelectionDict.o: SelectionDict.cc
	$(CXX) -c -o SelectionDict.o SelectionDict.cc $(LDFLAGS) $(CXXFLAGS)

SelectionDict.cc: Selection.cc SelectionLinkDef.h
	@rootcint -v4 -f SelectionDict.cc -c -I$(ROOFIT_BASE)/include -I$(CMSSW_BASE)/src  -I$(CMSSW_RELEASE_BASE)/src Selection.h SelectionLinkDef.h
##EOF

.PHONY: clean	
clean: clean_Selection clean_Analyzer clean_Fit clean_Stat clean_DumpAscii

.PHONY: clean_Selection clean_Analyzer clean_Fit clean_Stat clean_DumpAscii
clean_Analyzer:
	[ -f Analyzer.d      ] && rm Analyzer.d || true
	[ -f Analyzer.o      ] && rm Analyzer.o || true
	[ -f Analyzer.so     ] && rm Analyzer.so || true
	[ -f AnalyzerDict.cc ] && rm AnalyzerDict.cc || true
	[ -f AnalyzerDict.o  ] && rm AnalyzerDict.o || true
clean_Fit:
	[ -f fit.so          ] && rm fit.so || true
	[ -f fit.o           ] && rm fit.o || true
	[ -f fit.d           ] && rm fit.d || true
	[ -f fitDict.cc      ] && rm fitDict.cc || true
	[ -f fitDict.o       ] && rm fitDict.o || true
clean_Stat:
	[ -f stat.so          ] && rm stat.so || true
	[ -f stat.o           ] && rm stat.o || true
	[ -f stat.d           ] && rm stat.d || true
	[ -f statDict.cc      ] && rm statDict.cc || true
	[ -f statDict.o       ] && rm statDict.o || true
clean_Selection:
	[ -f Selection.so          ] && rm Selection.so || true
	[ -f Selection.o           ] && rm Selection.o || true
	[ -f Selection.d           ] && rm Selection.d || true
	[ -f SelectionDict.cc      ] && rm SelectionDict.cc || true
	[ -f SelectionDict.o       ] && rm SelectionDict.o || true
clean_DumpAscii:
	[ -f DumpAscii.so          ] && rm DumpAscii.so || true
	[ -f DumpAscii.o           ] && rm DumpAscii.o || true
	[ -f DumpAscii.d           ] && rm DumpAscii.d || true
	[ -f DumpAsciiDict.cc      ] && rm DumpAsciiDict.cc || true
	[ -f DumpAsciiDict.o       ] && rm DumpAsciiDict.o || true
