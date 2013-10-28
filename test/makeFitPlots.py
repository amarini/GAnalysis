#!/usr/bin/python
import sys,os
import array
import ROOT
import time
from optparse import OptionParser

DEBUG=1

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

if(DEBUG>0):print "----- BEGIN -----"

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")

(options,args)=parser.parse_args()

print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')
from common import *

if(DEBUG>0): print "--> load dat file: "+options.inputDat

config=read_dat(options.inputDat)

if(DEBUG>0):
	print "--------- DATA CONFIG -----------"
	PrintDat(config)

WorkDir=ReadFromDat(config,"WorkDir","./","-->Set Default WDIR")

PtCuts=ReadFromDat(config,"PtCuts",[0,100,200,300],"--> Default PtCuts")

HtCuts=ReadFromDat(config,"HtCuts",[0,100,200,300],"--> Default HtCuts")

nJetsCuts=ReadFromDat(config,"nJetsCuts",[1,3],"--> Default nJetsCuts")

SigPhId=ReadFromDat(config,"SigPhId",[0,0.011],"--> Default SigPhId")

BkgPhId=ReadFromDat(config,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

inputFileNameFit=WorkDir + "/fitresults.root"  

file=ROOT.TFile.Open(inputFileNameFit)

for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	
		try:
			PtCuts2=PtCuts[0:PtCuts.index(-1) ]
		except ValueError: PtCuts2=PtCuts
		for p in range(0,len(PtCuts2)-1):
			try:
				C=file.Get("Bin_PT_%.1f_%.1f_HT_%.1f_nJets_%.0f_canvas"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj]) )
				C.SaveAs(WorkDir+"plots/fit_"+C.GetName()+".pdf")
			except ReferenceError: 
				print "Error in Pt="+str(PtCuts2[p])+" HT="+str(HtCuts[h])+" nJets="+str(nJetsCuts[nj])
				print "-- Name="+"Bin_PT_%.1f_%.1f_HT_%.1f_nJets_%.0f_canvas"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj])

