#!/usr/bin/python
import sys,os
import array
import ROOT
import time
import math
from optparse import OptionParser

DEBUG=1

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

if(DEBUG>0):print "----- BEGIN -----"

usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
#parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
parser.add_option("","--inputDatMC" ,dest='inputDatMC',type='string',help="Input Configuration file for MC",default="")
(options,args)=parser.parse_args()

print "inserting in path cwd"
sys.path.insert(0,os.getcwd())
print "inserting in path cwd/python"
sys.path.insert(0,os.getcwd()+'/python')

from common import *

#if(DEBUG>0): print "--> load dat file: "+options.inputDat

#config=read_dat(options.inputDat)

#if(DEBUG>0):
#	print "--------- DATA CONFIG -----------"
#	PrintDat(config)

configMC=read_dat(options.inputDatMC)
if(DEBUG>0):
	print "--------- MC CONFIG -----------"
	PrintDat(configMC)

#WorkDir         = ReadFromDat(config  ,"WorkDir","./","-->Set Default WDIR")
WorkDirMC       = ReadFromDat(configMC,"WorkDir","./","-->Set Default WDIR MC")
InputFileName   = ReadFromDat(configMC  ,"outputFileName","output","-->Set Default FileName") + ".root"
InputFileNameMC = ReadFromDat(configMC,"outputFileName","output","-->Set Default FileName") + ".root"
#PtCuts         = ReadFromDat(configMC,"PtCuts",[0,100,200,300],"--> Default PtCuts")
HtCuts          = ReadFromDat(configMC,"HtCuts",[0,100,200,300],"--> Default HtCuts")
nJetsCuts       = ReadFromDat(configMC,"nJetsCuts",[1,3],"--> Default nJetsCuts")
SigPhId	        = ReadFromDat(configMC,"SigPhId",[0,0.011],"--> Default SigPhId")
BkgPhId         = ReadFromDat(configMC,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

ROOT.gSystem.Load("libGAnalysis.so") ##for syst names
#fRoot   = ROOT.TFile.Open(WorkDir+"/"+InputFileName)
fRootMC = ROOT.TFile.Open(WorkDirMC+"/"+InputFileNameMC)

for nJets in nJetsCuts:
	for Ht in HtCuts:
		if nJets >1 and Ht >0 : continue

		cutSig=ROOT.Analyzer.CUTS(0,8000,Ht,8000,SigPhId[0],SigPhId[1],int(nJets))
		
		h_gamma = fRootMC.Get("gammaPt_RECO_UNFOLD_"+cutSig.name() )
		h_e 	= fRootMC.Get("gammaPt_RECO_EMATCHED_"+cutSig.name() )
		
		h_e.Divide(h_gamma)

		C=ROOT.TCanvas("c","c")

		h_e.SetLineColor(ROOT.kBlue)
		h_e.SetLineWidth(2)

		txt=ROOT.TLatex()
		txt.SetNDC()
		txt.SetTextSize(0.04)
		txt.SetTextAlign(22)
		
		h_e.Draw("HIST")
		h_e.GetXaxis().SetTitle("P_{T}^{#gamma/e}[GeV]")
		h_e.GetYaxis().SetTitle("e/#gamma events (Fake Rate)")
		h_e.GetYaxis().SetRangeUser(0,0.05);

		txt.DrawLatex(0.5,.85,"H_{T} > %.0f & N_{jets} #geq %d"%(Ht,nJets) )

		C.SaveAs(WorkDirMC+"/plots/Efakerate_Ht%.0f_nJets%d.pdf"%(Ht,nJets))
print "--DONE--"
