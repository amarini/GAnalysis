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

inputFileNameUnfoldStudies=WorkDir + "/UnfoldStudies.root"  

ROOT.gSystem.Load("libGAnalysis.so") ##for syst names

file= ROOT.TFile.Open(inputFileNameUnfoldStudies)

def Ratio(H,H1,NoErrorH=False):
	R=H1.Clone(H1.GetName()+"_ratio")
	hTmp=H.Clone("tmp")
	#in order to account error properly in ratios
	if NoErrorH:
		for i in range(1,hTmp.GetNbinsX()+1):
			hTmp.SetBinError(i,0)
	R.Divide(hTmp)
	return R

#LOOP OVER THE BINs
for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	

		Bin="Ht_"+str(HtCuts[h])+"_nJets_"+str(nJetsCuts[nj])

		Dir=Bin	+"/"
		H_svd={}
		H_bayes={}
		for par in range(5,36,3):
			H_svd[par]=file.Get(Dir+"u_svd_par%dHt_%.1f_nJets_%.1f"%(par,HtCuts[h],nJetsCuts[nj]))
			H_svd[par].SetMarkerStyle(20);
			H_svd[par].SetMarkerSize(0.4);
			if par <= 5:
				H_svd[par].SetMarkerColor(ROOT.kRed+3);
			elif par <= 8:
				H_svd[par].SetMarkerColor(ROOT.kRed+1);
			elif par <= 11:
				H_svd[par].SetMarkerColor(ROOT.kRed-4);
			elif par <= 14:
				H_svd[par].SetMarkerColor(ROOT.kRed-7);
			elif par <= 17:
				H_svd[par].SetMarkerColor(ROOT.kRed-9);
			elif par <= 20:
				H_svd[par].SetMarkerColor(ROOT.kMagenta-7);
			elif par <= 23:
				H_svd[par].SetMarkerColor(ROOT.kMagenta-4);
			elif par <= 26:
				H_svd[par].SetMarkerColor(ROOT.kMagenta);
			elif par <= 29:
				H_svd[par].SetMarkerColor(ROOT.kMagenta+2);
			elif par <= 32:
				H_svd[par].SetMarkerColor(ROOT.kMagenta+3);
			elif par <= 35:
				H_svd[par].SetMarkerColor(ROOT.kMagenta+4);
			H_svd[par].SetLineColor(H_svd[par].GetMarkerColor())
		for par in range(1,8,2):
			H_bayes[par]=file.Get(Dir+"u_bayes_par%dHt_%.1f_nJets_%.1f"%(par,HtCuts[h],nJetsCuts[nj]))
			H_bayes[par].SetMarkerStyle(24);
			H_bayes[par].SetMarkerSize(0.4);
			if par <= 1:
				H_bayes[par].SetMarkerColor(ROOT.kBlue+3);
			elif par <= 3:
				H_bayes[par].SetMarkerColor(ROOT.kBlue+1);
			elif par <= 5:
				H_bayes[par].SetMarkerColor(ROOT.kBlue-4);
			elif par <= 7:
				H_bayes[par].SetMarkerColor(ROOT.kBlue-7);
			H_bayes[par].SetLineColor(H_bayes[par].GetMarkerColor())
		H_invert=file.Get(Dir+"u_invert_par7Ht_%.1f_nJets_%.1f"%(HtCuts[h],nJetsCuts[nj])) ##FIXME: PAR in name
		H_invert.SetMarkerStyle(23);
		H_invert.SetMarkerSize(0.5);
		H_invert.SetMarkerColor(ROOT.kBlack)
		H_invert.SetLineColor(H_invert.GetMarkerColor())

		H=file.Get(Dir+"r_Ht_%.1f_nJets_%.1f"%(HtCuts[h],nJetsCuts[nj])) ##
		G=file.Get(Dir+"g_Ht_%.1f_nJets_%.1f"%(HtCuts[h],nJetsCuts[nj])) ##

		
		## CANVAS
		C=ROOT.TCanvas("C","C")
		C.SetLogx()
		C.SetLogy()
		
		## PLOT STYLE
		H.SetMarkerStyle(20)
		H.SetMarkerColor(ROOT.kGray+3)
		H.SetMarkerSize(0.4)
		H.SetLineColor(ROOT.kGray+3)
	
		## AXIS
		H.GetXaxis().SetTitle("p_{T}^{#gamma}");
		H.GetYaxis().SetTitle("L #frac{d#sigma}{dp_{T}}[fb^{-1}/GeV]");
		H.GetXaxis().SetMoreLogLabels()
		H.GetXaxis().SetNoExponent()

		#DRAW
		H.Draw("P")
		H.Draw("AXIS X+ Y+ SAME")
		for key in H_svd:
			H_svd[key].Draw("P SAME")
		for key in H_bayes:
			H_bayes[key].Draw("P SAME")
		H_invert.Draw("P SAME")
	
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
			
		
		L=ROOT.TLegend(0.65,0.60,.89,.89,Header)
		L.SetFillStyle(0)
		L.SetBorderSize(0)
		L.AddEntry(H,"RECO")
		L.AddEntry(H_svd[5],"svd 5")
		L.AddEntry(H_svd[14],"svd 14")
		L.AddEntry(H_svd[23],"svd 23")
		L.AddEntry(H_svd[35],"svd 35")
		L.AddEntry(H_bayes[1],"bayes 1")
		L.AddEntry(H_bayes[3],"bayes 3")
		L.AddEntry(H_bayes[5],"bayes 5")
		L.AddEntry(H_bayes[7],"bayes 7")
		L.AddEntry(H_invert,"Inversion")
		L.Draw()
		#SAVE
		C.SaveAs(WorkDir+"plots/unfoldStudies_Ht%.0f_nJets%.0f.pdf"%(HtCuts[h],nJetsCuts[nj]))		
		C.SaveAs(WorkDir+"plots/unfoldStudies_Ht%.0f_nJets%.0f.root"%(HtCuts[h],nJetsCuts[nj]))		

		C2=ROOT.TCanvas("C2","C2")
		C2.SetLogx()

		R_H=Ratio(H,H,NoErrorH=True);
		R_H.GetYaxis().SetRangeUser(0.9,2.4)
		R_H.GetYaxis().SetTitle("Unfold/Reco")
		R_bayes={}
		R_svd={}
		for key in H_bayes:
			R_bayes[key]=Ratio(H,H_bayes[key],NoErrorH=True)
		for key in H_svd:
			R_svd[key]=Ratio(H,H_svd[key],NoErrorH=True)
		R_invert=Ratio(H,H_invert,NoErrorH=True)

		R_H.Draw("P")
		R_H.Draw("AXIS X+ Y+ SAME")
		for key in R_svd:
			R_svd[key].Draw("P SAME")
		for key in R_bayes:
			R_bayes[key].Draw("P SAME")
		R_invert.Draw("P SAME")
		
		L.Draw("SAME")

		R_H.Draw("P SAME") # redraw on top
		C2.SaveAs(WorkDir+"plots/unfoldStudiesRatio_Ht%.0f_nJets%.0f.pdf"%(HtCuts[h],nJetsCuts[nj]))		
		C2.SaveAs(WorkDir+"plots/unfoldStudiesRatio_Ht%.0f_nJets%.0f.root"%(HtCuts[h],nJetsCuts[nj]))		

