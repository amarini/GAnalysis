


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

.PHONY all:
all: Analyzer_cc.so
#all: Analyzer.so

Analyzer.d: Analyzer.cc Analyzer.h
	$(CXX) -o Analyzer.$(DepSuf) -M Analyzer.$(SrcSuf) $(CXXFLAGS) $(LDFLAGS)

Analyzer.o: Analyzer.cc Analyzer.h Analyzer.d
	$(CXX) -c -o Analyzer.$(ObjSuf) Analyzer.$(SrcSuf) $(LDFLAGS) $(CXXFLAGS)

Analyzer.so: Analyzer.o
	$(LD) $(SOFLAGS) $(LDFLAGS) $(ROOTLIBS)  Analyzer.o -o Analyzer.so

Analyzer_cc.so: Analyzer.cc Analyzer.h
	root -q -l -b <<EOF \
.L Analyzer.cc++ \
EOF

fit_C.so: fit.C
	root -q -l -b <<EOF \
.L fit.C++ \
EOF

	
