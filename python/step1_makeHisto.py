#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser

DEBUG=1
ROOT.gROOT.SetBatch(1);

### #Book Cuts
PtCuts=[100,150,200,250,300,350,450,550,650,750,-1,100,300,750]
SigPhId=[-10.,-.1]
BkgPhId=[0.1,10.]

from common import *

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"

usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--nJobs" ,dest='nJobs',type='int',help="Total number of jobs. Useful to run on batch",default=-1)
parser.add_option("","--jobId" ,dest='jobId',type='int',help="Current job number. Useful to run on batch",default=0)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")

(options,args)=parser.parse_args()

if(DEBUG>0):print "--LOAD ANALYZER--"
ROOT.gSystem.Load("Analyzer.so");

if(DEBUG>0):print "--USE ANALYZER---"

A=ROOT.Analyzer()

if(DEBUG>0):A.debug=DEBUG;


if(DEBUG>0): print "--> load dat file: "+options.inputDat;
config=read_dat(options.inputDat)

if(DEBUG>0):
	PrintDat(config)

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")

A.outputFileName=WorkDir+ReadFromDat(config,"outputFileName","output","-->Default Output Name")

try: 
	for tree in config["DataTree"]: A.AddTree(tree) 
except KeyError: A.AddTree("SinglePhoton_Run2012C-22Jan2013-v1_AOD/*.root")

if(DEBUG>0): print "--> loaded files"

PtCuts=ReadFromDat(config,"PtCuts",[0,100,200,300],"--> Default PtCuts")

HtCuts=ReadFromDat(config,"HtCuts",[0,100,200,300],"--> Default HtCuts")

nJetsCuts=ReadFromDat(config,"nJetsCuts",[1,3],"--> Default nJetsCuts")

SigPhId=ReadFromDat(config,"SigPhId",[0,0.011],"--> Default SigPhId")

BkgPhId=ReadFromDat(config,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

try:
	for iT in range(0,len(config["TriggerMenus"]) ):
		A.LoadTrigger(config["TriggerMenus"][iT],config["PtTriggers"][iT][0],config["PtTriggers"][iT][1],config["PreScale"][iT]);
		print "-> TRIGGER: "+config["TriggerMenus"][iT] + " "+str(config["PtTriggers"][iT][0])+"-"+str(config["PtTriggers"][iT][1])+"    "+str(config["PreScale"][iT])
except KeyError: print "NO TRIGGER LOADED!!!"
except IndexError: print "Check TRigger configurations: index out of range"

if(DEBUG>0): print "-->Loading Cuts in Analyzer"
for p in range(0,len(PtCuts)):
	A.PtCuts.push_back(PtCuts[p])
for h in range(0,len(HtCuts)):
	A.HtCuts.push_back(HtCuts[h])
for j in range(0,len(nJetsCuts)):
	A.nJetsCuts.push_back( int(nJetsCuts[j]) )

A.SigPhId.first=SigPhId[0];
A.SigPhId.second=SigPhId[1];
A.BkgPhId.first=BkgPhId[0];
A.BkgPhId.second=BkgPhId[1];
##EffArea
A.useEffArea=1;
A.effAreaFile=WorkDir+"effarea.txt"
if(DEBUG>0):print "Using EFF AREA="+A.effAreaFile

#BATCH JOBS
A.nJobs=options.nJobs
A.jobId=options.jobId
### 
if(DEBUG>0): print "--> Init"
A.Init()

if(DEBUG>0): print "----- LOOP -----"
A.Loop()

if config["DoSyst"] :
	print "--- LOOP ON SYST ---- PU UP--"
	#A.currentSyst=ROOT.Analyzer.SYST.PUUP  -- dont work
	A.currentSyst= 3
	A.Loop()
	print "--- LOOP ON SYST ---- PU DN --"
	A.currentSyst=4
	A.Loop()
	print "--- LOOP ON SYST ---- JES UP--"
	A.currentSyst=1
	A.Loop()
	print "--- LOOP ON SYST ---- JES DN --"
	A.currentSyst=2
	A.Loop()

if(DEBUG>0): print "----- END ------"
