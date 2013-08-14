#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser

DEBUG=1

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"

usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--nJobs" ,dest='nJobs',type='int',help="Total number of jobs. Useful to run on batch",default=0)
parser.add_option("","--jobId" ,dest='jobId',type='int',help="Current job number. Useful to run on batch",default=0)

(options,args)=parser.parse_args()

if(DEBUG>0):print "--LOAD ANALYZER--"
ROOT.gSystem.Load("Analyzer_cc.so");
ROOT.gROOT.SetBatch(1);

if(DEBUG>0):print "--USE ANALYZER---"

A=ROOT.Analyzer()
A.AddTree("SinglePhoton_Run2012C-22Jan2013-v1_AOD/*.root")
if(DEBUG>0): print "--> loaded files"
A.outputFileName="output"

### #Book Cuts
PtCuts=[100,150,200,250,300,350,450,550,650,750,-1,100,300,750]
SigPhId=[-10.,-.1]
BkgPhId=[0.1,10.]
for p in range(0,len(PtCuts)):
	A.PtCuts.push_back(PtCuts[p])
	###	don't work unless make dictonaries worknig
	### 	A.cutsContainer.push_back(ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],0,8000,BkgPhId[0],BkgPhId[1])); #bkg
	### 	A.cutsContainer.push_back(ROOT.Analyzer.CUTS(PtCuts[p],PtCUts[p+1],0,8000,SigPhId[0],SigPhId[1])); #sig
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
