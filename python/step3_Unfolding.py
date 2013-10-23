#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser

DEBUG=1

ROOT.gROOT.SetBatch()

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
parser.add_option("-l","--libRooUnfold" ,dest='libRooUnfold',type='string',help="Shared RooUnfoldLibrary",default="/afs/cern.ch/user/a/amarini/work/RooUnfold-1.1.1/libRooUnfold.so")

(options,args)=parser.parse_args()

from common import *

if(DEBUG>0): print "--> load dat file: "+options.inputDat;

config=read_dat(options.inputDat)

if(DEBUG>0):
	PrintDat(config)

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")

PtCuts=ReadFromDat(config,"PtCuts",[0,100,200,300],"--> Default PtCuts")

HtCuts=ReadFromDat(config,"HtCuts",[0,100,200,300],"--> Default HtCuts")

nJetsCuts=ReadFromDat(config,"nJetsCuts",[1,3],"--> Default nJetsCuts")

SigPhId=ReadFromDat(config,"SigPhId",[0,0.011],"--> Default SigPhId")

BkgPhId=ReadFromDat(config,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

inputFileNameFit=WorkDir + "/fitresults.txt"  
inputFileNameRoot= WorkDir + ReadFromDat(config,"outputFileName","output","--> Default outputFileName")

if(DEBUG>0): print "--> Load RooUnfold Library"
ROOT.gSystem.Load(options.libRooUnfold)

if(DEBUG>0): print "--> Opening files"
fFit= open(inputFileNameFit,"r")
fRoot= ROOT.TFile.Open(inputFileNameRoot);

for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 or HtCuts[h] !=0:continue;
		for p in range(0,len(PtCuts)):
			## TAKE FITTED FRACTION
			## TAKE HISTO WITH YIELDS
			## FILL HISTO CORRECTED
		## TAKE MATRIX & HISTO FOR REPSONSE MATRIX
		## UNFOLD
		## SAVE OUTPUT

#ToFitTemplate.append(file.Get("photoniso_VPt_%.0f_%.0f_Ht_%.0f_%.0f_phid_%.3f_%.3f_nJets_%d"%(PtCuts[p],PtCuts[p+1],Ht,8000,SigPhId[0],SigPhId[1] ,nJets ) ) )

