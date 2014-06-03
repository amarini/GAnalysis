#!/usr/bin/python
import sys,os
import array
import ROOT
import time
import math
from optparse import OptionParser

DEBUG=1

ROOT.gROOT.SetStyle("Plain");

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

ROOT.gStyle.SetPalette(1);
ROOT.gStyle.SetHatchesLineWidth(3);

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
	h.GetYaxis().SetTitle("Events (norm. to data)")
	h.GetYaxis().SetTitleOffset(1.7)
	h.GetXaxis().SetTitleOffset(0.8)
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

	Bkg["rebin"]=4
	Bkg["data"].Rebin(Bkg["rebin"])
	Bkg["mc"].Rebin(Bkg["rebin"])
	Bkg["truth"].Rebin(Bkg["rebin"])

	C=ROOT.TCanvas("c","c")
	C.Divide(2);
	txt=ROOT.TLatex()
	txt.SetNDC()
	txt.SetTextSize(0.04)
	txt.SetTextAlign(22)
	
	# -------------- DRAW RC ---------------#
	p1=C.cd(1)
	p1.SetLeftMargin(0.15)
	SetDataStyle(Sig["data"])
	SetMCStyle(Sig["mc"])
	SetTruthStyle(Sig["truth"])
	#l=ROOT.TLegend(.6,.69,.89,.89)
	l=ROOT.TLegend(.18,.69,.48,.89)
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

	LegendFontSize=0.025
	e=l.AddEntry(Sig["data"],"data (RC)","PL")
	e.SetTextSize(LegendFontSize)

	DrawBands=True
	if DrawBands:
		Sig["truth-err"]=Sig["truth"].Clone("error-truth")
		#Sig["truth-err"].SetFillStyle(3254)
		Sig["truth-err"].SetFillStyle(3004)
		Sig["truth-err"].SetFillColor(ROOT.kRed-4)
		Sig["truth-err"].SetMarkerStyle(0);
		Sig["truth-err"].SetMarkerColor(Sig["truth-err"].GetFillColor());
		Sig["truth-err"].Draw("E2 SAME")

		Sig["mc-err"]=Sig["mc"].Clone("error-mc")
		Sig["mc-err"].SetFillStyle(3005)
		Sig["mc-err"].SetFillColor(ROOT.kBlue-4)
		Sig["mc-err"].SetMarkerStyle(0);
		Sig["mc-err"].SetMarkerColor(Sig["mc-err"].GetFillColor());
		Sig["mc-err"].Draw("E2 SAME")

		Sig["mc"].Draw("HIST SAME")
		Sig["truth"].Draw("HIST SAME")
		Sig["data"].Draw("P SAME")

		e=l.AddEntry(Sig["mc-err"],"mc (RC)","F")
		e.SetTextSize(LegendFontSize)
		e=l.AddEntry(Sig["truth-err"],"mc-truth","F")
		e.SetTextSize(LegendFontSize)
	else:
		e=l.AddEntry(Sig["mc"],"mc (RC)","L")
		e.SetTextSize(LegendFontSize)
		e=l.AddEntry(Sig["truth"],"mc-truth","L")
		e.SetTextSize(LegendFontSize)

	l.Draw()
	Sig["legend"]=l
	txt.DrawLatex(.5,.94,"Signal Templates")

	# -------------- DRAW BKG ---------------#
	p2=C.cd(2)
	p2.SetLeftMargin(0.15)
	SetDataStyle(Bkg["data"])
	SetMCStyle(Bkg["mc"])
	SetTruthStyle(Bkg["truth"])
	#l=ROOT.TLegend(.60,.69,.89,.89)
	l=ROOT.TLegend(.18,.69,.48,.89)
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
	e=l.AddEntry(Bkg["data"],"data (#scale[0.8]{#sigma_{i#eta i#eta}#geq 0.011})","PL")
	e.SetTextSize(LegendFontSize)

	if DrawBands:
		Bkg["truth-err"]=Bkg["truth"].Clone("error-truth")
		#Bkg["truth-err"].SetFillStyle(3254)
		Bkg["truth-err"].SetFillStyle(3004)
		Bkg["truth-err"].SetFillColor(ROOT.kRed-4)
		Bkg["truth-err"].SetMarkerStyle(0);
		Bkg["truth-err"].SetMarkerColor(Bkg["truth-err"].GetFillColor());
		Bkg["truth-err"].Draw("E2 SAME")

		Bkg["mc-err"]=Bkg["mc"].Clone("error-mc")
		Bkg["mc-err"].SetFillStyle(3005)
		Bkg["mc-err"].SetFillColor(ROOT.kBlue-4)
		Bkg["mc-err"].SetMarkerStyle(0);
		Bkg["mc-err"].SetMarkerColor(Bkg["mc-err"].GetFillColor());
		Bkg["mc-err"].Draw("E2 SAME")

		Bkg["mc"].Draw("HIST SAME")
		Bkg["truth"].Draw("HIST SAME")
		Bkg["data"].Draw("P SAME")

		e=l.AddEntry(Bkg["mc-err"],"mc (#scale[0.8]{#sigma_{i#eta i#eta}#geq 0.011})","F")
		e.SetTextSize(LegendFontSize)
		e=l.AddEntry(Bkg["truth-err"],"mc-truth (#scale[0.8]{#sigma_{i#eta i#eta}< 0.011})","F")
		e.SetTextSize(LegendFontSize)
	else:
		e=l.AddEntry(Bkg["mc"],"mc (#scale[0.8]{#sigma_{i#eta i#eta}#geq 0.011})","L")
		e.SetTextSize(LegendFontSize)
		e=l.AddEntry(Bkg["truth"],"mc-truth (#scale[0.8]{#sigma_{i#eta i#eta}< 0.011})","L")
		e.SetTextSize(LegendFontSize)
	M=max(Bkg["data"].GetMaximum(),Bkg["truth"].GetMaximum(),Bkg["mc"].GetMaximum())
	Bkg["data"].SetMaximum(M*1.2)
	l.Draw()
	Bkg["legend"]=l
	txt.DrawLatex(.5,.94,"Background Templates")

	C.SaveAs(WorkDir+"/plots/Templates_Pt%.0f_%.0f.pdf"%(PtCuts[p],PtCuts[p+1]))
	

