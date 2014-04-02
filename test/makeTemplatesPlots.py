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
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
parser.add_option("","--inputDatMC" ,dest='inputDatMC',type='string',help="Input Configuration file for MC",default="")
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

configMC=read_dat(options.inputDatMC)
if(DEBUG>0):
	print "--------- MC CONFIG -----------"
	PrintDat(configMC)

WorkDir         = ReadFromDat(config  ,"WorkDir","./","-->Set Default WDIR")
WorkDirMC       = ReadFromDat(configMC,"WorkDir","./","-->Set Default WDIR MC")
InputFileName   = ReadFromDat(config  ,"outputFileName","output","-->Set Default FileName") + ".root"
InputFileNameMC = ReadFromDat(configMC,"outputFileName","output","-->Set Default FileName") + ".root"
PtCuts          = ReadFromDat(config,"PtCuts",[0,100,200,300],"--> Default PtCuts")
SigPhId	        = ReadFromDat(config,"SigPhId",[0,0.011],"--> Default SigPhId")
BkgPhId         = ReadFromDat(config,"BkgPhId",[0.011,0.014],"--> Default BkgPhId")

ROOT.gSystem.Load("libGAnalysis.so") ##for syst names
fRoot   = ROOT.TFile.Open(WorkDir+"/"+InputFileName)
fRootMC = ROOT.TFile.Open(WorkDirMC+"/"+InputFileNameMC)


def SetDataStyle(h):
	h.SetMarkerStyle(20)
	h.SetLineColor(ROOT.kBlack)
	h.GetXaxis().SetTitle("#gamma Iso")
	h.GetYaxis().SetTitle("# Events (norm. to data)")
def SetMCStyle(h):
	h.SetLineColor(ROOT.kBlue)
	h.SetLineWidth(2)
def SetTruthStyle(h):
	h.SetLineColor(ROOT.kRed)
	h.SetLineWidth(2)
	h.SetLineStyle(ROOT.kDashed)

Ht=0
nJets=1
jetPt=30
for p in range(0,len(PtCuts)-1):
	#if jpt > 250 and PtCuts[p]<200:continue; ##avoid trying to fit: no bkg
	cutSig=ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],Ht,8000,SigPhId[0],SigPhId[1],nJets);
	cutSig.JetPtThreshold=jetPt;
	#Get Histograms -- Sig
	Sig={}
	Sig["data"] = fRoot.Get("photonisoRC_"+cutSig.name() )
	Sig["mc"]   = fRootMC.Get("photonisoRC_"+cutSig.name() )
	Sig["truth"]= fRootMC.Get("photoniso_MATCHED_" + cutSig.name() )

	cutBkg=ROOT.Analyzer.CUTS(PtCuts[p],PtCuts[p+1],Ht,8000,BkgPhId[0],BkgPhId[1],nJets);
	cutBkg.JetPtThreshold=jetPt;
	Bkg={}
	Bkg["data"] = fRoot.Get("photoniso_"+cutBkg.name() )  
	Bkg["mc"]   = fRootMC.Get("photoniso_"+cutBkg.name() )
	Bkg["truth"]= fRootMC.Get("photoniso_NOTMATCHED_"+cutSig.name() )  #Truth=Sig cuts

	if Bkg['data']==None: continue;
	if Sig['data']==None: continue;

	C=ROOT.TCanvas("c","c")
	C.Divide(2);
	txt=ROOT.TLatex()
	txt.SetNDC()
	txt.SetTextSize(0.04)
	txt.SetTextAlign(22)

	C.cd(1)
	SetDataStyle(Sig["data"])
	SetMCStyle(Sig["mc"])
	SetTruthStyle(Sig["truth"])
	txt.DrawLatex(.5,.94,"Signal Templates")
	l=ROOT.TLegend(.75,.69,.89,.89)
	l.SetFillStyle(0)
	l.SetBorderSize(0)

	Sig["data"].Draw("P")
	Sig["mc"].Draw("HIST SAME")
	try:
		Sig["mc"].Scale(Sig["data"].Integral()/Sig["mc"].Integral())
	except: pass
	Sig["truth"].Draw("HIST SAME")
	try:
		Sig["truth"].Scale(Sig["data"].Integral()/Sig["truth"].Integral())
	except: pass
	l.AddEntry(Sig["data"],"data","PF")
	l.AddEntry(Sig["mc"],"mc","L")
	l.AddEntry(Sig["truth"],"mc-truth","L")
	l.Draw()

	C.cd(2)
	SetDataStyle(Bkg["data"])
	SetMCStyle(Bkg["mc"])
	SetTruthStyle(Bkg["truth"])
	txt.DrawLatex(.5,.94,"Background Templates")
	l=ROOT.TLegend(.75,.69,.89,.89)
	l.SetFillStyle(0)
	l.SetBorderSize(0)

	Bkg["data"].Draw("P")
	Bkg["mc"].Draw("HIST SAME")
	try:
		Bkg["mc"].Scale(Bkg["data"].Integral()/Bkg["mc"].Integral())
	except: pass
	Bkg["truth"].Draw("HIST SAME")
	try:
		Bkg["truth"].Scale(Bkg["data"].Integral()/Bkg["truth"].Integral())
	except: pass
	l.AddEntry(Bkg["data"],"data","PF")
	l.AddEntry(Bkg["mc"],"mc","L")
	l.AddEntry(Bkg["truth"],"mc-truth","L")
	l.Draw()

	C.SaveAs(WorkDir+"/plots/Templates_Pt%.0f_%.0f.pdf"%(PtCuts[p],PtCuts[p+1]))
	

