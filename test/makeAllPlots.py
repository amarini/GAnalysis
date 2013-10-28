import os,sys,array
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
inputFileName=WorkDir+ReadFromDat(config,"outputFileName","output","-->Default Output Name")+".root"

from subprocess import call
from glob import glob

doPurityPlots=True
doInclusivePlots=True
doFitPlots=True

call(["mkdir",WorkDir+"plots"])
#purityPlots
if doPurityPlots:
	cmd=["python","test/makePurityPlots.py","--inputDat="+options.inputDat]
	call(cmd)
#inclusivePtPlots
if doInclusivePlots:
	line=".x test/gamma_Pt_Incl.C(\"%s\",\"gammaPt_VPt_0_8000_Ht_0_8000_phid_0.000_0.011_nJets_1\",\"%s/plots/gammaPt_Incl_Ht0.pdf\")"%(inputFileName,WorkDir)
	ROOT.gROOT.ProcessLine(line)
	line=".x test/gamma_Pt_Incl.C(\"%s\",\"gammaPt_VPt_0_8000_Ht_300_8000_phid_0.000_0.011_nJets_1\",\"%s/plots/gammaPt_Incl_Ht300.pdf\")"%(inputFileName,WorkDir)
	ROOT.gROOT.ProcessLine(line)
	line=".x test/gamma_Pt_Incl.C(\"%s\",\"gammaPt_VPt_0_8000_Ht_100_8000_phid_0.000_0.011_nJets_1\",\"%s/plots/gammaPt_Incl_Ht100.pdf\")"%(inputFileName,WorkDir)
	ROOT.gROOT.ProcessLine(line)
	line=".x test/gamma_Pt_Incl.C(\"%s\",\"gammaPt_VPt_0_8000_Ht_0_8000_phid_0.000_0.011_nJets_3\",\"%s/plots/gammaPt_Incl_nJets3.pdf\")"%(inputFileName,WorkDir)
	ROOT.gROOT.ProcessLine(line)
#fitPlots
if doFitPlots:
	cmd=["python","test/makeFitPlots.py","--inputDat="+options.inputDat]
	call(cmd)
	
