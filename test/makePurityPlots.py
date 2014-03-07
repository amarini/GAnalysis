#!/usr/bin/python
import sys,os
import array
import time
from optparse import OptionParser

DEBUG=1

if(DEBUG>0):print "-PARSING OPTIONS-"
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)
parser.add_option("","--inputDat" ,dest='inputDat',type='string',help="Input Configuration file",default="")
parser.add_option("","--inputDatMC" ,dest='inputDatMC',type='string',help="MC Input Configuration file",default="")

(options,args)=parser.parse_args()

import ROOT

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

if(DEBUG>0):print "----- BEGIN -----"


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

inputFileNameFit=WorkDir + "/fit.txt" 

doMC=False
if not options.inputDatMC == "": 
	doMC=True
	if(DEBUG>0): print "--> load dat file: "+options.inputDatMC
	configMC=read_dat(options.inputDatMC)
	if(DEBUG>0):
        	print "--------- MC CONFIG -----------"
        	PrintDat(configMC)
	WorkDirMC=ReadFromDat(configMC,"WorkDir","./","-->Set Default MC WDIR")
	inputFile=WorkDirMC+ReadFromDat(configMC,"outputFileName","output","-->Set Default Output") + ".root"
	fMC=ROOT.TFile.Open(inputFile)
	


if DEBUG>0 : print "--> Read File"
fFit= open(inputFileNameFit,"r")

if DEBUG>0:print "--> Read Fraction"
#READ FITTED FRACTION IN A DATABASE
#Pt 43.5 48.3 Ht 0.0 nJets 1 Fraction= 0.528608322144 ERROR= 0.000138673000038
Frac={};
FracBias={};
FracErr={};
for line in fFit:
	#exclude not well done lines
	if '#' in line : continue
	if len(line) <5 : continue
	l=line.split(' ')
	for iWord in range(0,len(l)):
		if "Pt" == l[iWord] :
			ptmin= round(float(l[iWord+1]),1)
			ptmax= round(float(l[iWord+2]),1)
		elif "Ht" in l[iWord]:
			ht=float(l[iWord+1])
		elif "nJets" in l[iWord]:
			nj=float(l[iWord+1])
		elif "jetPt" in l[iWord]:
			jpt=float(l[iWord+1])
		elif "Fraction" in l[iWord]:
			fr=float(l[iWord+1])
		elif "TOYS" in l[iWord]: #read error from toys
			er=float(l[iWord+1])
		elif "BIAS" in l[iWord]: #read error from toys
			bias=float(l[iWord+1])
	try:
		Frac[ (ptmin,ptmax,ht,nj,jpt) ] = fr
	except NameError: continue;
	try:
		FracErr[ (ptmin,ptmax,ht,nj,jpt) ] = er
	except NameError: continue;
	try:
		FracBias[ (ptmin,ptmax,ht,nj,jpt) ] = bias
	except NameError: continue;

#Float_t * is needed for TH1D
ROOT.gROOT.ProcessLine("struct Bins{ \
		Double_t PtBins[1023];\
		};")

from ROOT import Bins
PtBins=ROOT.Bins()

