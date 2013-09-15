#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser

DEBUG=1

### #Book Cuts
PtCuts=[100,150,200,250,300,350,450,550,650,750,-1,100,300,750]
SigPhId=[-10.,-.1]
BkgPhId=[0.1,10.]

from common import *

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"

usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--nJobs" ,dest='nJobs',type='int',help="Total number of jobs. Useful to run on batch",default=0)
parser.add_option("","--jobId" ,dest='jobId',type='int',help="Current job number. Useful to run on batch",default=0)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")

(options,args)=parser.parse_args()

if(DEBUG>0):print "--LOAD ANALYZER--"
ROOT.gSystem.Load("Analyzer.so");
ROOT.gROOT.SetBatch(1);

if(DEBUG>0):print "--USE ANALYZER---"

A=ROOT.Analyzer()

if(DEBUG>0):A.debug=DEBUG;


if(DEBUG>0): print "--> load dat file: "+options.inputDat;
	config=read_dat(options.inputDat)

try:
	WorkDir=config["WorkDir"]
except KeyError:
	WorkDir="./"

try:	
	A.outputFileName=WorkDir+config["outputFileName"]
	if(DEBUG>0):print "OutputFile="+config["outputFileName"]
except KeyError:	
	A.outputFileName=WorkDir+"output"
	if(DEBUG>0):print "OutputFile=output"

try: 
	for tree in config["DataTree"]: A.AddTree(tree) 
except KeyError: A.AddTree("SinglePhoton_Run2012C-22Jan2013-v1_AOD/*.root")

if(DEBUG>0): print "--> loaded files"

try:
	PtCuts=config["PtCuts"]
except KeyError: PtCuts=[0,100,200,300]

try:
	SigPhId=config["SigPhId"]
except KeyError: SigPhId=[0,0.11]	

try:
	BkgPhId=config["BkgPhId"]
except KeyError: BkgPhId=[0,0.11]	

for p in range(0,len(PtCuts)):
	A.PtCuts.push_back(PtCuts[p])

A.SigPhId.first=SigPhId[0];
A.SigPhId.second=SigPhId[1];
A.BkgPhId.first=BkgPhId[0];
A.BkgPhId.second=BkgPhId[1];
### 
if(DEBUG>0): print "--> Init"
A.Init()

if(DEBUG>0): print "----- LOOP -----"
A.Loop()

if(DEBUG>0): print "----- END ------"
