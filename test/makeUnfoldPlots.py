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

inputFileNameUnfold=WorkDir + "/UnfoldedDistributions.root"  

ROOT.gSystem.Load("Analyzer.so") ##for syst names
file= ROOT.TFile.Open(inputFileNameUnfold)

def makeBands(h1,h2,type="Mean"):
	H=h1.Clone(h1.GetName()+"_band")
	for i in range(0,h1.GetNbinsX()):
		if type=="First":
			H.SetBinContent(i, h1.GetBinContent(i))
		else: #type = "Mean"
			H.SetBinContent(i, (h1.GetBinContent(i)+h2.GetBinContent(i) )/2.0)
		H.SetBinError  (i, math.fabs(h1.GetBinContent(i)-h2.GetBinContent(i) )/2.0)
	return H

#LOOP OVER THE BINs
for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	

		Bin="Ht_"+str(HtCuts[h])+"_nJets_"+str(nJetsCuts[nj])
	
		#GET HISTOS
		H=file.Get("b_Ht_%.1f_nJets_%.1f"%(HtCuts[h],nJetsCuts[nj]))
		H_PUUP    =file.Get("b_Ht_%.1f_nJets_%.1f%s"%(HtCuts[h],nJetsCuts[nj],ROOT.Analyzer.SystName(ROOT.Analyzer.PUUP)))
		H_PUDN    =file.Get("b_Ht_%.1f_nJets_%.1f%s"%(HtCuts[h],nJetsCuts[nj],ROOT.Analyzer.SystName(ROOT.Analyzer.PUDN)))
		H_JESUP   =file.Get("b_Ht_%.1f_nJets_%.1f%s"%(HtCuts[h],nJetsCuts[nj],ROOT.Analyzer.SystName(ROOT.Analyzer.JESUP)))
		H_JESDN   =file.Get("b_Ht_%.1f_nJets_%.1f%s"%(HtCuts[h],nJetsCuts[nj],ROOT.Analyzer.SystName(ROOT.Analyzer.JESDN)))
		H_SIGSHAPE=file.Get("b_Ht_%.1f_nJets_%.1f%s"%(HtCuts[h],nJetsCuts[nj],ROOT.Analyzer.SystName(ROOT.Analyzer.SIGSHAPE)))
		H_BKGSHAPE=file.Get("b_Ht_%.1f_nJets_%.1f%s"%(HtCuts[h],nJetsCuts[nj],ROOT.Analyzer.SystName(ROOT.Analyzer.BKGSHAPE)))
	
		H_PU=makeBands(H_PUUP,H_PUDN)
		H_JES=makeBands(H_JESUP,H_JESDN)
		H_SIG=makeBands(H,H_SIGSHAPE,"First")
		H_BKG=makeBands(H,H_BKGSHAPE,"First")
		
		## CANVAS
		C=ROOT.TCanvas("C","C")
		C.SetLogx()
		C.SetLogy()
		
		## PLOT STYLE
		H.SetMarkerStyle(20)
		H.SetMarkerColor(ROOT.kBlack)
		H.SetLineColor(ROOT.kBlack)
	
		H_PU.SetMarkerStyle(0)
		H_PU.SetFillColor  (ROOT.kBlue-4)
		H_PU.SetMarkerColor(ROOT.kBlue-4)
		H_PU.SetLineColor  (ROOT.kBlue-4)
		H_PU.SetFillStyle(3001)
		
		H_JES.SetMarkerStyle(0)
		H_JES.SetFillColor  (ROOT.kGreen-4)
		H_JES.SetMarkerColor(ROOT.kGreen-4)
		H_JES.SetLineColor  (ROOT.kGreen-4)
		H_JES.SetFillStyle(3002)
		
		H_SIG.SetMarkerStyle(0)
		H_SIG.SetFillColor  (ROOT.kMagenta+2)
		H_SIG.SetMarkerColor(ROOT.kMagenta+2)
		H_SIG.SetLineColor  (ROOT.kMagenta+2)
		H_SIG.SetFillStyle(3002)
		
		H_BKG.SetMarkerStyle(0)
		H_BKG.SetFillColor  (ROOT.kRed-4)
		H_BKG.SetMarkerColor(ROOT.kRed-4)
		H_BKG.SetLineColor  (ROOT.kRed-4)
		H_BKG.SetFillStyle(3003)

		## AXIS
		H.GetXaxis().SetTitle("p_{T}^{#gamma}");
		H.GetYaxis().SetTitle("L #frac{d#sigma}{dp_{T}}[fb^{-1}/GeV]");
		H.GetXaxis().SetMoreLogLabels()
		H.GetXaxis().SetNoExponent()

		#DRAW
		H.Draw("P")
		H.Draw("AXIS X+ Y+ SAME")
		H_BKG.Draw("P E3 SAME")
		H_PU.Draw("P E3 SAME")
		H_JES.Draw("P E3 SAME")
		H_SIG.Draw("P E3 SAME")
		H.Draw("P SAME") # redraw on top

		## TEXT
		l=ROOT.TLatex()
		l.SetNDC()
		l.SetTextFont(63)
		l.SetTextSize(30)
		l.SetTextAlign(22);
		l.DrawLatex(0.28,.85,"CMS Preliminary")
		l.SetTextFont(43)
		l.SetTextSize(24)
		l.DrawLatex(.28,.80,"#sqrt{s} = 8TeV, #it{L} = 19.7fb^{-1}")
		## LEGEND
	
		if HtCuts[h] == 0:
			Header="N_{jets} #geq %.0f"%(nJetsCuts[nj])
		else:
			Header="H_{T} > %.0f GeV, N_{jets} #geq %.0f"%(HtCuts[h],nJetsCuts[nj])
			
		
		L=ROOT.TLegend(0.65,0.55,.89,.89,Header)
		L.SetFillStyle(0)
		L.SetBorderSize(0)
		L.AddEntry(H,"Data")
		L.AddEntry(H_PU,"PU Syst")
		L.AddEntry(H_JES,"JES Syst")
		L.AddEntry(H_SIG,"SIG shape Syst")
		L.AddEntry(H_BKG,"BKG shape Syst")

		L.Draw()
		#SAVE
		C.SaveAs(WorkDir+"plots/unfoldedPlots_Ht%.0f_nJets%.0f.pdf"%(HtCuts[h],nJetsCuts[nj]))		
		C.SaveAs(WorkDir+"plots/unfoldedPlots_Ht%.0f_nJets%.0f.root"%(HtCuts[h],nJetsCuts[nj]))		
