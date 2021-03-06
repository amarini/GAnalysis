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
parser.add_option("","--inputDatMC" ,dest='inputDatMC',type='string',help="Input Configuration file",default="data/configMC.dat")
parser.add_option("","--jetphox",dest='jetphox',type='string',help='JetPhox',default="")
#parser.add_option("","--doPurityPlots" ,dest='doPurityPlots',action='store_true',help="Input Configuration file",default="")

(options,args)=parser.parse_args()

doPurityPlots=True
doInclusivePlots=True
doFitPlots=True
doParsPlots=True
doUnfoldPlots=True
doUnfoldStudies=True
doTemplatePlots=True
doElectronFakeRate=True

isMC=False
if "mc" in options.inputDat.lower():
	doUnfoldStudies=False
	isMC=True

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


call(["rm","-r",WorkDir+"plots"])
call(["mkdir","-p",WorkDir+"plots"])
#purityPlots
if doPurityPlots:
	print >>sys.stderr, " --- PURITY --- "
	cmd=["python","test/makePurityPlots.py","--inputDat="+options.inputDat]
	if isMC:
		cmd=["python","test/makePurityPlots.py","--inputDat="+options.inputDat,"--inputDatMC="+options.inputDat]
	call(cmd)
#inclusivePtPlots
if doInclusivePlots:
	print >>sys.stderr, " --- INCLUSIVE --- "
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
	print >>sys.stderr, " --- FIT PLOTS --- "
	cmd=["python","test/makeFitPlots.py","--inputDat="+options.inputDat]
	call(cmd)
#LandaPars
if doParsPlots:
	print >>sys.stderr,  " --- PARS PLOTS --- "
	cmd=["python","test/makeLandauParsPlots.py","--inputDat="+options.inputDat]
	call(cmd)
#unfolded distributions
if doUnfoldPlots:
	print >>sys.stderr, " --- UNFOLD PLOTS --- "
	cmd=["python","test/makeUnfoldPlots.py","--inputDat="+options.inputDat,"--jetphox="+options.jetphox]#,"--inputDatMC="+options.inputDatMC]
	call(cmd)

if doUnfoldStudies:
	print >>sys.stderr, " --- UNFOLD STUDIES --- "
	cmd=["python","test/makeUnfoldStudiesPlots.py","--inputDat="+options.inputDat]

if doTemplatePlots:
	print >>sys.stderr, " --- TEMPLATE PLOTS --- "
	cmd=["python","test/makeTemplatesPlots.py","--inputDat="+options.inputDat,"--inputDatMC="+options.inputDatMC]
	call(cmd)

if doElectronFakeRate:
	print >>sys.stderr, " --- ELECTRON FRACTION PLOTS --- "
	cmd=["python","test/makeElectroFractionPlots.py","--inputDatMC="+options.inputDatMC]
	call(cmd)