#LOOP OVER THE BINs
AllH={}
AllHMC={}
C=ROOT.TCanvas("C","C")
L=ROOT.TLegend(0.65,0.15,.89,.45)
L.SetFillStyle(0)
L.SetBorderSize(0)
C.SetLogx()
jpt=30.
for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	
		#CREATE TARGET HISTO
		try:
			PtCuts2_tmp=PtCuts[0:PtCuts.index(-1) ]
		except ValueError: PtCuts2_tmp=PtCuts

		PtCuts2=[]
		for pt in PtCuts2_tmp:		
			PtCuts2.append(round(pt,1));

		for c in range(0,len(PtCuts2)):
			PtBins.PtBins[c]=PtCuts2_tmp[c] ## bin for histo with high precision
		Bin="Ht_"+str(HtCuts[h])+"_nJets_"+str(nJetsCuts[nj])
		#Will it work?
		H=ROOT.TH1D("f_"+Bin,"Fraction_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )
		HBias=ROOT.TH1D("bias_"+Bin,"Bias_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )
		if doMC:
			HMC=ROOT.TH1D("mc_"+Bin,"Fraction_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )

		for p in range(0,len(PtCuts2)-1):
			## TAKE FITTED FRACTION
			try:
				fr=Frac[ (PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt) ]
			except (IndexError,KeyError): 
				print "ERROR IN FRACTION: Pt %.1f %.1f Ht %.0f nJ %.0f JetPt %.0f"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt)
				fr=1	
			try:
				er=FracErr[ (PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt) ]
			except (IndexError,KeyError): 
				print "ERROR IN ERR: Pt %.1f %.1f Ht %.0f nJ %.0f JetPt %.0f"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt)
				er=1	
			try:
				bias=FracBias[ (PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt) ]
			except (IndexError,KeyError): 
				print "ERROR IN BIAS: Pt %.1f %.1f Ht %.0f nJ %.0f JetPt %.0f"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],nJetsCuts[nj],jpt)
				bias=1	
			H.SetBinContent( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), fr )
			H.SetBinError( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), er )

			HBias.SetBinContent( H.FindBin( (PtCuts2[p]+PtCuts2[p+1])/2.), bias )

			if doMC:
				RU= fMC.Get("gammaPt_RECO_UNFOLD_VPt_0_8000_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%d"%(HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]))
				RE= fMC.Get("gammaPt_VPt_%.0f_%.0f_Ht_%.0f_8000_phid_%.3f_%.3f_nJets_%d"%(PtCuts2[p],PtCuts2[p+1],HtCuts[h],SigPhId[0],SigPhId[1],nJetsCuts[nj]))
				try:
					frmc= RU.GetBinContent( RU.FindBin((PtCuts2[p]+PtCuts2[p+1])/2.) ) / RE.Integral()
				except AttributeError: 
					print "--ERROR in MC Fraction: Pt %.0f Ht %.0f nJets %d"%(PtCuts2[p],HtCuts[h],nJetsCuts[nj])
					frmc=0
				HMC.SetBinContent( HMC.FindBin((PtCuts2[p]+PtCuts2[p+1])/2.) , frmc)
		## PLOT HISTOS
		if   HtCuts[h] == 0 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kBlack)
			H.SetMarkerStyle(20)
			if doMC: 
				HMC.SetLineColor(ROOT.kBlack)
				HMC.SetLineWidth(2)
				HMC.SetLineStyle(ROOT.kDashed)
			HBias.SetLineColor(ROOT.kBlack)
			HBias.SetLineWidth(2)
			HBias.SetLineStyle(3)
		elif HtCuts[h] == 100 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kRed+1)
			H.SetLineColor(ROOT.kRed+1)
			H.SetMarkerStyle(33)
			if doMC: 
				HMC.SetLineColor(ROOT.kRed)
				HMC.SetLineWidth(2)
				HMC.SetLineStyle(ROOT.kDashed)
			HBias.SetLineColor(ROOT.kRed+1)
			HBias.SetLineWidth(2)
			HBias.SetLineStyle(3)
		elif HtCuts[h] == 300 and nJetsCuts[nj]==1:
			H.SetMarkerColor(ROOT.kBlue-3)
			H.SetLineColor(ROOT.kBlue-3)
			H.SetMarkerStyle(29)
			if doMC: 
				HMC.SetLineColor(ROOT.kBlue-3)
				HMC.SetLineWidth(2)
				HMC.SetLineStyle(ROOT.kDashed)
			HBias.SetLineColor(ROOT.kBlue-3)
			HBias.SetLineWidth(2)
			HBias.SetLineStyle(3)
		elif HtCuts[h] == 0 and nJetsCuts[nj]==3:
			H.SetMarkerColor(ROOT.kGreen+2)
			H.SetLineColor(ROOT.kGreen+2)
			H.SetMarkerStyle(21)
			H.SetMarkerSize(0.8)
			if doMC: 
				HMC.SetLineColor(ROOT.kGreen+2)
				HMC.SetLineWidth(2)
				HMC.SetLineStyle(ROOT.kDashed)
			HBias.SetLineColor(ROOT.kGreen+2)
			HBias.SetLineWidth(2)
			HBias.SetLineStyle(3)
		else:
			H.SetMarkerStyle(25)
		#DRAW
		H.SetFillStyle(0);
		H.SetFillColor(H.GetLineColor());
		if   h== 0 and nj==0:
			print "Draw"
			H.GetXaxis().SetTitle("p_{T}^{#gamma}");
			H.GetYaxis().SetTitle("Purity");
			H.GetXaxis().SetMoreLogLabels()
			H.GetXaxis().SetNoExponent()
			H.GetYaxis().SetRangeUser(0,1);
			H.Draw("P E4")
		else:
			print "Draw h"+str(h)+" nj"+str(nj)
			H.Draw("P E4 SAME")
		HBias.Draw("HIST SAME")

		if doMC:
			HMC.Draw("HIST SAME")
			AllHMC[ (h,nj) ] = HMC

		L.AddEntry(H,"H_{T}>"+str(HtCuts[h])+" N_{jets}#geq"+str(nJetsCuts[nj]))

		AllH[ (h,nj) ] = H
L.Draw()
C.SaveAs(WorkDir+"plots/fraction.pdf")		
C.SaveAs(WorkDir+"plots/fraction.root")		
