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

inputFileNameFit=WorkDir + "/fitPars.txt"  


if DEBUG>0 : print "--> Read File"
fFit= open(inputFileNameFit,"r")

if DEBUG>0:print "--> Read Fraction"
#READ FITTED FRACTION IN A DATABASE
#Pt 43.5 48.3 Ht 0.0 nJets 1 Fraction= 0.528608322144 ERROR= 0.000138673000038
Par0={};
Par1={};
Par2={};
for line in fFit:
	#exclude not well done lines
	if '#' in line : continue
	if len(line) <5 : continue
	l=line.split(' ')
	for iWord in range(0,len(l)):
		if "Pt" in l[iWord] :
			ptmin=float(l[iWord+1])
			ptmax=float(l[iWord+2])
		elif "Ht" in l[iWord]:
			ht=float(l[iWord+1])
		elif "nJets" in l[iWord]:
			nj=float(l[iWord+1])
		elif "Par0" in l[iWord]:
			p0=float(l[iWord+1])
		elif "Par1" in l[iWord]:
			p1=float(l[iWord+1])
		elif "Par2" in l[iWord]:
			p2=float(l[iWord+1])
	try:
		Par0[ (ptmin,ptmax,ht,nj) ] = p0
		Par1[ (ptmin,ptmax,ht,nj) ] = p1
		Par2[ (ptmin,ptmax,ht,nj) ] = p2
	except NameError: continue;

#Float_t * is needed for TH1F
ROOT.gROOT.ProcessLine("struct Bins{ \
		Float_t PtBins[1023];\
		};")

from ROOT import Bins
PtBins=ROOT.Bins()

#LOOP OVER THE BINs
AllH=[]
C=ROOT.TCanvas("C","C")
L=ROOT.TLegend(0.65,0.15,.89,.45)
L.SetFillStyle(0)
L.SetBorderSize(0)
C.SetLogx()
for h in range(0,len(HtCuts)):
	for nj in range(0,len(nJetsCuts)):
		if nJetsCuts[nj] != 1 and HtCuts[h] !=0:continue;	
		#CREATE TARGET HISTO
		try:
			PtCuts2=PtCuts[0:PtCuts.index(-1) ]
		except ValueError: PtCuts2=PtCuts

		for c in range(0,len(PtCuts2)):
			PtBins.PtBins[c]=PtCuts2[c]
		Bin="Ht_"+str(HtCuts[h])+"_nJets_"+str(nJetsCuts[nj])
		#Will it work?
		H0=ROOT.TH1F("h0_"+Bin,"Par0_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )
		H1=ROOT.TH1F("h1_"+Bin,"Par1_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )
		H2=ROOT.TH1F("h2_"+Bin,"Par2_"+Bin , len(PtCuts2)-1 , PtBins.PtBins )

		for p in range(0,len(PtCuts2)-1):
			try:
				p0=Par0[ (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]
				p1=Par1[ (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]
				p2=Par2[ (PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj]) ]
			except (IndexError,KeyError): 
				print "ERROR IN PARS: Pt %.1f %.1f Ht %.0f nJ %.0f"%(PtCuts[p],PtCuts[p+1],HtCuts[h],nJetsCuts[nj])
				p0=-999	
				p1=-999
				p2=-999
			H0.SetBinContent( H0.FindBin( (PtCuts[p]+PtCuts[p+1])/2.), p0 ) ## NORMALIZATION
			H1.SetBinContent( H1.FindBin( (PtCuts[p]+PtCuts[p+1])/2.), p1 )
			H2.SetBinContent( H2.FindBin( (PtCuts[p]+PtCuts[p+1])/2.), p2 )

		H0.SetMarkerStyle(33)
		H1.SetMarkerStyle(20)
		H2.SetMarkerStyle(21)
		H2.SetMarkerSize(0.8)
		## PLOT HISTOS
		if   HtCuts[h] == 0 and nJetsCuts[nj]==1:
			H0.SetMarkerColor(ROOT.kBlack)
			H0.SetLineColor(ROOT.kBlack)
			H1.SetMarkerColor(ROOT.kBlack)
			H1.SetLineColor(ROOT.kBlack)
			H2.SetMarkerColor(ROOT.kBlack)
			H2.SetLineColor(ROOT.kBlack)
		elif HtCuts[h] == 100 and nJetsCuts[nj]==1:
			H0.SetMarkerColor(ROOT.kRed+1)
			H0.SetLineColor(ROOT.kRed+1)
			H1.SetMarkerColor(ROOT.kRed+1)
			H1.SetLineColor(ROOT.kRed+1)
			H2.SetMarkerColor(ROOT.kRed+1)
			H2.SetLineColor(ROOT.kRed+1)
		elif HtCuts[h] == 300 and nJetsCuts[nj]==1:
			H0.SetMarkerColor(ROOT.kBlue-3)
			H0.SetLineColor(ROOT.kBlue-3)
			H1.SetMarkerColor(ROOT.kBlue-3)
			H1.SetLineColor(ROOT.kBlue-3)
			H2.SetMarkerColor(ROOT.kBlue-3)
			H2.SetLineColor(ROOT.kBlue-3)
		elif HtCuts[h] == 0 and nJetsCuts[nj]==3:
			H0.SetMarkerColor(ROOT.kGreen+2)
			H0.SetLineColor(ROOT.kGreen+2)
			H1.SetMarkerColor(ROOT.kGreen+2)
			H1.SetLineColor(ROOT.kGreen+2)
			H2.SetMarkerColor(ROOT.kGreen+2)
			H2.SetLineColor(ROOT.kGreen+2)
		else:
			H0.SetMarkerStyle(25)
			H1.SetMarkerStyle(25)
			H2.SetMarkerStyle(25)
		#DRAW
		if   h== 0 and nj==0:
			print "Draw"
			H1.GetXaxis().SetTitle("p_{T}^{#gamma}");
			H1.GetYaxis().SetTitle("Landau Parl");
			H1.GetXaxis().SetMoreLogLabels()
			H1.GetXaxis().SetNoExponent()
			H1.GetYaxis().SetRangeUser(0,ROOT.TMath.Max(H1.GetMaximum(),H2.GetMaximum())*1.3);
			H1.Draw("P")
			#H0.Draw("P SAME")
			H2.Draw("P SAME")
		else:
			print "Draw h"+str(h)+" nj"+str(nj)
			#H0.Draw("P SAME")
			H1.Draw("P SAME")
			H2.Draw("P SAME")

		AllH.append(H0)
		AllH.append(H1)
		AllH.append(H2)
		
		L.AddEntry(H1,"Par1 H_{T}>"+str(HtCuts[h])+" N_{jets}#geq"+str(nJetsCuts[nj]))
		L.AddEntry(H2,"Par2 H_{T}>"+str(HtCuts[h])+" N_{jets}#geq"+str(nJetsCuts[nj]))

L.Draw()
C.SaveAs(WorkDir+"plots/pars.pdf")		
